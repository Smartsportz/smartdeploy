from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_9_Database_Architecture_Prisma_Schema_Design.docx")
ASSET_DIR = Path("docs/assets")

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"


def sect_pr() -> str:
    page_borders = tag("w:pgBorders", {"w:offsetFrom": "page"}, body="".join([
        empty("w:top", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
        empty("w:left", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
        empty("w:bottom", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
        empty("w:right", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
    ]))
    return tag("w:sectPr", body="".join([
        empty("w:pgSz", {"w:w": "11906", "w:h": "16838"}),
        empty("w:pgMar", {"w:top": "720", "w:right": "720", "w:bottom": "720", "w:left": "720", "w:header": "720", "w:footer": "720", "w:gutter": "0"}),
        page_borders,
        empty("w:cols", {"w:space": "720"}),
        empty("w:docGrid", {"w:linePitch": "360"}),
    ]))


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def document_xml() -> str:
    body: list[str] = []

    body.append(p("PHASE 9 - DATABASE ARCHITECTURE & PRISMA SCHEMA DESIGN", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Enterprise Data Model", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 9 Database Architecture and Prisma Schema Design"],
        ["Project", "Smart Sportz"],
        ["Focus", "PostgreSQL, Prisma schema, normalized data domains, multi-role access, future multi-tenancy, tournaments, sports, live scoring, payments, reporting, audit logging, CMS, analytics, indexes, migrations, and seed data"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved Phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 9 Intent", [
        "This document defines the Smart Sportz enterprise data model. It converts the database prompt into a structured PostgreSQL and Prisma schema specification for normalized transactional data, live operations, payments, reporting, audit history, CMS, and future multi-tenant SaaS readiness.",
        "The schema must remain normalized where appropriate while supporting efficient reporting, live match operations, and immutable historical records."
    ]))

    body.append(p("1. Objective", style="Heading1"))
    body.append(p("Design a scalable PostgreSQL database using Prisma ORM that supports multi-role access, future multi-tenant architecture, unlimited tournaments, multiple sports, real-time scoring, payments, reporting, audit logging, CMS, and analytics."))
    body.extend(bullets([
        "Use normalized tables while adding indexes and summary patterns where reporting requires it.",
        "Separate live cached state from persistent historical events.",
        "Keep critical records such as payments, results, match events, and audit logs immutable once finalized.",
        "Support future organization-level tenancy without major schema refactoring.",
    ]))

    body.append(p("2. Database Principles", style="Heading1"))
    body.append(table([
        ["Principle", "Requirement"],
        ["Normalization", "Use Third Normal Form where appropriate while balancing reporting needs."],
        ["Primary Keys", "Use UUID primary keys across all models."],
        ["Soft Deletes", "Use deletedAt for business entities rather than physical deletion."],
        ["Audit Fields", "Include createdAt, updatedAt, deletedAt, createdBy, and updatedBy where appropriate."],
        ["Integrity", "Use explicit foreign key constraints and referential integrity."],
        ["Performance", "Add indexed search columns, composite indexes, pagination, and optimistic concurrency support."],
        ["Transactions", "Use transaction-safe operations for multi-step writes."],
    ], [2400, 6960]))

    body.append(p("3. Enterprise Data Domain Map", style="Heading1"))
    body.append(p("The Prisma schema should be organized into logical domains so the data model stays readable, scalable, and aligned with business ownership boundaries."))
    body.append(image_paragraph("rIdImage1", "Enterprise Data Domain Map", "Enterprise data domain map diagram", 1))

    body.append(p("4. Database Modules", style="Heading1"))
    body.append(table([
        ["Domain", "Models"],
        ["Identity and Security", "User, Role, Permission, RolePermission, UserRole, Session, RefreshToken, PasswordReset, AuditLog."],
        ["Organization", "Organization, OrganizationSettings, SubscriptionPlan."],
        ["Tournament", "Tournament, TournamentCategory, TournamentRule, TournamentStage, TournamentAnnouncement."],
        ["Sports and Venue", "Sport, SportRule, SportCategory, Venue, VenueArea, Court, Equipment."],
        ["Registration", "Registration, RegistrationDocument, Waitlist, Coupon, CouponUsage."],
        ["Teams and Players", "Team, TeamMember, TeamCoach, TeamManager, TeamDocument, Player, PlayerStatistics, PlayerMedical, PlayerAchievement."],
        ["Fixtures, Matches, Live Scores", "Fixture, Match, MatchPeriod, MatchEvent, MatchCommentary, MatchOfficial, LiveScore, ScoreSnapshot, ScoreCorrection."],
        ["Results and Payments", "Result, Leaderboard, Standing, Payment, Refund, Invoice, Receipt."],
        ["Notifications, CMS, Reporting, Settings", "Notification, Template, Queue, Page, Gallery, Sponsor, Blog, FAQ, Report, Schedule, PlatformSetting, BrandingSetting, IntegrationSetting."],
    ], [2600, 6760]))

    body.append(p("5. Core Relationships", style="Heading1"))
    body.append(table([
        ["Root Entity", "Relationships"],
        ["Organization", "Users, tournaments, venues, branding, settings, and future tenant-scoped resources."],
        ["Tournament", "Registrations, fixtures, matches, results, announcements, payments, teams, players, sponsors."],
        ["Team", "Players, registrations, team documents, coaches, managers, match participation."],
        ["Match", "Events, live score, officials, commentary, score snapshots, result."],
    ], [2400, 6960]))

    body.append(p("6. User and RBAC Model", style="Heading1"))
    body.append(p("Use many-to-many relationships between users, roles, and permissions. Permissions should be granular, configurable, and suitable for Super Admin management."))
    body.append(image_paragraph("rIdImage2", "User and RBAC Data Model", "User and RBAC data model diagram", 2))
    body.append(table([
        ["Model", "Purpose"],
        ["User", "Identity, contact details, login information, status, and profile."],
        ["Role", "Super Admin, Tournament Manager, Scorer, Finance Officer, Read Only, and custom roles."],
        ["Permission", "Granular keys such as tournament.create, tournament.edit, live.update, payment.refund, report.export."],
        ["AuditLog", "Immutable record of critical user, permission, and system actions."],
    ], [2300, 7060]))

    body.append(p("7. Tournament Model", style="Heading1"))
    body.append(table([
        ["Area", "Fields and Relations"],
        ["Tournament Core", "Name, code, description, sport, organizer, venue, registration dates, event dates, status, type, rules, prize information."],
        ["Related Entities", "Teams, players, fixtures, matches, sponsors, announcements, registrations, payments, results."],
        ["Future Support", "Tournament categories, stages, rules, hybrid formats, reporting, and multi-organization scope."],
    ], [2400, 6960]))

    body.append(p("8. Team and Player Model", style="Heading1"))
    body.append(table([
        ["Model", "Key Data"],
        ["Team", "Team name, logo, captain, coach, manager, contact, status, documents, tournament registrations."],
        ["Player", "Personal details, team, jersey number, position, medical information, statistics, achievements."],
        ["Historical Participation", "A player may participate in multiple tournaments over time while keeping historical records."],
    ], [2400, 6960]))

    body.append(p("9. Match, Event, and Live Score Model", style="Heading1"))
    body.append(p("Match events should use an event-sourced design. Persistent events allow replaying match history while Redis or live-state tables support low-latency operations."))
    body.append(image_paragraph("rIdImage3", "Match, Event, and Live Score Model", "Match event and live score model diagram", 3))
    body.append(table([
        ["Model", "Fields and Behavior"],
        ["Match", "Teams, venue, schedule, status, officials, score summary."],
        ["MatchEvent", "Match, timestamp, event type, team, player, value, metadata, created by; examples include goal, wicket, foul, timeout, point, card."],
        ["LiveScore", "Current score, timer, current period, match state, last updated."],
        ["ScoreSnapshot", "Point-in-time state for display, recovery, and audit."],
        ["Result and Standing", "Final outcome, leaderboard, standings, ranking, qualification status."],
    ], [2400, 6960]))

    body.append(p("10. Payment Model", style="Heading1"))
    body.append(table([
        ["Model", "Fields"],
        ["Payment", "Order ID, transaction ID, gateway, amount, currency, status, method, paidAt."],
        ["Refund", "Payment, amount, reason, status, processed by."],
        ["Invoice and Receipt", "Immutable completed-payment records for billing, reporting, and downloads."],
    ], [2400, 6960]))

    body.append(p("11. Notification Model", style="Heading1"))
    body.append(p("Notification records should store channel, recipient, subject, body, status, scheduled time, sent time, retry count, and template reference. Templates should be stored separately with variables."))

    body.append(p("12. Audit Model", style="Heading1"))
    body.append(table([
        ["Audit Field", "Purpose"],
        ["User, Module, Entity, Entity ID", "Identify who performed the action and what record was affected."],
        ["Action", "Create, update, delete, publish, approve, refund, permission change, score correction, and other critical operations."],
        ["Previous Data and New Data", "JSON before/after payloads for traceability."],
        ["IP Address, Device, Timestamp", "Security and investigation metadata."],
        ["Immutability", "Audit records must never be modified."],
    ], [2600, 6760]))

    body.append(p("13. Indexing Strategy", style="Heading1"))
    body.append(table([
        ["Index Type", "Examples"],
        ["Search Indexes", "Tournament name, user email, team name, player name."],
        ["Status Indexes", "Match status, registration status, payment status, live match flag."],
        ["Date Indexes", "Created date, payment date, match schedule date."],
        ["Composite Indexes", "Tournament + status, match + venue, payment + date."],
        ["Reporting Support", "Add indexes and summary tables where reporting load requires it."],
    ], [2400, 6960]))

    body.append(p("14. Soft Delete Strategy", style="Heading1"))
    body.append(p("Business records should not be physically deleted. Use deletedAt to mark records inactive. Queries should exclude soft-deleted records by default while allowing administrators to restore records where appropriate."))

    body.append(p("15. Migration Strategy", style="Heading1"))
    body.append(table([
        ["Migration Guideline", "Requirement"],
        ["Tooling", "Use Prisma Migrate."],
        ["Change Size", "Prefer small, incremental migrations."],
        ["Compatibility", "Favor backward-compatible changes and documented rollback procedures."],
        ["Seed Timing", "Seed data after initial migration and keep seeds repeatable."],
    ], [2400, 6960]))

    body.append(p("16. Seed Data", style="Heading1"))
    body.append(p("Provide seed scripts for roles, permissions, sports, tournament types, venue types, demo organizations, demo users, sample tournaments, sample teams, and sample players. Seeds should allow developers to run the application immediately after setup."))

    body.append(p("17. Reporting and Performance", style="Heading1"))
    body.append(p("The schema should support revenue by tournament, participation by sport, venue utilization, match completion rates, team rankings, and player performance. Optimize heavy reporting separately from transactional workloads."))
    body.append(image_paragraph("rIdImage4", "Database Lifecycle, Indexing, and Reporting", "Database lifecycle indexing and reporting diagram", 4))
    body.extend(bullets([
        "Use connection pooling, proper indexing, query pagination, and cursor-based pagination for large datasets.",
        "Use materialized views where appropriate.",
        "Use Redis caching for frequently accessed live data.",
        "Avoid excessive joins by using indexes and summary tables where necessary.",
    ]))

    body.append(p("18. Prisma Organization", style="Heading1"))
    body.append(table([
        ["Prisma Section", "Models"],
        ["Identity", "User, Role, Permission, UserRole, RolePermission, Session, RefreshToken, PasswordReset, AuditLog."],
        ["Organization", "Organization, settings, subscription plan, branding."],
        ["Tournament and Registration", "Tournament, sport, venue, registration, team, player, fixtures."],
        ["Match", "Match, period, event, commentary, official, live score, snapshot, correction, result."],
        ["Payment and Notification", "Payment, refund, invoice, receipt, notification, template, queue."],
        ["CMS, Reporting, Settings", "Pages, gallery, sponsors, blogs, FAQs, reports, schedules, platform settings."],
    ], [2400, 6960]))

    body.append(p("19. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Use UUIDs for primary keys.",
        "Define explicit foreign key relationships.",
        "Use enums for fixed-value fields where appropriate.",
        "Model many-to-many relationships through junction tables.",
        "Include audit fields and soft-delete support in business entities.",
        "Generate Prisma models, migrations, and seed scripts.",
        "Add indexes for search, reporting, and live match performance.",
        "Design the schema to support future multi-tenant SaaS deployment without major refactoring.",
        "Ensure historical records such as payments, results, match events, and audit logs are immutable once finalized.",
    ]))
    body.append(rich_callout("Phase 9 Completion Criteria", [
        "Phase 9 is complete when the database objective, design principles, schema domains, core relationships, RBAC model, tournament/team/player models, match/event/live score model, payment and notification models, audit strategy, indexes, soft deletes, migrations, seed data, reporting support, performance optimization, Prisma organization, and implementation rules are clear enough for production planning."
    ]))

    body.append(sect_pr())
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{NS_W}" xmlns:r="{NS_R}" xmlns:wp="{NS_WP}" xmlns:a="{NS_A}" xmlns:pic="{NS_PIC}">
  <w:body>
    {''.join(body)}
  </w:body>
</w:document>'''


def numbering_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="{NS_W}">
  <w:abstractNum w:abstractNumId="1">
    <w:multiLevelType w:val="hybridMultilevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
      <w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>'''


def content_types_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''


def root_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''


def document_rels_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
  <Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rIdFontTable" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase9_data_domain_map.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase9_rbac_data_model.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase9_match_event_live_model.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase9_database_lifecycle.png"/>
</Relationships>'''


def settings_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="{NS_W}">
  <w:updateFields w:val="true"/>
  <w:defaultTabStop w:val="720"/>
  <w:compat/>
</w:settings>'''


def font_table_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="{NS_W}">
  <w:font w:name="Times New Roman"><w:family w:val="roman"/><w:pitch w:val="variable"/></w:font>
  <w:font w:name="Symbol"><w:family w:val="roman"/><w:pitch w:val="variable"/></w:font>
</w:fonts>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Phase 9 Database Architecture and Prisma Schema Design</dc:title>
  <dc:subject>Enterprise PostgreSQL and Prisma data model for identity, tournaments, live scores, payments, CMS, reports, audit logs, indexes, migrations, and seeds</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def app_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <Company>Brillaris</Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>1.0</AppVersion>
</Properties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/phase9_data_domain_map.png": ASSET_DIR / "phase9_data_domain_map.png",
        "word/media/phase9_rbac_data_model.png": ASSET_DIR / "phase9_rbac_data_model.png",
        "word/media/phase9_match_event_live_model.png": ASSET_DIR / "phase9_match_event_live_model.png",
        "word/media/phase9_database_lifecycle.png": ASSET_DIR / "phase9_database_lifecycle.png",
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
