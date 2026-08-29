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


OUT = Path("docs/Smart_Sportz_Phase_11_DevOps_Deployment_CICD_Production_Infrastructure.docx")
ASSET_DIR = Path("docs/assets")


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def document_xml() -> str:
    body: list[str] = []

    body.append(p("PHASE 11 - DEVOPS, DEPLOYMENT, CI/CD & PRODUCTION INFRASTRUCTURE", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Production Infrastructure Blueprint", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 11 DevOps, Deployment, CI/CD and Production Infrastructure"],
        ["Project", "Smart Sportz"],
        ["Focus", "Environment strategy, Git workflow, CI/CD, Docker, Nginx, SSL, secrets, database operations, Redis, file storage, monitoring, logging, alerting, disaster recovery, scalability, security operations, release management, and maintenance"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved Phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 11 Intent", [
        "This document converts the infrastructure prompt into a production-grade DevOps blueprint for Smart Sportz.",
        "The platform must support automated deployments, zero-downtime releases, horizontal scaling, high availability, secure secrets, CI/CD, monitoring, alerting, backups, disaster recovery, and separated development, testing, staging, and production environments."
    ]))

    body.append(p("1. Module Objective", style="Heading1"))
    body.append(p("Design a production infrastructure that supports reliable tournament operations, live scoring, payment flows, public traffic, admin workflows, and management workflows across development, testing, staging, and production."))
    body.extend(bullets([
        "Automate deployments while keeping production releases controlled and rollback-ready.",
        "Use horizontal scaling and stateless service design wherever possible.",
        "Protect secrets, credentials, payment keys, database access, and production configuration.",
        "Monitor health, performance, errors, logs, backups, SSL, queues, webhooks, and real-time connections.",
    ]))

    body.append(p("2. Environment Strategy", style="Heading1"))
    body.append(p("Maintain independent environments with separate configuration, database, storage bucket, API keys, credentials, and logging. Production credentials must never be shared with non-production environments."))
    body.append(image_paragraph("rIdImage1", "Environment Strategy and Promotion Flow", "Environment strategy and promotion flow diagram", 1))
    body.append(table([
        ["Environment", "Purpose"],
        ["Development", "Local and shared development with isolated test credentials and sample data."],
        ["Testing", "Automated CI validation, disposable data, repeatable test execution."],
        ["Staging", "Production-like deployment for release verification and smoke tests."],
        ["Production", "Live environment with protected secrets, backups, monitoring, alerts, and strict access control."],
    ], [2400, 6960]))

    body.append(p("3. Repository Strategy", style="Heading1"))
    body.append(table([
        ["Branch", "Purpose"],
        ["main", "Protected production-ready branch."],
        ["release/*", "Release stabilization branches."],
        ["develop", "Integration branch for upcoming work where the workflow requires it."],
        ["feature/*", "Feature development branches."],
        ["hotfix/* and bugfix/*", "Urgent production fixes and normal defect work."],
        ["Rules", "Pull requests required, code reviews mandatory, branch protection on main, conventional commit messages."],
    ], [2400, 6960]))

    body.append(p("4. CI/CD Pipeline", style="Heading1"))
    body.append(p("The pipeline should fail fast on errors and promote artifacts through quality gates, staging verification, manual production approval, and production deployment."))
    body.append(image_paragraph("rIdImage2", "CI/CD Pipeline and Release Gates", "CI CD pipeline and release gates diagram", 2))
    body.append(table([
        ["Pipeline Stage", "Requirement"],
        ["Install and Validate", "Install dependencies, lint, type check, unit tests."],
        ["Test and Build", "Integration tests, build frontend, build backend."],
        ["Security and Package", "Security scan, package Docker images, tag artifacts."],
        ["Staging", "Deploy to staging and run smoke tests."],
        ["Production", "Manual approval, deploy to production, verify health, keep rollback plan ready."],
    ], [2400, 6960]))

    body.append(p("5. Dockerization", style="Heading1"))
    body.append(table([
        ["Artifact", "Requirement"],
        ["Frontend Dockerfile", "Minimal production-ready image or static artifact build."],
        ["Backend Dockerfile", "Minimal Node.js runtime image with health checks and production dependencies."],
        ["Docker Compose", "Local development services for frontend, backend, PostgreSQL, Redis, and Nginx."],
        ["Image Quality", "Small images, deterministic builds, non-root runtime where practical, environment-driven configuration."],
    ], [2400, 6960]))

    body.append(p("6. Production Infrastructure Topology", style="Heading1"))
    body.append(p("The production topology should place Nginx in front of the application services, support HTTPS, REST API routing, WebSocket proxying, Dockerized services, PostgreSQL, Redis, cloud storage, and CDN delivery for public assets."))
    body.append(image_paragraph("rIdImage3", "Production Infrastructure Topology", "Production infrastructure topology diagram", 3))

    body.append(p("7. Reverse Proxy", style="Heading1"))
    body.append(table([
        ["Nginx Responsibility", "Requirement"],
        ["Traffic", "HTTPS termination, HTTP to HTTPS redirects, HTTP/2 support."],
        ["Routing", "Static asset serving, API routing, WebSocket proxying for Socket.IO."],
        ["Performance", "Compression and caching where appropriate."],
        ["Protection", "Security headers and rate limiting."],
    ], [2400, 6960]))

    body.append(p("8. SSL and Domain Management", style="Heading1"))
    body.extend(bullets([
        "Use HTTPS only and redirect all HTTP traffic to HTTPS.",
        "Enable automatic certificate renewal and monitor SSL certificate expiry.",
        "Enable HSTS where appropriate.",
        "Support multiple domains and subdomains for public, admin, API, and environment-specific access.",
    ]))

    body.append(p("9. Secret Management", style="Heading1"))
    body.append(p("Never hard-code secrets. Store database credentials, JWT secrets, Razorpay keys, SMTP credentials, storage credentials, and API tokens in secure environment-specific secret stores. Rotate secrets periodically and document ownership."))

    body.append(p("10. Database Operations", style="Heading1"))
    body.append(table([
        ["Operation", "Requirement"],
        ["Backups", "Daily automated backups with verification."],
        ["Recovery", "Point-in-time recovery where supported."],
        ["Migrations", "Validate migrations before deployment and document rollback approach."],
        ["Growth", "Monitor storage growth, connection usage, and slow queries."],
        ["Future Scale", "Prepare for read replicas and partitioning where required."],
    ], [2400, 6960]))

    body.append(p("11. Redis Operations", style="Heading1"))
    body.append(table([
        ["Usage", "Requirement"],
        ["Live Match State", "Low-latency live match state for real-time views."],
        ["Sessions and Cache", "Session data if required, application cache, and temporary values."],
        ["Queues", "Background job queues where applicable."],
        ["Operations", "Memory limits, eviction policy, persistence if appropriate, and health checks."],
        ["Scaling", "Socket.IO shared adapter strategy for multiple backend instances."],
    ], [2400, 6960]))

    body.append(p("12. File Storage", style="Heading1"))
    body.append(table([
        ["Asset Category", "Examples"],
        ["Images", "Team logos, player photos, tournament banners, gallery assets."],
        ["Generated Files", "Certificates, invoices, receipts, exports, reports."],
        ["Documents", "Verification documents and private uploaded files."],
        ["Policies", "Access control, signed URLs for private assets, optional versioning, lifecycle rules."],
    ], [2400, 6960]))

    body.append(p("13. Monitoring", style="Heading1"))
    body.extend(bullets([
        "Monitor API latency, error rates, CPU, memory, disk usage, database connections, Redis health, Socket.IO connections, and queue length.",
        "Expose health endpoints for infrastructure monitoring.",
        "Track release health immediately after staging and production deployments.",
    ]))

    body.append(p("14. Logging", style="Heading1"))
    body.append(p("Implement centralized structured logging for application logs, access logs, error logs, authentication events, payment events, live score updates, and background job execution. Use correlation IDs to trace requests across services."))

    body.append(p("15. Alerting and Disaster Recovery", style="Heading1"))
    body.append(p("Alerting and recovery plans should protect live tournament operations, payment webhooks, score updates, databases, storage, and production availability."))
    body.append(image_paragraph("rIdImage4", "Observability, Alerting, and Recovery Model", "Observability alerting and recovery model diagram", 4))
    body.append(table([
        ["Area", "Requirement"],
        ["Alerting", "High error rate, failed deployments, database issues, payment webhook failures, Redis failures, disk thresholds, SSL expiry, backup failures."],
        ["Disaster Recovery", "Prepare for database failure, storage outage, server failure, network interruption, and accidental deletion."],
        ["Recovery Targets", "Document Recovery Point Objective and Recovery Time Objective."],
        ["Testing", "Regularly test restore, rollback, and recovery procedures."],
    ], [2400, 6960]))

    body.append(p("16. Scalability", style="Heading1"))
    body.append(table([
        ["Layer", "Scaling Strategy"],
        ["Frontend", "Serve static assets through CDN."],
        ["Backend", "Use stateless application servers behind a load balancer."],
        ["Socket.IO", "Use a shared adapter strategy such as Redis adapter for multiple instances."],
        ["Database", "Prepare for read replicas, indexing, partitioning, and storage growth."],
    ], [2400, 6960]))

    body.append(p("17. Security Operations", style="Heading1"))
    body.extend(bullets([
        "Run dependency vulnerability scanning and container image scanning.",
        "Use rate limiting, IP allow/block lists, and security headers.",
        "Rotate credentials periodically.",
        "Review audit logs and third-party dependencies regularly.",
    ]))

    body.append(p("18. Release Management", style="Heading1"))
    body.append(table([
        ["Release Asset", "Requirement"],
        ["Version", "Every release must have a version number."],
        ["Changelog", "Summarize features, fixes, operations changes, and known risks."],
        ["Database Notes", "Document migrations and compatibility expectations."],
        ["Rollback", "Provide rollback plan and deployment checklist."],
        ["Deployment Style", "Support rolling or blue/green deployments where possible."],
    ], [2400, 6960]))

    body.append(p("19. Maintenance Operations", style="Heading1"))
    body.extend(bullets([
        "Support scheduled maintenance windows and clear user notifications.",
        "Prepare future read-only mode for maintenance-safe access.",
        "Run background migration tasks safely.",
        "Warm caches after deployment and drain queues before shutdown.",
    ]))

    body.append(p("20. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Produce Dockerfiles for frontend and backend.",
        "Create Docker Compose configuration for local development.",
        "Include Nginx configuration supporting REST APIs and Socket.IO.",
        "Generate CI/CD workflow definitions for automated testing and deployment.",
        "Organize environment variables by environment with clear documentation.",
        "Add health check endpoints for all services.",
        "Ensure horizontal scaling without changing business logic.",
        "Implement structured logging and monitoring hooks.",
        "Design deployment artifacts so staging mirrors production as closely as possible.",
    ]))
    body.append(rich_callout("Phase 11 Completion Criteria", [
        "Phase 11 is complete when the environment strategy, repository workflow, CI/CD pipeline, Docker setup, Nginx responsibilities, SSL and domain policy, secret management, database and Redis operations, file storage policy, monitoring, logging, alerting, disaster recovery, scalability, security operations, release management, maintenance operations, and coding rules are ready for implementation planning."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase11_environment_strategy.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase11_cicd_pipeline.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase11_production_infrastructure.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase11_observability_dr.png"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Phase 11 DevOps, Deployment, CI/CD and Production Infrastructure</dc:title>
  <dc:subject>Production infrastructure blueprint covering environments, CI/CD, Docker, Nginx, SSL, secrets, database operations, Redis, storage, monitoring, logging, alerting, recovery, scalability, security, releases, and maintenance</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/phase11_environment_strategy.png": ASSET_DIR / "phase11_environment_strategy.png",
        "word/media/phase11_cicd_pipeline.png": ASSET_DIR / "phase11_cicd_pipeline.png",
        "word/media/phase11_production_infrastructure.png": ASSET_DIR / "phase11_production_infrastructure.png",
        "word/media/phase11_observability_dr.png": ASSET_DIR / "phase11_observability_dr.png",
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
