from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_8_Backend_Architecture_API_Design.docx")
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

    body.append(p("PHASE 8 - BACKEND ARCHITECTURE & API DESIGN", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Enterprise Backend Architecture", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 8 Backend Architecture and API Design"],
        ["Project", "Smart Sportz"],
        ["Focus", "Node.js, Express, TypeScript, Clean Architecture, REST APIs, Socket.IO, RBAC, PostgreSQL, Prisma, Redis, storage, payments, notifications, jobs, logging, security, and OpenAPI documentation"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved Phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 8 Intent", [
        "This document defines the Smart Sportz backend architecture and API design. It converts the backend prompt into a structured engineering specification for a modular, scalable, secure, production-ready Node.js, Express, TypeScript backend.",
        "The backend must expose versioned REST APIs, support Socket.IO live scoring, enforce Azure-style RBAC, use PostgreSQL with Prisma, cache live data in Redis, and remain ready for Docker deployment and horizontal scaling."
    ]))

    body.append(p("1. Module Objective", style="Heading1"))
    body.append(p("Build a production-ready backend using Node.js, Express, and TypeScript following Clean Architecture principles."))
    body.extend(bullets([
        "Be modular, scalable, and feature-isolated.",
        "Expose REST APIs with future versioning such as /api/v1.",
        "Support Socket.IO for live scoring and match updates.",
        "Secure every endpoint with authentication, authorization, validation, and audit logging.",
        "Use PostgreSQL with Prisma ORM and Redis for active live data.",
        "Be ready for Docker deployment and horizontal scaling.",
    ]))

    body.append(p("2. Backend Architecture Topology", style="Heading1"))
    body.append(p("The backend topology separates HTTP APIs, business services, repositories, data stores, cache, Socket.IO, external providers, and background jobs."))
    body.append(image_paragraph("rIdImage1", "Backend Architecture Topology", "Backend architecture topology diagram", 1))

    body.append(p("3. Project Structure", style="Heading1"))
    body.append(table([
        ["Folder", "Purpose"],
        ["src/app", "Express application bootstrap, shared app setup, and lifecycle wiring."],
        ["src/config", "Environment, database, cache, storage, payment, notification, and security configuration."],
        ["src/routes", "Versioned route definitions grouped by module."],
        ["src/controllers", "Thin HTTP adapters that call services and format responses."],
        ["src/services", "Business rules, orchestration, transactions, domain decisions."],
        ["src/repositories", "Prisma data access and query isolation."],
        ["src/middleware", "Authentication, authorization, validation, rate limiting, errors, logging."],
        ["src/validators", "Zod schemas, DTO validation, custom sport rules."],
        ["src/sockets", "Socket.IO namespaces, rooms, events, connection lifecycle."],
        ["src/events and jobs", "Domain events, background jobs, retries, schedules, notifications."],
        ["src/payments/uploads/reports/cms/analytics/integrations", "Dedicated infrastructure and business capability areas."],
        ["prisma, tests, docker", "Schema, migrations, test suites, Docker deployment assets."],
    ], [2600, 6760]))

    body.append(p("4. Feature Modules", style="Heading1"))
    body.append(p("Each business capability should be isolated to reduce coupling. Every module should include controller, service, repository, validator, routes, DTOs, and tests."))
    body.append(table([
        ["Module Group", "Modules"],
        ["Identity and Access", "Authentication, users, roles, permissions, organizations."],
        ["Tournament Operations", "Sports, venues, tournaments, registrations, teams, players, fixtures, matches, live scores, results."],
        ["Commerce", "Payments, coupons, receipts, refunds where applicable."],
        ["Communication", "Notifications, templates, email, SMS, WhatsApp, future push."],
        ["Content and Reporting", "Reports, CMS, gallery, sponsors, analytics."],
        ["Platform", "Audit logs, settings, uploads, integrations, jobs."],
    ], [2400, 6960]))

    body.append(p("5. Clean Architecture Flow", style="Heading1"))
    body.append(p("Business rules must stay inside the Service Layer. Controllers should stay thin and repositories should isolate persistence details."))
    body.append(image_paragraph("rIdImage2", "Clean Architecture Request Flow", "Clean Architecture request flow diagram", 2))

    body.append(p("6. Authentication", style="Heading1"))
    body.append(table([
        ["Capability", "Specification"],
        ["Current Auth", "Email and password login, JWT access tokens, refresh tokens, secure logout, password reset, email verification."],
        ["Future Ready", "OTP login, Google login, Microsoft login."],
        ["Token Handling", "Short-lived access tokens, refresh rotation, logout invalidation, secure cookie/header strategy as appropriate."],
        ["Password Security", "bcrypt hashing, password policy, reset token expiry, audit trail for sensitive events."],
    ], [2400, 6960]))

    body.append(p("7. Authorization and RBAC", style="Heading1"))
    body.append(p("Every request passes through authentication middleware, permission middleware, and resource ownership checks where applicable. Permissions must be configurable from the Super Admin portal."))
    body.append(image_paragraph("rIdImage3", "Authentication and RBAC Pipeline", "Authentication and RBAC pipeline diagram", 3))

    body.append(p("8. REST API Design", style="Heading1"))
    body.append(table([
        ["Area", "Example Endpoints"],
        ["Authentication", "POST /api/v1/auth/login, logout, refresh, forgot-password."],
        ["Users", "GET, POST /api/v1/users; PUT, DELETE /api/v1/users/:id."],
        ["Tournaments", "GET, POST /api/v1/tournaments; GET, PUT, DELETE /api/v1/tournaments/:id."],
        ["Matches", "GET, POST /api/v1/matches; PUT /api/v1/matches/:id; POST /api/v1/matches/:id/start; POST /api/v1/matches/:id/end."],
        ["Live Scores", "GET /api/v1/live/matches; POST /api/v1/live/events; POST /api/v1/live/undo; GET /api/v1/live/:matchId."],
        ["Payments", "POST /api/v1/payments/create-order; POST /api/v1/payments/webhook; GET /api/v1/payments/history."],
        ["Reports", "GET /api/v1/reports/tournaments, revenue, participants."],
    ], [2300, 7060]))

    body.append(p("9. Request Validation", style="Heading1"))
    body.append(p("Validate all incoming data using Zod. Requirements include type-safe schemas, consistent error responses, field-level validation, custom validators for sport-specific rules, and a strict never-trust-client-input posture."))

    body.append(p("10. Socket.IO Gateway", style="Heading1"))
    body.append(table([
        ["Socket Area", "Specification"],
        ["Namespaces", "/live, /admin, /management."],
        ["Rooms", "Tournament, match, venue."],
        ["Server Events", "MatchStarted, MatchPaused, MatchResumed, ScoreUpdated, EventAdded, MatchCompleted."],
        ["Client Events", "JoinMatch, LeaveMatch, SubscribeTournament."],
        ["Scaling", "Design for horizontal Socket.IO gateway scaling and state resync after reconnect."],
    ], [2400, 6960]))

    body.append(p("11. Event Processing", style="Heading1"))
    body.append(p("Every live action generates an event, validates the command, writes to the database, updates Redis, and broadcasts changed data to the correct Socket.IO rooms."))
    body.append(image_paragraph("rIdImage4", "Event Processing and Integration Pipeline", "Event processing and integration pipeline diagram", 4))

    body.append(p("12. Redis Caching", style="Heading1"))
    body.append(table([
        ["Cache Area", "Policy"],
        ["Live Scores", "Write-through cache and immediate refresh after events."],
        ["Match State", "Active state held in Redis for low-latency live clients."],
        ["Leaderboards", "Invalidate or recalculate after completed matches and scoring events."],
        ["Tournament Data", "Time-based expiration for frequently accessed non-live data."],
    ], [2400, 6960]))

    body.append(p("13. File Storage", style="Heading1"))
    body.append(p("Use Cloudinary or AWS S3 for team logos, player photos, tournament banners, gallery media, certificates, and documents. Generate secure URLs and support file deletion."))

    body.append(p("14. Payment Service", style="Heading1"))
    body.append(table([
        ["Payment Step", "Requirement"],
        ["Create Order", "Create Razorpay order from trusted backend amount and registration context."],
        ["Redirect / Client Pay", "Client completes payment, but client payment status is never trusted."],
        ["Webhook", "Receive webhook and verify Razorpay signature."],
        ["Post-Payment", "Update registration, generate receipt, and send notifications."],
    ], [2400, 6960]))

    body.append(p("15. Notification Service and Background Jobs", style="Heading1"))
    body.append(table([
        ["Area", "Specification"],
        ["Notification Channels", "Email, SMS, WhatsApp, future push."],
        ["Reliability", "Queue notifications for reliable delivery, retries, and failure tracking."],
        ["Scheduled Jobs", "Registration closing, tournament reminders, backup, report generation, notification retries, waitlist promotion."],
        ["Job Safety", "Design jobs to be idempotent and retry-safe."],
    ], [2400, 6960]))

    body.append(p("16. Error Handling", style="Heading1"))
    body.append(p("Implement a centralized error handler with structured responses that include success=false, a message, and field-level errors where relevant. Unexpected errors should be logged with correlation IDs for troubleshooting."))

    body.append(p("17. Logging and Audit", style="Heading1"))
    body.extend(bullets([
        "Use structured logging for requests, responses excluding sensitive data, authentication events, permission failures, payment events, live score changes, and system errors.",
        "Maintain immutable audit logs for critical actions.",
        "Use correlation IDs for request tracing across APIs, jobs, and integrations.",
    ]))

    body.append(p("18. Security", style="Heading1"))
    body.append(table([
        ["Security Control", "Requirement"],
        ["HTTP Protection", "Helmet, secure HTTP headers, CORS, CSRF protection where applicable."],
        ["Abuse Prevention", "Rate limiting and meaningful error handling without leaking internals."],
        ["Input and Data", "Input sanitization, Zod validation, Prisma SQL injection protection, XSS protection."],
        ["Secrets and Passwords", "bcrypt password hashing and encrypted sensitive configuration values."],
    ], [2400, 6960]))

    body.append(p("19. API Documentation", style="Heading1"))
    body.append(p("Generate OpenAPI/Swagger documentation. Each endpoint should define purpose, authentication requirement, request schema, response schema, error codes, and example payloads. Documentation should stay synchronized with implementation."))

    body.append(p("20. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Use TypeScript across the entire codebase.",
        "Follow Clean Architecture with clear separation of concerns.",
        "Keep controllers thin and place business logic in services.",
        "Use Prisma transactions for multi-step operations.",
        "Implement optimistic concurrency where appropriate.",
        "Provide unit tests for services and integration tests for APIs.",
        "Use dependency injection patterns where beneficial.",
        "Design modules so new sports, payment providers, or notification channels can be added with minimal changes.",
        "Ensure all endpoints enforce authentication, authorization, validation, and audit logging.",
    ]))
    body.append(rich_callout("Phase 8 Completion Criteria", [
        "Phase 8 is complete when the backend objective, project structure, feature modules, Clean Architecture flow, authentication, RBAC, REST APIs, validation, Socket.IO gateway, event processing, Redis caching, file storage, payment service, notifications, jobs, errors, logging, security, OpenAPI documentation, and implementation rules are clear enough for production planning."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase8_backend_topology.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase8_clean_architecture_flow.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase8_auth_rbac_pipeline.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase8_event_processing_pipeline.png"/>
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
  <dc:title>Smart Sportz - Phase 8 Backend Architecture and API Design</dc:title>
  <dc:subject>Enterprise backend architecture, Clean Architecture, REST APIs, RBAC, Socket.IO, Redis, Prisma, payments, jobs, logging, security, and OpenAPI specification</dc:subject>
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
        "word/media/phase8_backend_topology.png": ASSET_DIR / "phase8_backend_topology.png",
        "word/media/phase8_clean_architecture_flow.png": ASSET_DIR / "phase8_clean_architecture_flow.png",
        "word/media/phase8_auth_rbac_pipeline.png": ASSET_DIR / "phase8_auth_rbac_pipeline.png",
        "word/media/phase8_event_processing_pipeline.png": ASSET_DIR / "phase8_event_processing_pipeline.png",
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
