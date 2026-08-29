from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import p, rich_callout, style_xml, table, x
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


OUT = Path("docs/Smart_Sportz_Stitch_Frontend_UI_Model_Reference.docx")
REF = Path("stitch_smart_sportz_management_platform")

SCREENSHOTS = {
    "landing": REF / "smart_sportz_landing_page" / "screen.png",
    "registration": REF / "tournament_details_registration" / "screen.png",
    "live": REF / "live_match_basketball_finals" / "screen.png",
    "admin": REF / "admin_dashboard" / "screen.png",
}


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def image_paragraph_actual(
    rel_id: str,
    name: str,
    descr: str,
    doc_pr_id: int,
    px_w: int,
    px_h: int,
    max_width_in: float = 6.7,
    max_height_in: float = 5.35,
) -> str:
    ratio = px_w / px_h
    width_in = min(max_width_in, max_height_in * ratio)
    height_in = width_in / ratio
    cx = int(width_in * 914400)
    cy = int(height_in * 914400)
    return f'''
<w:p>
  <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="80"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="{x(name)}" descr="{x(descr)}"/>
        <wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/></wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="{doc_pr_id}" name="{x(name)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{rel_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''


def document_xml() -> str:
    body: list[str] = []

    body.append(p("SMART SPORTZ - STITCH FRONTEND UI MODEL REFERENCE", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Frontend Screens, Visual Model, Workflows, Components, and Page Behavior Reference", style="Subtitle"))
    body.append(p("Created from the local stitch_smart_sportz_management_platform reference folder", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Stitch Frontend UI Model Reference"],
        ["Project", "Smart Sportz"],
        ["Source Folder", r"D:\JOB\Brillaris\Smart_Sportz\stitch_smart_sportz_management_platform"],
        ["Reference Screens", "Landing page, tournament detail and registration page, live match basketball finals page, and admin dashboard page"],
        ["Design Model", "Kinetic Velocity: stadium-tech, dark navy, glassmorphism, live sports broadcast energy, data-focused management UI"],
        ["Instruction", "Reference-only document. No frontend implementation or code changes are included."],
        ["Date", "July 12, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Reference-Only Scope", [
        "This document observes the provided frontend screenshots and model notes. It does not implement, edit, or replace the application.",
        "The goal is to preserve the design direction, screen intent, workflow behavior, component model, and future implementation guidance in a clean Word document."
    ]))

    body.append(p("1. Reference Package Overview", style="Heading1"))
    body.append(p("The Stitch reference package contains four visual screens and one design model file. Together they define the front-facing sports brand, tournament registration conversion flow, live match experience, and admin operations experience for Smart Sportz."))
    body.append(table([
        ["Reference", "What It Defines"],
        ["smart_sportz_landing_page", "Public marketing and discovery page with hero, live feed, featured series, global statistics, upcoming fixtures, capabilities, and footer."],
        ["tournament_details_registration", "Tournament detail page with event hero, rules, schedule, prize pool, venue, organizer/contact strip, and secure registration/payment form."],
        ["live_match_basketball_finals", "Live match viewing page with score center, timer, team cards, statistics, rosters, officials, timeline, and admin-only commentary input."],
        ["admin_dashboard", "Executive/admin operations dashboard with sidebar navigation, KPI cards, live match controls, registration analytics, tournament registry, filters, export, and create tournament action."],
        ["kinetic_velocity/DESIGN.md", "Design tokens and brand model: colors, typography, layout, spacing, depth, shapes, and component behavior."],
    ], [2600, 6760]))

    body.append(p("2. Kinetic Velocity Design Model", style="Heading1"))
    body.append(p("The model is a premium sports-management interface: dark, cinematic, broadcast-aware, and data-dense without looking like a spreadsheet. It should feel elite and operational at the same time."))
    body.append(table([
        ["Design Area", "Reference Rule"],
        ["Brand Personality", "Authoritative, kinetic, elite, high-stakes, and broadcast-ready."],
        ["Base Palette", "Deep navy and charcoal surfaces: #0b1326, #060e20, #131b2e, #171f33, #222a3d, #2d3449."],
        ["Primary Accent", "Electric blue for navigation states, primary actions, active dashboard elements, focus rings, and pro-tier highlights."],
        ["Secondary Accent", "Vibrant orange for tournament progress, payment/conversion points, active energy, and important callouts."],
        ["Live Accent", "Red live status with a small dot and pulse behavior for active matches, live feeds, urgent events, and real-time alerts."],
        ["Typography", "Anton for large uppercase headings, Inter for readable UI/body content, JetBrains Mono for metadata, timestamps, IDs, and score/ticker details."],
        ["Depth", "Glassmorphism: translucent dark cards, subtle 1px borders, backdrop blur, and soft glow for overlays instead of heavy black shadows."],
        ["Spacing", "8px base rhythm, 24px gutters, 48px desktop margins, 16px mobile margins, and max-width around 1440px."],
        ["Shape", "4px standard button/input radius, 8px card radius, rounded-full status tags."],
    ], [2200, 7160]))
    body.extend(bullets([
        "The design should use strong visual hierarchy: huge condensed page headings, smaller mono labels, and compact data readouts.",
        "The UI should avoid pastel SaaS softness; it should feel like a tournament operations room connected to a live stadium broadcast.",
        "Status color must be meaningful: blue for active/primary, orange for energy/payment/progress, red for live/urgent, green for healthy/open/approved.",
    ]))

    body.append(p("3. Public Landing Page Reference", style="Heading1"))
    body.append(image_paragraph_actual("rIdLanding", "Smart Sportz Landing Page Screenshot", "Public landing page reference screenshot", 1, 603, 1600))
    body.append(table([
        ["Area", "Observed Detail"],
        ["Hero", "Full stadium image background with deep dark overlay, small badge, large uppercase headline, supporting copy, and two CTAs: Explore Tournaments and Register Now."],
        ["Navigation", "Logo left, compact top nav, search icon, and Admin Login action. Active nav state uses small underline/tint."],
        ["Live Feed", "Horizontal ticker below hero with live match labels and compact score/status text."],
        ["Featured Series", "Three image-backed tournament cards with sport badge, title, prize pool, and Join Now action."],
        ["Global Stats", "Large compact numeric row: global events, active players, streaming reach, data accuracy."],
        ["Upcoming Fixtures", "Filter tabs plus fixture cards showing category/status, date, teams, and details action."],
        ["Capabilities", "Three capability cards: real-time sync, secure payments, deep analytics."],
        ["Footer", "Brand, copyright, policy links, contact/sponsorship links, and social/action icons."],
    ], [2200, 7160]))

    body.append(p("4. Tournament Detail and Registration Reference", style="Heading1"))
    body.append(image_paragraph_actual("rIdRegistration", "Tournament Detail Registration Screenshot", "Tournament detail and registration reference screenshot", 2, 598, 1600))
    body.append(table([
        ["Area", "Observed Detail"],
        ["Event Hero", "Arena background, Registration Open badge, Elite Series tag, huge tournament title, Register Now and Download Rulebook actions."],
        ["Rules Panel", "Compact tournament rule list with icon heading and structured bullet requirements."],
        ["Prize Pool", "Prize amount emphasized with orange accent; breakdown for 1st place, 2nd place, and MVP award."],
        ["Schedule", "Round cards for qualifiers, quarter finals, semi finals, and grand finale with dates and notes."],
        ["Entry Fee", "Fee card with included items such as official team kit, hydration/snacks, and digital game analytics."],
        ["Venue", "Arena card with address and embedded map visual."],
        ["Organizer Strip", "Organizer identity, contact email, message/phone quick actions."],
        ["Registration Form", "Team/captain/contact fields, player roster fields, add player action, secure payment note, and Pay Entry Fee CTA."],
    ], [2200, 7160]))

    body.append(p("5. Live Match Basketball Finals Reference", style="Heading1"))
    body.append(image_paragraph_actual("rIdLive", "Live Match Basketball Finals Screenshot", "Live match page reference screenshot", 3, 1495, 1600))
    body.append(table([
        ["Area", "Observed Detail"],
        ["Match Header", "Live badge, match number, quarter, tournament name, sport, venue, and central score panel."],
        ["Scoreboard", "Home and away team blocks, team marks, large score, game clock, and home/away labels."],
        ["Statistics", "Possession split, field goal percentage bars, fouls, timeouts, and card/event counters."],
        ["Rosters", "Team roster cards with jersey number, player name, position, and points."],
        ["Officials", "Official/referee listing with role badges."],
        ["Live Timeline", "Auto-update timeline with timestamps, period marker, event type tags, commentary text, and score context."],
        ["Admin Input", "Commentary input at bottom marked admin-only, with send action."],
        ["Footer", "Public site footer remains consistent with brand and legal links."],
    ], [2200, 7160]))

    body.append(p("6. Admin Dashboard Reference", style="Heading1"))
    body.append(image_paragraph_actual("rIdAdmin", "Admin Dashboard Screenshot", "Admin dashboard reference screenshot", 4, 1270, 1600))
    body.append(table([
        ["Area", "Observed Detail"],
        ["Top Bar", "Brand, public nav, search input, and Admin Login button remain visible."],
        ["Sidebar", "Admin Panel identity, Dashboard, Tournaments, Teams, Analytics, Settings, Create Tournament CTA, Help, and Logout."],
        ["Executive Header", "Executive Dashboard title, system health description, and System Status: Optimal pill."],
        ["KPI Cards", "Today's matches, total revenue, active players, and upcoming matches with icons, badges, values, and progress bars."],
        ["Live Match Control", "Table for live match details, score, time elapsed, and actions such as Update Score and End Match."],
        ["Registration Analytics", "Bar chart by day with team sign-up and individual user trend cards."],
        ["Tournament Registry", "Table with tournament name, status, teams registered progress, prize pool, row action menu, export CSV, and filters."],
        ["Operations Tone", "Data-dense but not flat; the design uses large headings and compact cards to preserve energy."],
    ], [2200, 7160]))

    body.append(p("7. Cross-Screen Navigation and Layout Model", style="Heading1"))
    body.append(table([
        ["Pattern", "Frontend Rule"],
        ["Brand Header", "All public and dashboard pages should keep Smart Sportz identity visible and consistent."],
        ["Navigation", "Home, Live, Tournaments, Sports, Gallery, About, Search, and Admin Login are the shared public navigation model."],
        ["Dark Surface", "Every page uses the same deep navy base and elevated glass cards for continuity."],
        ["Responsive Behavior", "Desktop uses wide grids and sidebars; tablet reduces columns; mobile should stack sections and collapse admin navigation."],
        ["Footer", "Policy, terms, contact, sponsorship, copyright, and social/action icons should remain consistent."],
        ["Search", "Public search is compact in landing/detail pages and expanded in admin dashboard."],
        ["Status Language", "Use visible status tags for Live, Registration Open, Completed, Upcoming, Next 48h, Active Now, and System Optimal."],
    ], [2200, 7160]))

    body.append(p("8. Component Model", style="Heading1"))
    body.append(table([
        ["Component", "Behavior and Style"],
        ["Primary Button", "Electric blue or light blue filled button with compact mono/caps label and strong hover/focus state."],
        ["Conversion Button", "Orange filled button for payment, registration, and high-energy conversion actions."],
        ["Ghost Button", "Transparent dark/glass background with subtle border for secondary actions like rulebook, filters, details, and export."],
        ["Status Badge", "Rounded pill or compact label using semantic color: red live, green open/healthy, orange progress/payment, blue active."],
        ["Card", "Dark glass surface, thin border, 8px radius, strong heading, compact metadata, and icon or sport visual."],
        ["Data Table", "Dark rows, mono headings, clear columns, compact actions, and progress bars for registration or score context."],
        ["Form Field", "Dark input, 1px border, focused electric-blue glow, clear placeholder, and tight labels."],
        ["Timeline Item", "Vertical rail, dot marker, timestamp, period, event tag, commentary, and optional score context."],
        ["Progress Bar", "Muted track with electric blue or orange fill depending on context."],
        ["Map/Media Panel", "Framed card with embedded image/map and address/action details beside or above it depending on viewport."],
    ], [2200, 7160]))

    body.append(p("9. Frontend Workflow Mapping", style="Heading1"))
    body.append(table([
        ["Workflow", "Screen and User Journey"],
        ["Tournament Discovery", "Landing hero -> Featured Series -> Upcoming Fixtures -> Tournament Detail."],
        ["Tournament Registration", "Tournament Detail -> Register Now -> Secure Spot form -> Pay Entry Fee -> confirmation/receipt."],
        ["Live Match Viewing", "Live nav -> Match page -> real-time score, stats, rosters, timeline, and public updates."],
        ["Admin Match Control", "Dashboard -> Live Match Control -> Update Score / End Match -> live page and timeline update."],
        ["Admin Tournament Operations", "Dashboard sidebar -> Tournaments/Teams/Analytics/Settings -> Create Tournament -> registry and reports."],
        ["Registration Monitoring", "Dashboard registration chart -> tournament registry -> team/individual signup tracking."],
        ["Reporting and Export", "Admin dashboard -> Filters / Export CSV -> reports and operational review."],
    ], [2200, 7160]))

    body.append(p("10. Page Requirements From Reference Screens", style="Heading1"))
    body.append(table([
        ["Page", "Required Sections"],
        ["Landing Page", "Hero, live ticker, featured series, statistics, upcoming fixtures, capability cards, footer."],
        ["Tournament Detail", "Hero, registration badge, rulebook action, rules, prize pool, schedule, fee, venue/map, organizer contact."],
        ["Registration Form", "Team name, captain name, email, phone, roster fields, add player action, secure payment note, payment CTA, policy note."],
        ["Live Match Page", "Match metadata, scoreboard, timer, stats, rosters, officials, timeline, admin commentary input, footer."],
        ["Admin Dashboard", "Sidebar, KPI cards, system status, live match table, registration chart, tournament registry, export/filter actions."],
    ], [2200, 7160]))

    body.append(p("11. Implementation Guidance for Future Build", style="Heading1"))
    body.extend(bullets([
        "Use the reference as the visual and workflow target, not as final production code.",
        "Preserve the Kinetic Velocity brand model: Anton display headings, Inter interface text, JetBrains Mono metadata, navy glass surfaces, electric blue/orange/red accents.",
        "Translate static HTML screens into reusable React components: AppShell, Header, Footer, SportCard, TournamentCard, StatCard, DataTable, Timeline, Scoreboard, RegistrationForm, AdminSidebar, KPIGrid.",
        "Connect each visible workflow to internal APIs already documented in the API master document: public, auth, tournaments, registrations, payments, live score, admin, CMS, notifications, and reports.",
        "For production, replace static map/image/sample data with CMS, tournament, venue, match, registration, and payment APIs.",
        "All real-time pages should be Socket.IO-ready and React Query-ready so live score and dashboard changes update without full refresh.",
        "Keep accessibility in mind: visible focus states, semantic form labels, readable contrast, keyboard navigation, and responsive table alternatives for mobile.",
    ]))

    body.append(p("12. Acceptance Criteria", style="Heading1"))
    body.extend(bullets([
        "The final frontend should visually match the dark stadium-tech direction shown in the Stitch references.",
        "Landing, tournament detail, live match, and admin dashboard pages should each have complete responsive states.",
        "Registration and payment should feel secure and focused, with no unnecessary blank space or confusing form layout.",
        "Live score screens should clearly separate public viewing, admin control, statistics, and timeline/commentary behavior.",
        "Admin pages should remain operationally dense while preserving premium typography, spacing, and visual hierarchy.",
        "Every reusable component should support loading, empty, error, success, disabled, permission-denied, and mobile states.",
    ]))
    body.append(rich_callout("Stitch Frontend Reference Completion Criteria", [
        "This document is complete when it records the design model, screen-level observations, common component behavior, page requirements, workflow mapping, and future implementation guidance from the provided frontend images and Kinetic Velocity model."
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
  <Relationship Id="rIdLanding" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/stitch_landing_screen.png"/>
  <Relationship Id="rIdRegistration" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/stitch_registration_screen.png"/>
  <Relationship Id="rIdLive" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/stitch_live_match_screen.png"/>
  <Relationship Id="rIdAdmin" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/stitch_admin_dashboard_screen.png"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Stitch Frontend UI Model Reference</dc:title>
  <dc:subject>Frontend screenshots, Kinetic Velocity design model, screen observations, workflows, components, and future implementation guidance</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/stitch_landing_screen.png": SCREENSHOTS["landing"],
        "word/media/stitch_registration_screen.png": SCREENSHOTS["registration"],
        "word/media/stitch_live_match_screen.png": SCREENSHOTS["live"],
        "word/media/stitch_admin_dashboard_screen.png": SCREENSHOTS["admin"],
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
