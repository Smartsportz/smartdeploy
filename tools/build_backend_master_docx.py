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


OUT = Path("docs/Smart_Sportz_Backend_Master_Logic_Workflows_Specification.docx")
ASSET_DIR = Path("docs/assets")


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def document_xml() -> str:
    body: list[str] = []

    body.append(p("SMART SPORTZ - BACKEND MASTER SPECIFICATION", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Backend Logic, API Workflows, Data Architecture and Production Blueprint", style="Subtitle"))
    body.append(p("Consolidated from Phases 1-11", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Backend Master Logic and Workflows Specification"],
        ["Project", "Smart Sportz"],
        ["Source Phases", "Phase 1 Foundation, Phase 3 Public Website, Phase 4 Registration and Payment, Phase 5 Super Admin Portal, Phase 6 Management Portal, Phase 7 Live Score, Phase 8 Backend Architecture, Phase 9 Database, Phase 10 Frontend Integration, Phase 11 DevOps"],
        ["Backend Scope", "Node.js, Express, TypeScript, Clean Architecture, REST APIs, Socket.IO, authentication, RBAC, PostgreSQL, Prisma, Redis, storage, Razorpay, notifications, background jobs, logging, audit, security, OpenAPI, testing, Docker, and production operations"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Backend Master Intent", [
        "This document consolidates backend-facing requirements from all Smart Sportz phase documents into one implementation-ready engineering specification.",
        "It defines backend modules, request flow, service logic, API boundaries, real-time workflows, persistence rules, integrations, background jobs, security controls, testing expectations, and production behavior."
    ]))

    body.append(p("1. Backend Product Scope", style="Heading1"))
    body.append(p("The Smart Sportz backend is a modular enterprise platform that powers public discovery, registration, payments, Super Admin operations, Management User operations, live score updates, CMS content, notifications, reporting, audit trails, and production observability."))
    body.extend(bullets([
        "Expose versioned REST APIs under a future-ready namespace such as /api/v1.",
        "Support Socket.IO for real-time live scoring, tournament feeds, and notifications.",
        "Enforce authentication, RBAC, scoped permissions, validation, rate limiting, and audit logging on every sensitive action.",
        "Use PostgreSQL and Prisma for persistent data, Redis for live state, queues, cache, and Socket.IO scaling, and cloud storage for uploaded assets.",
        "Remain stateless at the application layer so Dockerized backend instances can scale horizontally.",
    ]))

    body.append(p("2. Phase-to-Backend Reference Map", style="Heading1"))
    body.append(table([
        ["Phase", "Backend Meaning"],
        ["1 Foundation", "Defines core modules, Node.js, Express, TypeScript, JWT, refresh tokens, Zod, Multer, Socket.IO, OpenAPI, Winston, Redis, and Node Cron."],
        ["3 Public Website", "Requires public APIs for tournaments, live matches, fixtures, results, leaderboards, CMS content, search, and SEO content feeds."],
        ["4 Registration and Payment", "Requires registration APIs, document upload, Razorpay order creation, webhook verification, payment statuses, refunds, invoices, receipts, notifications, and audit logs."],
        ["5 Super Admin", "Requires high-privilege admin APIs for users, roles, permissions, tournaments, master data, finance, CMS, reports, audit logs, settings, and integrations."],
        ["6 Management Portal", "Requires scoped operations APIs for assigned tournaments, matches, players, verification, live scoring, announcements, results, documents, reports, and activity logs."],
        ["7 Live Score", "Requires event-driven scoring logic, sport adapters, match lifecycle validation, Redis live state, Socket.IO broadcasting, score corrections, statistics, and replayable history."],
        ["8 Backend Architecture", "Defines Clean Architecture, feature modules, controllers, services, repositories, middleware, validation, Socket.IO gateway, jobs, logging, security, and OpenAPI documentation."],
        ["9 Database", "Defines PostgreSQL and Prisma models for identity, organization, tournament, registration, teams, players, matches, live scores, payments, notifications, CMS, reports, settings, and audit."],
        ["10 Frontend Architecture", "Defines typed API contracts, TanStack Query integration, Socket.IO client events, page states, and frontend expectations for backend error responses."],
        ["11 DevOps", "Defines Docker, Nginx routing, health checks, environment separation, secrets, monitoring, logs, alerts, backups, recovery, and horizontal scaling."],
    ], [2200, 7160]))

    body.append(p("3. Backend System Topology", style="Heading1"))
    body.append(p("The backend topology separates HTTP APIs, middleware, feature services, repositories, data stores, live Socket.IO channels, background jobs, external providers, and operations hooks."))
    body.append(image_paragraph("rIdImage1", "Smart Sportz Backend System Topology", "Smart Sportz backend system topology diagram", 1))

    body.append(p("4. Backend Technology Stack", style="Heading1"))
    body.append(table([
        ["Layer", "Technology and Responsibility"],
        ["Runtime", "Node.js LTS with TypeScript."],
        ["HTTP Framework", "Express.js with modular routers, middleware, controllers, and error handling."],
        ["Database", "PostgreSQL with Prisma ORM, migrations, seed data, transactions, indexes, and soft-delete support."],
        ["Cache and Live State", "Redis for active live scores, cache, queues, Socket.IO adapter, and rate-limited transient state."],
        ["Real Time", "Socket.IO server with room subscriptions for matches, tournaments, and notifications."],
        ["Validation", "Zod schemas for params, query, body, file metadata, webhook payloads, and service DTOs."],
        ["Files", "Multer or streaming upload pipeline to cloud storage with signed URLs for private assets."],
        ["Payments", "Razorpay order creation, checkout confirmation, webhook verification, refunds, receipts, and invoices."],
        ["Notifications", "Email, SMS, WhatsApp, push, templates, queue, retries, and delivery logs."],
        ["Docs and Logs", "OpenAPI or Swagger documentation, Winston-style structured logs, correlation IDs, and audit logs."],
    ], [2400, 6960]))

    body.append(p("5. Project Structure", style="Heading1"))
    body.append(table([
        ["Folder", "Responsibility"],
        ["src/app", "Express app bootstrap, middleware wiring, lifecycle setup, global error handler."],
        ["src/config", "Environment, database, cache, storage, payment, notification, security, and feature flags."],
        ["src/modules", "Feature modules such as auth, users, RBAC, tournaments, registration, payments, live-score, CMS, reports, notifications."],
        ["src/modules/*/controllers", "HTTP request mapping, response formatting, status codes, and OpenAPI metadata."],
        ["src/modules/*/services", "Business logic, transactions, workflows, domain events, authorization coordination."],
        ["src/modules/*/repositories", "Prisma queries, scoped data access, pagination, search, indexes, and persistence rules."],
        ["src/middleware", "Auth, RBAC, validation, rate limiting, request context, correlation ID, error handling."],
        ["src/sockets", "Socket.IO gateway, room registry, event contracts, auth handshake, publish helpers."],
        ["src/jobs", "Queues, workers, scheduled tasks, retries, reports, notifications, cleanup, maintenance tasks."],
        ["src/shared", "Errors, DTOs, constants, utils, logger, audit helper, response wrapper, test utilities."],
    ], [2400, 6960]))

    body.append(p("6. Clean Architecture Request Flow", style="Heading1"))
    body.append(p("Every backend request should pass through a consistent chain: route, middleware, validation, controller, service, repository, data store, audit log, and response."))
    body.append(image_paragraph("rIdImage2", "Clean Architecture Request Flow", "Clean architecture request flow diagram", 2))
    body.append(table([
        ["Layer", "Rule"],
        ["Middleware", "Authenticate user, attach request context, enforce rate limits, apply RBAC or route-level guards."],
        ["Validation", "Validate body, query, params, files, and webhook signatures before service logic runs."],
        ["Controller", "Stay thin. Map HTTP inputs to service DTOs and map service results to response shape."],
        ["Service", "Own business rules, transactions, authorization coordination, domain events, and cross-module workflows."],
        ["Repository", "Own Prisma access, scoped queries, filters, pagination, indexes, and persistence semantics."],
        ["Audit and Logging", "Log important actions, errors, state changes, payment events, score corrections, and security events."],
    ], [2300, 7060]))

    body.append(p("7. Core Feature Modules", style="Heading1"))
    body.append(table([
        ["Module", "Backend Responsibilities"],
        ["Auth", "Login, logout, refresh token rotation, password reset, OTP/verification, remember me, session policy."],
        ["Users and RBAC", "Users, roles, permissions, user-role assignment, role-permission mapping, scoped access, revocation."],
        ["Organizations", "Future tenant-ready organizations, settings, branding, subscription plan, scoped ownership."],
        ["Tournaments", "Tournament CRUD, categories, rules, stages, formats, fixtures, announcements, sponsors, CMS links."],
        ["Sports and Venues", "Sports, sport rules, venues, courts, areas, equipment, availability, assigned access."],
        ["Registration", "Team/player registration, documents, waitlist, approval, rejection, coupons, eligibility, audit."],
        ["Payments", "Razorpay orders, payment statuses, webhook verification, refunds, receipts, invoices, finance reports."],
        ["Teams and Players", "Team roster, player profile, documents, medical data, achievements, statistics, verification."],
        ["Matches and Live Score", "Fixtures, matches, lifecycle, events, commentary, live state, score corrections, statistics, leaderboards."],
        ["CMS", "Pages, homepage sections, sponsors, gallery, blogs, FAQs, public content publishing."],
        ["Notifications", "Templates, queue, delivery status, retries, channels, announcements, operational alerts."],
        ["Reports and Audit", "Revenue, participation, venue utilization, match completion, exports, audit search, security investigation."],
    ], [2300, 7060]))

    body.append(p("8. Authentication, RBAC, and Scope Enforcement", style="Heading1"))
    body.append(p("Backend authorization must be enforced independently from frontend route guards. Every API and Socket.IO action must validate identity, permission, and resource scope."))
    body.append(image_paragraph("rIdImage3", "Authentication, RBAC, and Scope Enforcement", "Authentication RBAC and scope enforcement diagram", 3))
    body.extend(bullets([
        "JWT access tokens should be short-lived and paired with refresh token rotation.",
        "Permissions should be granular action keys such as tournament.create, live.update, payment.refund, report.export, and cms.publish.",
        "Management users must be restricted to assigned tournaments, assigned venues, assigned sports, granted modules, and granted actions.",
        "Revoked permissions must affect new API requests and Socket.IO actions immediately where technically possible.",
        "Sensitive actions must record audit logs with user, module, entity, entity ID, action, previous data, new data, IP, device, and timestamp.",
    ]))

    body.append(p("9. REST API Design", style="Heading1"))
    body.append(table([
        ["API Family", "Example Responsibilities"],
        ["Auth APIs", "Login, refresh, logout, forgot password, OTP, reset password, current profile."],
        ["Public APIs", "Tournaments, sports, fixtures, live scores, results, leaderboards, gallery, sponsors, blogs, FAQs."],
        ["Registration APIs", "Create registration, upload documents, validate coupon, status tracking, approval workflow."],
        ["Payment APIs", "Create order, confirm status, webhook, refund, invoice, receipt, payment reports."],
        ["Admin APIs", "Users, roles, permissions, tournaments, master data, CMS, finance, reports, audit, settings."],
        ["Management APIs", "Assigned tournaments, matches, verification, live score commands, announcements, results, documents, reports."],
        ["Live Score APIs", "Match lifecycle, event timeline, score snapshots, corrections, statistics, replay, leaderboard refresh."],
        ["File APIs", "Upload policy, signed URLs, private file access, image/document validation, delete or archive rules."],
    ], [2300, 7060]))

    body.append(p("10. API Contract Rules", style="Heading1"))
    body.extend(bullets([
        "Use consistent response envelopes for success, validation failure, authorization failure, not found, conflict, and server errors.",
        "Use cursor or page-based pagination consistently with search, filters, sort, and column-specific query options.",
        "Use idempotency keys for webhook handling, payment confirmation, and retryable mutation workflows where duplicates are risky.",
        "Document every endpoint with OpenAPI purpose, auth requirement, permission key, request schema, response schema, error codes, and example payload.",
        "Keep frontend-facing error messages user-safe while logging technical details with correlation IDs.",
    ]))

    body.append(p("11. Registration, Payment, and Approval Workflow", style="Heading1"))
    body.append(p("The backend must protect registration and payment correctness through validation, transaction boundaries, secure webhook verification, idempotency, audit logs, and notifications."))
    body.append(image_paragraph("rIdImage4", "Registration, Payment, and Approval Backend Workflow", "Registration payment and approval backend workflow diagram", 4))
    body.append(table([
        ["Workflow Step", "Backend Logic"],
        ["Registration Create", "Validate tournament status, category, eligibility, capacity, registration dates, required fields, and team/player data."],
        ["Document Upload", "Validate type and size, store in cloud storage, attach to registration, set verification state."],
        ["Coupon Validation", "Check tournament scope, usage limit, expiry, allowed category, and discounted amount."],
        ["Razorpay Order", "Create order with exact payable amount, store transaction, set payment status Pending or Processing."],
        ["Webhook Verification", "Verify signature, enforce idempotency, update status only from trusted webhook event, record audit."],
        ["Approval", "Approve, reject, waitlist, request verification, or trigger refund according to role permission and tournament rule."],
        ["Receipts and Invoices", "Generate immutable receipt and invoice records after successful payment and approval rules."],
        ["Notifications", "Queue email, SMS, WhatsApp, push, and in-app updates for key registration and payment states."],
    ], [2300, 7060]))

    body.append(p("12. Live Score Event Processing", style="Heading1"))
    body.append(p("Live scoring should use an event-driven backend model. Stored match events are the source of truth; Redis stores active state for fast display; Socket.IO broadcasts updates to public and operational clients."))
    body.append(image_paragraph("rIdImage5", "Live Score Event Processing Workflow", "Live score event processing workflow diagram", 5))
    body.append(table([
        ["Area", "Backend Requirement"],
        ["Match Lifecycle", "Scheduled, check-in, ready, live, paused, delayed, interrupted, completed, cancelled transitions with validation and audit."],
        ["Sport Adapter", "Sport-specific validation for cricket, football, basketball, volleyball, tennis, badminton, chess, athletics, and future sports."],
        ["Event Store", "Persist MatchEvent records with timestamp, type, team, player, value, metadata, createdBy, and correction lineage."],
        ["Redis State", "Store current score, timer, period, active match state, recent events, and public snapshot."],
        ["Socket.IO", "Authenticate socket handshake, join match/tournament rooms, broadcast score, timeline, commentary, standings, and notifications."],
        ["Corrections", "Require permission and reason, preserve before/after state, recalculate snapshots, notify viewers, audit action."],
        ["Reports", "Update results, standings, leaderboards, player/team statistics, and match analytics after events or finalization."],
    ], [2300, 7060]))

    body.append(p("13. Database and Prisma Rules", style="Heading1"))
    body.append(table([
        ["Rule", "Requirement"],
        ["Primary Keys", "Use UUID primary keys across all models."],
        ["Audit Fields", "Use createdAt, updatedAt, deletedAt, createdBy, and updatedBy where appropriate."],
        ["Soft Delete", "Use deletedAt for business entities and exclude deleted records by default."],
        ["Relationships", "Define explicit foreign keys and many-to-many junction tables such as UserRole and RolePermission."],
        ["Indexes", "Add indexes for search, status, dates, tournament plus status, payment plus date, match plus venue, and live match queries."],
        ["Transactions", "Use transactions for registration plus payment preparation, approval changes, refunds, score finalization, and multi-step updates."],
        ["Immutability", "Keep payments, results, match events, receipts, invoices, and audit logs immutable after finalization."],
        ["Seeds", "Seed roles, permissions, sports, tournament types, venue types, demo organizations, users, tournaments, teams, and players."],
    ], [2300, 7060]))

    body.append(p("14. Redis, Cache, Queues, and Jobs", style="Heading1"))
    body.append(p("Redis should support active live score state, cache, queues, Socket.IO scaling, and short-lived operational data. Background workers should handle non-blocking workflows."))
    body.append(image_paragraph("rIdImage6", "Jobs, Notifications, Logging, and Operations Flow", "Jobs notifications logging and operations flow diagram", 6))
    body.extend(bullets([
        "Use Redis for current live match state, timers, scoreboard snapshots, notification queues, report jobs, and optional session-related state.",
        "Use background jobs for notifications, reports, exports, receipt/invoice generation, cleanup, cache warming, and scheduled maintenance tasks.",
        "Use retry policies, dead-letter handling or failure logs, delivery status tracking, and idempotent job handlers.",
        "Expose health signals for API, database, Redis, Socket.IO, queues, storage, payment provider, and notification providers.",
    ]))

    body.append(p("15. File Storage and Document Logic", style="Heading1"))
    body.append(table([
        ["Asset Type", "Backend Rule"],
        ["Team Logos and Player Photos", "Validate image type and size, store in public or controlled bucket path, return optimized URL where appropriate."],
        ["Tournament Banners and Gallery", "Support CMS upload, metadata, ordering, visibility, and lifecycle rules."],
        ["Verification Documents", "Private storage with signed URL access, document status, reviewer metadata, and audit trail."],
        ["Receipts, Invoices, Certificates, Reports", "Generated server-side, stored immutably or versioned, linked to payment or tournament records."],
        ["Security", "Never expose private bucket paths directly; use signed URLs and permission checks."],
    ], [2300, 7060]))

    body.append(p("16. Notification Service", style="Heading1"))
    body.append(table([
        ["Channel", "Backend Logic"],
        ["Email", "Template rendering, SMTP/provider config, delivery status, retry, unsubscribe where applicable."],
        ["SMS", "Short status updates for registration, payment, match schedule, and urgent alerts."],
        ["WhatsApp", "Operational and registration updates where configured and approved."],
        ["Push and In-App", "Portal notifications, live match alerts, admin alerts, and read/unread state."],
        ["Templates", "Variables, localization-ready structure, preview, versioning, active/inactive status."],
        ["Queue", "Asynchronous delivery, retry count, scheduledAt, sentAt, failure reason, delivery logs."],
    ], [2300, 7060]))

    body.append(p("17. Logging, Audit, Monitoring, and Recovery", style="Heading1"))
    body.extend(bullets([
        "Use structured logs for application, access, error, authentication, payment, live score, background job, and security events.",
        "Use correlation IDs to trace requests across APIs, jobs, Socket.IO events, webhooks, and provider integrations.",
        "Monitor latency, error rates, CPU, memory, disk, database connections, Redis health, Socket.IO connections, queue length, webhook failures, SSL expiry, and backups.",
        "Daily backups, point-in-time recovery where supported, backup verification, migration validation, and documented recovery procedures are backend responsibilities.",
        "Support rollback-aware releases, migration notes, queue draining before shutdown, cache warming after deploy, and future read-only mode.",
    ]))

    body.append(p("18. Security Controls", style="Heading1"))
    body.append(table([
        ["Control", "Backend Requirement"],
        ["Authentication", "JWT, refresh tokens, token rotation, session policy, password policy, OTP/reset protection."],
        ["Authorization", "Granular RBAC, scoped permissions, backend enforcement, Socket.IO action enforcement."],
        ["Input Protection", "Zod validation, file validation, request size limits, SQL injection protection through Prisma, XSS-safe output where backend controls content."],
        ["CSRF and CORS", "Apply suitable CORS policy and CSRF protection strategy for cookie-based surfaces if used."],
        ["Secrets", "Never hard-code secrets; use environment-specific secret stores and periodic rotation."],
        ["Rate Limiting", "Protect login, OTP, public APIs, payment endpoints, upload endpoints, and high-cost searches."],
        ["Dependency and Container Security", "Run dependency scanning and container image scanning in CI/CD."],
        ["Audit Review", "Review admin changes, permission changes, payment actions, score corrections, failed auth events, and API keys."],
    ], [2300, 7060]))

    body.append(p("19. Testing Strategy", style="Heading1"))
    body.extend(bullets([
        "Unit test services, validators, repositories, permissions, sport adapters, payment calculations, and notification template rendering.",
        "Integration test auth, RBAC, registration, payments, webhooks, refunds, live score commands, CMS publishing, reports, and file uploads.",
        "Socket.IO tests should verify auth handshake, room joins, match event broadcasts, reconnect behavior, and permission failures.",
        "Database tests should verify transactions, soft deletes, indexes, migrations, seeds, and immutable historical records.",
        "End-to-end API tests should cover public discovery, registration to payment to approval, management score update to public live display, and admin permission denial.",
    ]))

    body.append(p("20. Production and Deployment Rules", style="Heading1"))
    body.extend(bullets([
        "Provide production-ready backend Dockerfile and local Docker Compose services for backend, frontend, PostgreSQL, Redis, and Nginx.",
        "Expose health check endpoints for API, database connectivity, Redis, queues, and Socket.IO readiness.",
        "Separate development, testing, staging, and production configuration, databases, buckets, keys, logs, and secrets.",
        "Support zero-downtime style deployments with stateless backend instances, graceful shutdown, queue draining, and migration validation.",
        "Staging should mirror production as closely as possible before manual production approval.",
    ]))

    body.append(p("21. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Use Node.js, Express, TypeScript, PostgreSQL, Prisma, Redis, Socket.IO, Zod, OpenAPI, and structured logging.",
        "Implement Clean Architecture with controllers, services, repositories, DTOs, validation schemas, middleware, and shared error handling.",
        "Keep business rules in services and never in controllers or route files.",
        "Every API must define authentication, permission key, validation schema, response schema, error codes, and audit behavior where relevant.",
        "Use transactions for multi-step writes and idempotency for payment webhooks and retry-prone operations.",
        "Implement backend RBAC and scope checks even when the frontend already hides a feature.",
        "Use event-driven live scoring with replayable MatchEvent history and Redis live state.",
        "No mock APIs, TODO comments, or placeholder business logic in production code generation.",
    ]))
    body.append(rich_callout("Backend Master Completion Criteria", [
        "This backend master document is complete when it gives the implementation team a single source of truth for backend modules, Clean Architecture, REST APIs, Socket.IO workflows, authentication, RBAC, registration, payments, live score events, Prisma data rules, Redis and jobs, file storage, notifications, audit logs, security, testing, monitoring, and production deployment behavior."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/backend_master_topology.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/backend_clean_architecture_flow.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/backend_auth_rbac_flow.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/backend_registration_payment_flow.png"/>
  <Relationship Id="rIdImage5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/backend_live_score_event_flow.png"/>
  <Relationship Id="rIdImage6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/backend_jobs_observability_flow.png"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Backend Master Logic and Workflows Specification</dc:title>
  <dc:subject>Consolidated backend specification covering architecture, REST APIs, Socket.IO, authentication, RBAC, registration, payments, live scoring, Prisma, Redis, jobs, storage, notifications, audit, security, testing, monitoring, and production deployment</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/backend_master_topology.png": ASSET_DIR / "backend_master_topology.png",
        "word/media/backend_clean_architecture_flow.png": ASSET_DIR / "backend_clean_architecture_flow.png",
        "word/media/backend_auth_rbac_flow.png": ASSET_DIR / "backend_auth_rbac_flow.png",
        "word/media/backend_registration_payment_flow.png": ASSET_DIR / "backend_registration_payment_flow.png",
        "word/media/backend_live_score_event_flow.png": ASSET_DIR / "backend_live_score_event_flow.png",
        "word/media/backend_jobs_observability_flow.png": ASSET_DIR / "backend_jobs_observability_flow.png",
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
