from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import p, rich_callout, style_xml, table
from build_phase2_docx import image_paragraph
from build_phase9_docx import (
    NS_A,
    NS_PIC,
    NS_R,
    NS_W,
    NS_WP,
    app_xml,
    content_types_xml,
    font_table_xml,
    numbering_xml,
    root_rels_xml,
    sect_pr,
    settings_xml,
)


OUT = Path("docs/Smart_Sportz_Database_Master_Triple_DB_Backup_Logging_Architecture.docx")
ASSET_DIR = Path("docs/assets")


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def document_xml() -> str:
    body: list[str] = []

    body.append(p("SMART SPORTZ - DATABASE MASTER ARCHITECTURE", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Triple Database, Mirror Backup, Logging, JSON Export, Encryption and Redis Blueprint", style="Subtitle"))
    body.append(p("Consolidated from Smart Sportz Phase Documents", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Database Master Triple-DB Backup and Logging Architecture"],
        ["Project", "Smart Sportz"],
        ["Source Phases", "Phase 8 Backend Architecture, Phase 9 Database Architecture, Backend Master Specification, DevOps Phase, and all product phases that define tournaments, registrations, payments, live scores, CMS, reports, audit logs, and operations"],
        ["Database Scope", "DB-1 editable primary data store, DB-2 immutable mirror backup store, DB-3 software event/login/log database, encrypted JSON exports, Redis sessions/cache/live state, PostgreSQL/Prisma modeling, security, backup, restore, and monitoring"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Database Master Intent", [
        "This document defines the Smart Sportz database architecture using three separate database responsibilities: DB-1 for editable transactional data, DB-2 for immutable mirrored backup data, and DB-3 for software events, login records, audit trails, and operational logs.",
        "It also defines encrypted JSON table backups, secure handling of passwords and sensitive data, Redis usage for session/cache/live data, and database workflows aligned with the existing phase documents."
    ]))

    body.append(p("1. Architecture Objective", style="Heading1"))
    body.append(p("Design a secure, recoverable, auditable, and scalable database architecture for Smart Sportz that supports enterprise tournament management, registrations, payments, live scoring, CMS, reports, and platform operations."))
    body.extend(bullets([
        "DB-1 is the primary editable PostgreSQL database used by the live application for normal create, update, delete, soft-delete, and transactional workflows.",
        "DB-2 is the immutable mirror backup PostgreSQL database used for backup, recovery, investigation, and data safety. Application users must not edit or delete DB-2 records.",
        "DB-3 is the separate log database used for software events, login events, audit logs, security events, integration events, job logs, and operational observability.",
        "Redis is used for sessions, cache, live match active state, queues, rate limits, and temporary operational data. Redis is not the permanent source of truth.",
        "DB-1 and DB-2 should behave like a RAID-style mirror at the data architecture level. Technically, this is best implemented as logical replication/change capture plus immutable backup controls rather than an editable duplicate.",
    ]))

    body.append(p("2. Triple Database Topology", style="Heading1"))
    body.append(p("The architecture separates transactional data, immutable backup data, and log/event data so each store can use the correct permissions, retention, performance, and recovery rules."))
    body.append(image_paragraph("rIdImage1", "Smart Sportz Triple Database Topology", "Smart Sportz triple database topology diagram", 1))
    body.append(table([
        ["Store", "Purpose"],
        ["DB-1 Primary", "Editable operational database for users, roles, organizations, tournaments, registrations, teams, players, matches, live score history, payments, CMS, reports, and settings."],
        ["DB-2 Mirror Backup", "Immutable mirror database that receives DB-1 changes for backup and recovery. Insert-only or append-versioned. No application edit/delete permissions."],
        ["DB-3 Log Database", "Append-only software event database for login logs, audit logs, API events, Socket.IO events, payment webhooks, score corrections, background jobs, security events, and system errors."],
        ["Redis", "Session/cache/live-state layer with TTL and recovery from DB-1. Never treated as permanent record storage."],
        ["JSON Backup Storage", "Encrypted per-table JSON/NDJSON exports for DB-1 and DB-2 with manifests, checksums, signatures, and restore metadata."],
    ], [2300, 7060]))

    body.append(p("3. DB-1 Primary Database", style="Heading1"))
    body.append(table([
        ["Area", "DB-1 Rule"],
        ["Primary Role", "Live transactional source of truth for normal platform operations."],
        ["Allowed Actions", "Create, read, update, delete where required, soft delete for business entities, restore where allowed."],
        ["Access", "Application services access through Prisma repositories and service-layer transactions."],
        ["Data Model", "Normalized PostgreSQL schema with UUID primary keys, foreign keys, audit fields, indexes, and Prisma migrations."],
        ["Soft Delete", "Use deletedAt for business entities so data can be recovered and audit history remains meaningful."],
        ["Transactions", "Required for registration/payment workflows, score finalization, refunds, approval workflows, and multi-step updates."],
    ], [2300, 7060]))

    body.append(p("4. DB-2 Immutable Mirror Backup Database", style="Heading1"))
    body.append(p("DB-2 stores a protected mirror of DB-1. It must not be treated as a normal editable database. It exists for backup, restore, forensic review, and high-confidence recovery."))
    body.extend(bullets([
        "Use separate database credentials from DB-1. Application read/write users should not have update or delete permissions on DB-2.",
        "Write to DB-2 through controlled replication, change data capture, an outbox worker, or WAL/logical replication pipeline.",
        "Prefer append-versioned rows for changes: every DB-1 mutation creates a corresponding DB-2 immutable version with operation type, source table, source ID, version, timestamp, actor, checksum, and payload reference.",
        "Use WORM-style retention, restricted admin access, backups, and restore drills.",
        "DB-2 can be queried for recovery and investigation but should not power normal UI behavior unless explicitly switched during disaster recovery.",
    ]))

    body.append(p("5. DB-3 Log and Event Database", style="Heading1"))
    body.append(table([
        ["Log Type", "Examples"],
        ["Software Events", "Application start/stop, deployment marker, feature flag change, configuration update, job lifecycle."],
        ["Login Events", "Successful login, failed login, password reset, OTP request, token refresh, logout, session revoke."],
        ["Audit Events", "User change, role assignment, permission update, payment refund, approval, score correction, CMS publish."],
        ["API Events", "Endpoint, method, status, duration, correlation ID, user ID, IP, device, error code."],
        ["Socket Events", "Connection, disconnect, room join, live score command, broadcast, reconnect."],
        ["Payment Events", "Razorpay order, webhook received, signature verified, payment success/failure, refund status."],
        ["Security Events", "Rate limit hit, forbidden access, suspicious activity, API key event, credential rotation."],
    ], [2300, 7060]))

    body.append(p("6. Core ER Domain Diagram", style="Heading1"))
    body.append(p("DB-1 uses a relational model organized around identity, organizations, tournaments, registration, teams, players, fixtures, matches, payments, CMS, notifications, reporting, and settings."))
    body.append(image_paragraph("rIdImage2", "Smart Sportz Core ER Domain Diagram", "Smart Sportz core ER domain diagram", 2))

    body.append(p("7. Table Relationship Map", style="Heading1"))
    body.append(p("The table design should use explicit foreign keys, junction tables for many-to-many relationships, and indexed foreign key fields for high-volume workflows."))
    body.append(image_paragraph("rIdImage3", "High-Level Table Relationship Map", "High-level table relationship map diagram", 3))
    body.append(table([
        ["Domain", "Key Tables"],
        ["Identity", "User, Role, Permission, UserRole, RolePermission, Session, RefreshToken, PasswordReset."],
        ["Organization", "Organization, OrganizationSettings, BrandingSetting, IntegrationSetting."],
        ["Tournament", "Tournament, TournamentCategory, TournamentRule, TournamentStage, TournamentAnnouncement."],
        ["Sports and Venues", "Sport, SportRule, Venue, VenueArea, Court, Equipment."],
        ["Registration", "Registration, RegistrationDocument, Waitlist, Coupon, CouponUsage."],
        ["Teams and Players", "Team, TeamMember, TeamCoach, TeamManager, TeamDocument, Player, PlayerStatistics, PlayerMedical, PlayerAchievement."],
        ["Fixtures and Matches", "Fixture, Match, MatchPeriod, MatchEvent, MatchCommentary, MatchOfficial, LiveScore, ScoreSnapshot, ScoreCorrection."],
        ["Finance", "Payment, Refund, Invoice, Receipt."],
        ["CMS and Reports", "Page, Gallery, Sponsor, Blog, FAQ, Report, Schedule."],
        ["Logs", "SoftwareEventLog, LoginEventLog, AuditEventLog, ApiRequestLog, SocketEventLog, JobExecutionLog, SecurityEventLog."],
    ], [2300, 7060]))

    body.append(p("8. Write, Mirror, and JSON Backup Flow", style="Heading1"))
    body.append(p("Every important DB-1 mutation should be traceable through DB-2 mirror entries, DB-3 event logs, and encrypted JSON exports."))
    body.append(image_paragraph("rIdImage4", "Write, Mirror, and JSON Backup Data Flow", "Write mirror and JSON backup data flow diagram", 4))
    body.append(table([
        ["Step", "Requirement"],
        ["DB-1 Commit", "Business transaction completes in DB-1 through service-layer logic and Prisma transaction where required."],
        ["Change Capture", "Outbox table, WAL/logical replication, or worker captures table name, primary key, operation, timestamp, actor, payload checksum, and version."],
        ["DB-2 Mirror Write", "Append immutable mirror record or replicated row version. Never update or delete mirror data from application workflows."],
        ["DB-3 Log Write", "Record event metadata including correlation ID, user ID, IP, device, action, source module, and result."],
        ["JSON Export", "Export DB-1 and DB-2 table data separately as JSON or NDJSON with table name, schema version, export time, row count, checksum, and encrypted payload."],
        ["Verification", "Validate mirror lag, row counts, checksum match, restore test status, and backup object integrity."],
    ], [2300, 7060]))

    body.append(p("9. JSON Backup Strategy", style="Heading1"))
    body.extend(bullets([
        "Generate separate JSON/NDJSON backups for DB-1 and DB-2. Do not mix primary and mirror exports in the same file set.",
        "Use one file per table or table partition for large data volumes. Example: db1/tournaments/2026-07-05.ndjson.enc and db2/match_events/2026-07-05.ndjson.enc.",
        "Each export should include a signed manifest with database name, table name, schema version, export window, row count, checksum, encryption key version, and storage path.",
        "Encrypt every JSON backup before storage and keep key material outside the backup file.",
        "Compress after serialization and before encryption where the backup pipeline supports it.",
        "Periodically restore JSON backups into a temporary validation database to prove the backup is useful.",
    ]))

    body.append(p("10. Security and Encryption Model", style="Heading1"))
    body.append(p("Passwords should be hashed, not reversibly encrypted. Sensitive business data can use field-level encryption where needed. JSON backups and mirror storage must be encrypted and access-controlled."))
    body.append(image_paragraph("rIdImage5", "Database Security and Encryption Model", "Database security and encryption model diagram", 5))
    body.append(table([
        ["Data Type", "Protection"],
        ["Passwords", "Use Argon2id or bcrypt hash with per-user salt and optional server-side pepper. Never store plain passwords or reversible password encryption."],
        ["JWT and Refresh Tokens", "Store refresh tokens as hashed values or protected token fingerprints. Rotate refresh tokens and revoke on logout or suspicious activity."],
        ["PII", "Encrypt highly sensitive personal fields where required, such as medical details, identity document metadata, private contact data, and sensitive registration notes."],
        ["Payment Data", "Store gateway IDs, statuses, and required metadata. Do not store raw card details. Protect Razorpay keys through secret management."],
        ["Documents", "Private storage with signed URLs, document-level permissions, audit logs, and optional encryption-at-rest policies."],
        ["JSON Backups", "Encrypt with AES-256-GCM or equivalent envelope encryption, sign manifests, keep checksums, and apply retention rules."],
        ["Keys", "Use KMS or a secret manager, rotate keys periodically, version key IDs, and document re-encryption plans."],
    ], [2300, 7060]))

    body.append(p("11. Redis Session, Cache, Queue, and Live State Flow", style="Heading1"))
    body.append(p("Redis improves speed and live experience but must remain recoverable from DB-1. It is not a permanent system of record."))
    body.append(image_paragraph("rIdImage6", "Redis Session, Cache, Queue, and Live State Flow", "Redis session cache queue and live state flow diagram", 6))
    body.append(table([
        ["Redis Usage", "Rule"],
        ["Sessions", "Store session state, token revocation markers, short-lived auth metadata, and TTL-based session controls where needed."],
        ["Cache", "Cache public tournament lists, dashboard counts, live lookup data, permissions snapshots, and expensive report summaries with invalidation rules."],
        ["Live Score State", "Store current score, timer, period, active match snapshot, recent events, and Socket.IO room state for low-latency display."],
        ["Queues", "Support notification jobs, reports, exports, cache warming, cleanup, and retryable background tasks."],
        ["Rate Limits", "Track login attempts, OTP requests, payment retries, upload activity, and high-cost public endpoint usage."],
        ["Recovery", "Rebuild Redis from DB-1 and event history after restart or cache loss."],
    ], [2300, 7060]))

    body.append(p("12. DB-1 to DB-2 Mirror Method", style="Heading1"))
    body.append(p("The requested mirror behavior should be implemented as a database-level mirror pattern. Although the phrase RAID-2 was used, the practical behavior is a RAID-style mirror where DB-2 receives protected copies of DB-1 changes and remains immutable."))
    body.extend(bullets([
        "Use logical replication, WAL streaming, CDC, or an application outbox worker depending on deployment capability.",
        "Record operation type: INSERT, UPDATE, SOFT_DELETE, RESTORE, FINALIZE, PAYMENT_EVENT, SCORE_EVENT, SECURITY_EVENT.",
        "Use checksums to verify payload integrity between DB-1, DB-2, and JSON export manifests.",
        "Restrict DB-2 database roles to insert/read for the replication user and read-only for recovery/investigation users.",
        "Monitor replication lag and alert if mirror delay crosses the production threshold.",
    ]))

    body.append(p("13. Backup and Restore Policy", style="Heading1"))
    body.append(table([
        ["Backup Type", "Requirement"],
        ["DB-1 Physical Backup", "Daily automated backup, point-in-time recovery where supported, migration-safe restore test."],
        ["DB-2 Mirror Backup", "Immutable backup with restricted access, WORM retention, checksum validation, and restore drill."],
        ["DB-3 Log Backup", "Partitioned log backup with retention rules, security review access, and query archive strategy."],
        ["JSON Table Backup", "Encrypted per-table export for DB-1 and DB-2 with manifests and independent restore validation."],
        ["Disaster Recovery", "Document RPO, RTO, restore steps, rollback plan, emergency credential access, and verification checklist."],
    ], [2300, 7060]))

    body.append(p("14. Indexing and Performance", style="Heading1"))
    body.extend(bullets([
        "Index user email, phone, role, status, tournament status, sport, venue, registration status, payment status, match status, scheduled date, and live match flag.",
        "Use composite indexes for tournament plus status, match plus venue, payment plus date, registration plus tournament, and player/team search fields.",
        "Partition or archive very large DB-3 logs by date and event type.",
        "Use materialized views or summary tables for heavy reports such as revenue, participation, venue utilization, standings, and live match analytics.",
        "Use cursor pagination for large lists and table-driven admin screens.",
    ]))

    body.append(p("15. Compliance, Audit, and Investigation", style="Heading1"))
    body.append(table([
        ["Concern", "Database Requirement"],
        ["Audit History", "Every sensitive action should create immutable DB-3 logs and mirror evidence in DB-2 when it changes DB-1 state."],
        ["Login Review", "Successful login, failed login, OTP, reset, refresh, logout, revoke, and lockout events stored in DB-3."],
        ["Payment Traceability", "Order creation, webhook verification, payment status, refund, receipt, and invoice events linked across DB-1, DB-2, DB-3."],
        ["Score Correction", "Reason, old value, new value, operator, permission, timestamp, match, and public broadcast event stored."],
        ["Admin Change", "User, role, permission, settings, CMS publish, integration, and API key changes logged with before/after data."],
    ], [2300, 7060]))

    body.append(p("16. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Use PostgreSQL and Prisma for DB-1 primary data, DB-2 mirror data, and DB-3 event/log data unless infrastructure requires separate engines.",
        "Keep DB-1 editable through normal services and repositories; keep DB-2 immutable through restricted credentials and append-only mirror writes.",
        "Store software events, login events, audit logs, API logs, Socket.IO logs, payment webhook logs, security events, and job logs in DB-3.",
        "Create encrypted JSON/NDJSON backup exports for DB-1 and DB-2 separately, with manifests, checksums, signatures, and restore scripts.",
        "Hash passwords with Argon2id or bcrypt; encrypt sensitive fields and backup payloads using managed keys.",
        "Use Redis only for sessions, cache, live state, queues, and rate limits. Rebuild Redis from DB-1 if needed.",
        "Add health checks, replication lag checks, backup verification, restore tests, and audit queries.",
        "Do not add TODO comments, mock database behavior, or placeholder security logic.",
    ]))
    body.append(rich_callout("Database Master Completion Criteria", [
        "This database master document is complete when it defines DB-1 primary behavior, DB-2 immutable mirror backup behavior, DB-3 logging behavior, relational domains, table relationships, mirror replication, encrypted JSON backups, password hashing, field encryption, Redis usage, backup and restore policy, indexing, audit investigation, and implementation rules for Smart Sportz."
    ]))

    body.append(sect_pr())
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{NS_W}" xmlns:r="{NS_R}" xmlns:wp="{NS_WP}" xmlns:a="{NS_A}" xmlns:pic="{NS_PIC}">
  <w:body>
    {''.join(body)}
  </w:body>
</w:document>'''


def document_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  <Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rIdFontTable" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/database_triple_db_topology.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/database_er_domain_diagram.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/database_table_relationships.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/database_write_mirror_json_flow.png"/>
  <Relationship Id="rIdImage5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/database_security_encryption_model.png"/>
  <Relationship Id="rIdImage6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/database_redis_session_cache_flow.png"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Database Master Triple-DB Backup and Logging Architecture</dc:title>
  <dc:subject>Triple database architecture for DB-1 primary editable data, DB-2 immutable mirror backup, DB-3 logs, encrypted JSON backups, Redis sessions/cache/live state, security, backup, restore, and auditing</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/database_triple_db_topology.png": ASSET_DIR / "database_triple_db_topology.png",
        "word/media/database_er_domain_diagram.png": ASSET_DIR / "database_er_domain_diagram.png",
        "word/media/database_table_relationships.png": ASSET_DIR / "database_table_relationships.png",
        "word/media/database_write_mirror_json_flow.png": ASSET_DIR / "database_write_mirror_json_flow.png",
        "word/media/database_security_encryption_model.png": ASSET_DIR / "database_security_encryption_model.png",
        "word/media/database_redis_session_cache_flow.png": ASSET_DIR / "database_redis_session_cache_flow.png",
    }
    for source in assets.values():
        if not source.exists():
            raise FileNotFoundError(source)

    files = {
        "[Content_Types].xml": content_types_xml(),
        "_rels/.rels": root_rels_xml(),
        "docProps/core.xml": core_xml(),
        "docProps/app.xml": app_xml(),
        "word/document.xml": document_xml(),
        "word/_rels/document.xml.rels": document_rels_xml(),
        "word/styles.xml": style_xml(),
        "word/numbering.xml": numbering_xml(),
        "word/settings.xml": settings_xml(),
        "word/fontTable.xml": font_table_xml(),
    }
    with ZipFile(OUT, "w", ZIP_DEFLATED) as zf:
        for name, data in files.items():
            zf.writestr(name, data)
        for target, source in assets.items():
            zf.write(source, target)
    print(OUT.resolve())


if __name__ == "__main__":
    build()
