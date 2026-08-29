from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, page_break, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_6_Management_User_Portal.docx")
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

    body.append(p("PHASE 6 - MANAGEMENT USER PORTAL", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Tournament Operations Dashboard", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 6 Management User Portal"],
        ["Project", "Smart Sportz"],
        ["Focus", "Role-based operations dashboard, assigned tournaments, match management, live scoring, team/player verification, announcements, results, reports, offline-ready scoring, activity logs, and profile management"],
        ["Reference Style", "Same spacing, alignment, borders, margins, and black document treatment as the approved Phase 1 document"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 6 Intent", [
        "This document defines the Smart Sportz Management User Portal. It turns the operations prompt into a structured specification for assigned tournament workflows, live match control, live scoring, verification, results, reports, and future offline operation.",
        "Every route, widget, table, form, button, API call, and real-time action must respect permissions granted by the Super Admin."
    ]))

    body.append(p("1. Module Objective", style="Heading1"))
    body.append(p("Build a role-based operational dashboard for Management Users. The portal should let assigned users manage assigned tournaments, verify teams and players, control live matches, update scores, publish announcements, upload results, and generate reports when permitted."))
    body.extend(bullets([
        "Only show assigned tournament, venue, sport, module, and action data.",
        "Use permission-aware navigation and immediate revocation handling.",
        "Optimize live match and score screens for tablets and mobile devices used at venues.",
        "Synchronize score and match updates instantly to public pages through Socket.IO.",
        "Maintain detailed audit logs for every operational change.",
    ]))

    body.append(p("2. Access Control Scope", style="Heading1"))
    body.append(p("Management Users can access only assigned tournaments, assigned venues, assigned sports, granted modules, and granted actions. Revoked permissions must immediately block frontend UI and backend API access."))
    body.append(image_paragraph("rIdImage1", "Management User Access Scope", "Management User access control scope diagram", 1))

    body.append(page_break())
    body.append(p("3. Portal Layout", style="Heading1"))
    body.append(p("The portal should use a role-scoped top navigation, collapsible sidebar, and main content area tuned for fast tournament operations."))
    body.append(image_paragraph("rIdImage2", "Management User Portal Layout", "Management User portal layout diagram", 2))
    body.append(table([
        ["Layout Area", "Required Behavior"],
        ["Top Navigation", "Tournament switcher, search, notifications, live match status, profile, connection status, and quick context switching."],
        ["Sidebar", "Dashboard, matches, teams, players, live score, fixtures, results, reports, documents, profile. Sidebar collapses on smaller screens."],
        ["Main Content", "Widgets, live data, tables, forms, statistics, operational queues, and reports."],
        ["Permission Awareness", "Hidden or disabled navigation items when access is not granted."],
    ], [2400, 6960]))

    body.append(p("4. Dashboard", style="Heading1"))
    body.append(p("The dashboard must display only assigned tournament data and should prioritize pending actions and live operations."))
    body.append(table([
        ["Dashboard Area", "Required Content"],
        ["Widgets", "Active tournament, today's matches, live matches, pending team verifications, pending player verifications, pending announcements, match completion percentage, and venue occupancy."],
        ["Quick Actions", "Start match, verify team, publish result, and send announcement. Each action appears only if permitted."],
        ["Operational Context", "Current assignment, sport, venue, upcoming match, and active alerts."],
        ["States", "Loading, empty assignment, permission denied, offline, sync pending, and error states."],
    ], [2400, 6960]))

    body.append(p("5. Assigned Tournaments", style="Heading1"))
    body.append(table([
        ["Area", "Specification"],
        ["Columns", "Tournament name, sport, venue, status, registration status, live match count, actions."],
        ["Actions", "View, manage, open dashboard."],
        ["Filtering", "Status, sport, venue, registration state, live match presence, date."],
        ["Security", "Dataset must be server-filtered by assigned tournament IDs and scoped permissions."],
    ], [2400, 6960]))

    body.append(page_break())
    body.append(p("6. Match Management", style="Heading1"))
    body.append(table([
        ["Capability", "Details"],
        ["Filters", "Date, sport, round, venue, and match status."],
        ["Actions", "Start match, pause match, resume match, end match, edit match, reschedule if permitted."],
        ["Controls", "Confirmation dialogs for destructive or state-changing actions."],
        ["Audit", "Record match state changes with user, tournament, match, timestamp, device, and previous/new values."],
    ], [2400, 6960]))

    body.append(p("7. Live Match Control", style="Heading1"))
    body.append(table([
        ["Display Area", "Fields"],
        ["Match Context", "Team A, Team B, timer, current score, match status, officials, venue, and match events."],
        ["Controls", "Start, pause, resume, end, cancel, and emergency stop."],
        ["Sync Requirement", "Changes sync instantly to the public website using Socket.IO."],
        ["Safety", "Emergency stop and cancellation require confirmation and audit logging."],
    ], [2400, 6960]))

    body.append(p("8. Live Score Management", style="Heading1"))
    body.append(p("Live scoring must support sport-specific scoring models. Every score change must be timestamped and reversible when the user has permission."))
    body.append(image_paragraph("rIdImage3", "Live Match and Score Synchronization", "Live match score synchronization diagram", 3))
    body.append(table([
        ["Sport", "Supported Scoring Events"],
        ["Cricket", "Runs, wickets, overs, extras, partnerships."],
        ["Football", "Goals, assists, yellow cards, red cards, substitutions."],
        ["Basketball", "2-point score, 3-point score, free throws, fouls, timeouts."],
        ["Volleyball", "Points, sets, timeouts."],
    ], [2200, 7160]))

    body.append(page_break())
    body.append(p("9. Team and Player Verification", style="Heading1"))
    body.append(table([
        ["Verification Queue", "Checks and Actions"],
        ["Team Verification", "Verify team details, documents, entry fee, eligibility, team size. Actions: approve, reject, request changes."],
        ["Player Verification", "Verify identity, age, documents, eligibility, and team assignment. Actions: approve, reject, request additional documents."],
        ["Audit Requirement", "Capture reviewer, timestamp, decision, reason, previous state, and new state."],
    ], [2600, 6760]))

    body.append(p("10. Officials Management", style="Heading1"))
    body.append(table([
        ["Area", "Specification"],
        ["Assigned People", "Referees, assistant referees, scorers, volunteers."],
        ["Actions", "Assign, reassign, mark attendance, contact."],
        ["Visibility", "Only show officials for assigned tournaments, venues, or matches."],
    ], [2400, 6960]))

    body.append(p("11. Announcements", style="Heading1"))
    body.append(p("Management Users can create tournament-specific announcements when permitted."))
    body.extend(bullets([
        "Types: general, schedule change, venue change, emergency, results published.",
        "Delivery: website, email, SMS, WhatsApp, and future push notification.",
        "Support preview, scheduling, audience targeting, confirmation, and delivery status.",
    ]))

    body.append(page_break())
    body.append(p("12. Results Management", style="Heading1"))
    body.append(table([
        ["Capture Field", "Purpose"],
        ["Final Score", "Record the official match result after completion."],
        ["Winner and MVP", "Identify winning side and key performer."],
        ["Match Duration", "Record start, end, and total duration."],
        ["Match Summary and Remarks", "Operational notes and public-facing summary where permitted."],
        ["Actions", "Save draft, publish, edit if permitted. Publishing updates leaderboards automatically."],
    ], [2600, 6760]))

    body.append(p("13. Fixture View", style="Heading1"))
    body.append(table([
        ["View", "Behavior"],
        ["Calendar View", "Show matches by date, venue, status, and assigned tournament."],
        ["Bracket View", "Show knockout or hybrid structure where supported."],
        ["List View", "Searchable table of fixtures with filters and actions."],
        ["Highlights", "Current match, upcoming match, completed match."],
    ], [2400, 6960]))

    body.append(p("14. Venue Management and Participant Check-In", style="Heading1"))
    body.append(table([
        ["Module", "Specification"],
        ["Venue Monitoring", "View assigned venues, occupancy, current match, upcoming matches, and maintenance alerts."],
        ["Venue Permissions", "Cannot modify venue settings unless permission is granted."],
        ["Participant Check-In", "Support QR code or manual check-in for team arrival, player arrival, and official arrival."],
        ["Check-In Status", "Checked in, late, absent."],
    ], [2600, 6760]))

    body.append(page_break())
    body.append(p("15. Document Center", style="Heading1"))
    body.append(table([
        ["Document Type", "Access Rules"],
        ["Rule Book", "View/download based on tournament assignment and document permission."],
        ["Fixtures", "View/download generated fixtures for assigned tournaments."],
        ["Team Lists", "View assigned teams and approved participant lists."],
        ["Certificates", "Access generated certificates when permitted."],
        ["Venue Maps", "Download or view maps for assigned venues."],
    ], [2400, 6960]))

    body.append(p("16. Reports", style="Heading1"))
    body.append(table([
        ["Report", "Scope"],
        ["Match Report", "Match details, score events, officials, timeline, final result."],
        ["Team Report", "Team verification, eligibility, attendance, tournament participation."],
        ["Player Report", "Player verification, age, documents, eligibility, participation."],
        ["Attendance Report", "Team, player, and official check-in status."],
        ["Live Score Summary", "Score events, reversals, timestamps, operator activity."],
        ["Exports", "PDF, Excel, CSV where permitted."],
    ], [2400, 6960]))

    body.append(p("17. Notifications and Profile", style="Heading1"))
    body.append(table([
        ["Area", "Specification"],
        ["Inbox Alerts", "New assignment, match start reminder, registration approval needed, payment issue, schedule change, emergency announcement."],
        ["Notification State", "Read and unread status with filtering."],
        ["Profile Management", "Profile photo, name, contact details, password, notification preferences."],
        ["Profile Visibility", "Assigned roles, assigned tournaments, last login, activity history."],
    ], [2400, 6960]))

    body.append(page_break())
    body.append(p("18. Offline Mode", style="Heading1"))
    body.append(p("The live scoring interface should be future-ready for intermittent connectivity at outdoor venues and tournament grounds."))
    body.append(image_paragraph("rIdImage4", "Offline-Ready Venue Workflow", "Offline-ready venue workflow diagram", 4))
    body.extend(bullets([
        "Cache score updates locally.",
        "Queue updates while offline.",
        "Synchronize automatically when the connection is restored.",
        "Detect and resolve synchronization conflicts.",
        "Show clear operator feedback for synced, pending, failed, retry, and manual review states.",
    ]))

    body.append(p("19. Activity Log and Performance Dashboard", style="Heading1"))
    body.append(table([
        ["Feature", "Required Data"],
        ["Activity Log", "Timestamp, action, tournament, device, and examples such as match started, score updated, team approved, result published."],
        ["Performance Metrics", "Matches managed, scores updated, teams verified, players verified, average update time."],
        ["Visibility", "Performance dashboard visible only to the user and Super Admin."],
    ], [2600, 6760]))

    body.append(p("20. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Build a modular dashboard using reusable widgets.",
        "Enforce RBAC checks in both frontend and backend.",
        "Use Socket.IO for real-time score synchronization.",
        "Optimize the live score interface for tablets and mobile devices used at venues.",
        "Implement autosave for score updates where appropriate.",
        "Provide confirmation dialogs for destructive actions.",
        "Maintain detailed audit logs for every operational change.",
        "Ensure the UI remains responsive and usable in outdoor tournament environments with varying network conditions.",
        "Use server-side filtering for assignment-scoped data and never trust client-side filtering alone.",
    ]))
    body.append(rich_callout("Phase 6 Completion Criteria", [
        "Phase 6 is complete when the Management User portal objective, permission scope, layout, dashboard, assigned tournaments, match control, live scoring, verification workflows, officials, announcements, results, fixtures, venue monitoring, check-in, documents, reports, notifications, profile, offline readiness, activity log, performance dashboard, and implementation rules are clear enough for production planning."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase6_access_control_scope.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase6_management_portal_layout.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase6_live_match_score_sync.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase6_offline_venue_workflow.png"/>
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
  <dc:title>Smart Sportz - Phase 6 Management User Portal</dc:title>
  <dc:subject>Role-based tournament operations dashboard, live score management, verification, reports, offline mode, and activity logging specification</dc:subject>
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
        "word/media/phase6_access_control_scope.png": ASSET_DIR / "phase6_access_control_scope.png",
        "word/media/phase6_management_portal_layout.png": ASSET_DIR / "phase6_management_portal_layout.png",
        "word/media/phase6_live_match_score_sync.png": ASSET_DIR / "phase6_live_match_score_sync.png",
        "word/media/phase6_offline_venue_workflow.png": ASSET_DIR / "phase6_offline_venue_workflow.png",
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
