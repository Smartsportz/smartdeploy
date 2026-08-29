from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, page_break, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_5_Super_Admin_Portal_Part_1.docx")
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

    body.append(p("PHASE 5 - SUPER ADMIN PORTAL (PART 1)", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Super Admin Control Center", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 5 Super Admin Portal (Part 1)"],
        ["Project", "Smart Sportz"],
        ["Focus", "Enterprise administration portal, dashboard, navigation shell, user management, Azure-style RBAC, tournaments, master data, finance, CMS, notifications, reports, audit logs, and system settings"],
        ["Reference Style", "Same spacing, alignment, borders, margins, and black document treatment as the approved Phase 1 document"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 5 Intent", [
        "This document defines Part 1 of the Smart Sportz Super Admin Portal. It converts the raw administration prompt into a structured control-center specification for future frontend, backend, database, RBAC, audit, and reporting implementation.",
        "The Super Admin portal should feel like a modern cloud management console: fast, searchable, permission-aware, table-driven, audit-friendly, and ready for future multi-tenant SaaS expansion."
    ]))

    body.append(p("1. Portal Objective", style="Heading1"))
    body.append(p("Build the highest-privilege administration portal for Smart Sportz. The Super Admin must be able to control organizations, tournaments, users, permissions, payments, sports, venues, live matches, reports, website CMS, notifications, security, and settings from one unified interface."))
    body.extend(bullets([
        "Provide an executive view of the complete platform.",
        "Support operational management through searchable tables, filters, drawers, forms, modals, and bulk actions.",
        "Enforce granular RBAC for every sensitive action.",
        "Log every important administrative change for audit and security review.",
        "Prepare the system for future SaaS mode with organization switching and scoped permissions.",
    ]))

    body.append(p("2. Global Admin Layout", style="Heading1"))
    body.append(p("The admin layout should use a clean sidebar, sticky top navigation, dynamic main content region, command palette, dashboard widgets, and table-first operational views."))
    body.append(image_paragraph("rIdImage1", "Super Admin Shell Layout", "Super Admin shell layout diagram", 1))

    body.append(p("3. Top Navigation", style="Heading1"))
    body.append(table([
        ["Navigation Item", "Purpose"],
        ["Global Search", "Search tournaments, teams, players, organizations, payments, users, reports, and CMS content."],
        ["Quick Actions", "Create tournament, add sport, add venue, create user, send announcement, and other shortcut actions."],
        ["Notifications", "Show operational alerts, failed payments, pending approvals, live match events, and system warnings."],
        ["Live Match Indicator", "Display active live matches and provide fast navigation into live match control."],
        ["Theme Toggle", "Switch between light and dark mode where supported by the app design system."],
        ["Profile and Settings", "Access account profile, security, settings shortcut, and logout."],
        ["Organization Switcher", "Future-ready control for SaaS and multi-organization operation."],
    ], [2600, 6760]))

    body.append(page_break())
    body.append(p("4. Sidebar Information Architecture", style="Heading1"))
    body.append(table([
        ["Group", "Pages"],
        ["Dashboard", "Overview, Analytics, Activity Feed"],
        ["Tournament Management", "All Tournaments, Create Tournament, Fixtures, Matches, Live Matches, Results"],
        ["Registration", "Registrations, Teams, Players, Waitlist"],
        ["Finance", "Payments, Refunds, Coupons, Revenue"],
        ["User Management", "Management Users, Roles, Permissions, Audit Logs"],
        ["Master Data", "Sports, Venues, Categories, Age Groups, Organizations"],
        ["Website", "Homepage CMS, Gallery, Sponsors, Blogs, FAQs, Contact Requests"],
        ["Reports", "Tournament Reports, Financial Reports, Participation Reports, Custom Reports"],
        ["Settings", "General, Branding, Payment Gateway, Notifications, Email Templates, Integrations, Security"],
    ], [2600, 6760]))

    body.append(p("5. Dashboard Page", style="Heading1"))
    body.append(p("The dashboard provides an executive overview of the whole platform and should support fast drill-down into operational queues."))
    body.append(table([
        ["Dashboard Area", "Required Content"],
        ["KPI Widgets", "Active tournaments, live matches, upcoming events, teams registered, players registered, revenue, pending approvals, payments today, refund requests, active management users."],
        ["Charts", "Registrations over time, revenue trend, sport-wise participation, and live match distribution."],
        ["Activity Feed", "Tournament created, payment received, match started, match completed, user created, and other key events."],
        ["Quick Actions", "Create tournament, add sport, add venue, create user, and send announcement."],
    ], [2400, 6960]))

    body.append(p("6. Super Admin Module Map", style="Heading1"))
    body.append(p("The Super Admin module map organizes the portal around domain ownership areas. Each area should be implemented as an independent React route with nested layouts and reusable CRUD primitives."))
    body.append(image_paragraph("rIdImage2", "Super Admin Module Map", "Super Admin module map diagram", 2))

    body.append(page_break())
    body.append(p("7. Management User Page", style="Heading1"))
    body.append(p("This page allows the Super Admin to create, manage, suspend, activate, delete, and permission operational users."))
    body.append(table([
        ["Area", "Specification"],
        ["Table Columns", "Name, email, mobile, role, assigned tournaments, status, last login, actions."],
        ["Row Actions", "View, edit, reset password, assign permissions, suspend, activate, delete."],
        ["Bulk Actions", "Activate, suspend, export, delete."],
        ["Expected States", "Loading, empty, filtered empty, error, permission denied, confirmation, success, and destructive-action confirmation."],
    ], [2400, 6960]))

    body.append(p("8. Create Management User", style="Heading1"))
    body.append(table([
        ["Form Group", "Fields"],
        ["Identity", "First name, last name, email, mobile number, username, profile photo."],
        ["Security", "Password, confirm password, password policy validation, reset invitation option."],
        ["Employment", "Role, department, employee ID, status."],
        ["Assignments", "Tournaments, sports, venues."],
        ["Permission Templates", "Tournament Manager, Live Score Manager, Registration Officer, Finance Officer, Read Only, Custom."],
    ], [2400, 6960]))

    body.append(p("9. Azure-Style RBAC", style="Heading1"))
    body.append(p("Every permission should be individually assignable. Permissions should support inheritance, reusable groups, and scoped assignment by tournament, sport, venue, organization, module, or global platform level."))
    body.append(image_paragraph("rIdImage3", "Azure-Style RBAC Permission Model", "Azure-style RBAC permission model diagram", 3))
    body.append(table([
        ["Domain", "Permissions"],
        ["Tournament", "Create, view, edit, delete, publish, archive."],
        ["Matches", "Create, start, pause, resume, end, edit, delete."],
        ["Live Scores", "View, update, override, reset."],
        ["Teams", "Create, edit, delete, import, export."],
        ["Players", "Create, edit, delete, verify."],
        ["Registrations", "View, approve, reject, waitlist."],
        ["Payments", "View, verify, refund, export."],
        ["Reports", "View, export, schedule."],
        ["CMS", "Edit homepage, manage gallery, manage sponsors, publish blogs."],
        ["System", "Settings, integrations, audit logs, API keys."],
    ], [2200, 7160]))

    body.append(page_break())
    body.append(p("10. Tournament Management", style="Heading1"))
    body.append(table([
        ["Capability", "Details"],
        ["Core Actions", "Create tournament, edit tournament, publish, unpublish, duplicate, archive, delete."],
        ["Filters", "Sport, status, date, venue, organizer."],
        ["Tournament Detail Tabs", "Overview, registration, fixtures, teams, players, payments, live matches, reports."],
        ["Controls", "Use confirmation dialogs for destructive actions and publish/unpublish workflows."],
    ], [2400, 6960]))

    body.append(p("11. Sports, Venues, and Organizations", style="Heading1"))
    body.append(table([
        ["Module", "Fields and Features"],
        ["Sports Management", "Sport name, icon, banner, description, rules, status, add, edit, disable, delete."],
        ["Venue Management", "Venue name, address, city, state, country, capacity, number of courts/grounds, GPS coordinates, photos, availability calendar, maintenance status, venue map."],
        ["Organization Management", "Organization name, type, logo, contact person, email, phone, address, subscription plan, status. Supports future multi-tenant SaaS mode."],
    ], [2600, 6760]))

    body.append(p("12. Payment and Coupon Management", style="Heading1"))
    body.append(table([
        ["Area", "Specification"],
        ["Payment Dashboard", "Today's revenue, total revenue, pending payments, failed payments, and refunds."],
        ["Payment Table", "Transaction ID, tournament, participant, amount, method, status, date, and actions."],
        ["Payment Actions", "View, verify, refund, export."],
        ["Coupon Fields", "Coupon code, discount type, discount value, valid from, valid to, usage limit, applicable tournaments, status."],
    ], [2400, 6960]))

    body.append(page_break())
    body.append(p("13. Notification Center", style="Heading1"))
    body.append(p("The notification center should let Super Admin users create, schedule, preview, and send Email, SMS, WhatsApp, and push notifications."))
    body.extend(bullets([
        "Targets: all users, specific tournament, selected teams, selected players, and management users.",
        "Support templates for recurring notifications.",
        "Track delivery status, failures, retries, and sender identity.",
        "Require confirmation for high-volume sends.",
    ]))

    body.append(p("14. Website CMS", style="Heading1"))
    body.append(table([
        ["CMS Area", "Managed Content"],
        ["Homepage", "Hero, live banner, featured tournaments, testimonials, FAQs, about us, contact details, footer links."],
        ["Media", "Gallery, sponsor logos, banners, and published images."],
        ["Content", "Blogs, FAQs, contact requests, footer links, privacy and policy references where applicable."],
        ["Publishing", "Changes should support preview before publishing and maintain a publish history."],
    ], [2400, 6960]))

    body.append(p("15. Reports", style="Heading1"))
    body.append(table([
        ["Report Type", "Purpose"],
        ["Tournament Performance", "Tournament status, participation, outcomes, match activity, and operational health."],
        ["Team Participation", "Team counts, category breakdowns, registrations, approvals, and participation trend."],
        ["Player Participation", "Player count, demographics, category participation, and verification status."],
        ["Revenue and Payments", "Collected revenue, pending payments, failed payments, refunds, coupon usage, and reconciliation."],
        ["Live Match Statistics", "Live status, match timelines, results, and sport-specific scoring indicators."],
        ["Export Options", "PDF, Excel, CSV, and scheduled email delivery."],
    ], [2600, 6760]))

    body.append(page_break())
    body.append(p("16. Audit Logs and System Settings", style="Heading1"))
    body.append(p("Every administrative action must be searchable, exportable, and traceable. Settings should be versioned so configuration changes can be reviewed and audited."))
    body.append(image_paragraph("rIdImage4", "Admin Action, Audit, and Settings Flow", "Admin action audit and settings flow diagram", 4))
    body.append(table([
        ["Audit Field", "Description"],
        ["Timestamp", "Exact time the action occurred."],
        ["User", "Admin or management user who performed the action."],
        ["Action and Module", "The action type and module affected."],
        ["Previous and New Value", "Before/after values for meaningful changes."],
        ["IP Address and Device", "Security metadata for investigation and compliance."],
    ], [2600, 6760]))
    body.append(table([
        ["Settings Category", "Scope"],
        ["General and Branding", "Platform identity, logos, colors, public identity, and basic configuration."],
        ["Payment Gateway", "Razorpay keys, webhook settings, payment modes, refund rules, and reconciliation preferences."],
        ["Email, SMS, WhatsApp", "Provider credentials, templates, sender identities, delivery preferences."],
        ["Security", "Password policy, session policy, token configuration, API keys, and access controls."],
        ["Integrations, Backup, Maintenance", "External service settings, backup policy, and maintenance mode control."],
    ], [2600, 6760]))

    body.append(p("17. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Build each module as an independent React route with nested layouts.",
        "Use reusable CRUD components for tables, forms, filters, drawers, and modals.",
        "Implement Azure-style RBAC with granular permissions and scope-aware enforcement.",
        "Use optimistic UI updates where appropriate.",
        "Require confirmation dialogs for all destructive, financial, publishing, approval, refund, and permission actions.",
        "Provide audit logging for create, update, delete, publish, approve, refund, and permission changes.",
        "Implement server-side pagination, filtering, and sorting.",
        "Design the portal for future multi-tenant SaaS expansion without major architectural changes.",
        "Include loading, empty, error, success, permission-denied, and retry states in every operational page.",
    ]))
    body.append(rich_callout("Phase 5 Completion Criteria", [
        "Phase 5 Part 1 is complete when the Super Admin portal objective, navigation shell, sidebar structure, dashboard, management-user workflow, granular RBAC, tournament controls, master data, finance, notifications, CMS, reports, audit logs, settings, and implementation rules are clear enough for production planning."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase5_admin_shell_layout.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase5_super_admin_module_map.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase5_rbac_permission_model.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase5_admin_action_audit_flow.png"/>
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
  <dc:title>Smart Sportz - Phase 5 Super Admin Portal Part 1</dc:title>
  <dc:subject>Super Admin control center, RBAC, dashboard, management users, finance, CMS, reports, audit logs, and settings specification</dc:subject>
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
        "word/media/phase5_admin_shell_layout.png": ASSET_DIR / "phase5_admin_shell_layout.png",
        "word/media/phase5_super_admin_module_map.png": ASSET_DIR / "phase5_super_admin_module_map.png",
        "word/media/phase5_rbac_permission_model.png": ASSET_DIR / "phase5_rbac_permission_model.png",
        "word/media/phase5_admin_action_audit_flow.png": ASSET_DIR / "phase5_admin_action_audit_flow.png",
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
