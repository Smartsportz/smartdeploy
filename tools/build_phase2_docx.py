from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, page_break, r, rich_callout, style_xml, table, tag, x


OUT = Path("docs/Smart_Sportz_Phase_2_Design_System_Landing_Page.docx")
ASSET_DIR = Path("docs/assets")

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_PIC = "http://schemas.openxmlformats.org/drawingml/2006/picture"


def image_paragraph(rel_id: str, name: str, descr: str, doc_pr_id: int, width_in: float = 6.8) -> str:
    cx = int(width_in * 914400)
    cy = int((width_in / (1600 / 820)) * 914400)
    return f'''
<w:p>
  <w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="{x(name)}" descr="{x(descr)}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
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
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{cx}" cy="{cy}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>'''


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


def document_xml() -> str:
    body: list[str] = []

    body.append(p("PHASE 2 - DESIGN SYSTEM & LANDING PAGE SPECIFICATION", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - UI/UX Design Language", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 2 Design System and Landing Page Specification"],
        ["Project", "Smart Sportz"],
        ["Focus", "Premium SaaS design language, UI component standards, landing page structure, and dashboard design direction"],
        ["Reference Style", "Same spacing, alignment, borders, margins, and black document treatment as the approved Phase 1 document"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 2 Intent", [
        "This document defines the Smart Sportz visual language and landing-page specification. It converts the design prompt into a structured UI/UX foundation for future frontend implementation.",
        "The product interface should feel premium, modern, responsive, and sports-tech focused while remaining original and usable."
    ]))

    body.append(p("1. AI Design Role", style="Heading1"))
    body.append(p("The AI should act as a world-class UI/UX design team responsible for product design, design-system architecture, motion, accessibility, and frontend design quality."))
    for item in [
        "Principal Product Designer",
        "Senior UI Designer",
        "UX Researcher",
        "Design System Architect",
        "Motion Designer",
        "Frontend Design Engineer",
        "Accessibility Specialist",
    ]:
        body.append(p(item, num_id=1))
    body.append(p("Design inspiration should come from premium SaaS products such as Linear, Stripe, Notion, Vercel, Figma, Framer, and modern sports technology platforms. The result must be original, clean, responsive, and optimized for usability."))

    body.append(p("2. Design Philosophy", style="Heading1"))
    body.append(p("The Smart Sportz interface should communicate energy, precision, professionalism, trust, speed, simplicity, and modern sports technology."))
    for item in [
        "Avoid clutter and unnecessary decoration.",
        "Use whitespace to create hierarchy and confidence.",
        "Use purposeful motion to support comprehension, not distraction.",
        "Keep interactions fast, obvious, and accessible.",
        "Make public pages feel premium while keeping admin surfaces operationally efficient.",
    ]:
        body.append(p(item, num_id=1))

    body.append(p("3. Design Principles", style="Heading1"))
    for item in [
        "Minimalistic interface",
        "Large rounded corners from 16px to 32px",
        "Consistent spacing using an 8px grid",
        "Soft gradients and thin borders where useful",
        "Subtle shadows with high readability",
        "Mobile-first responsiveness",
        "Smooth animations and fast interactions",
        "Accessible color contrast",
    ]:
        body.append(p(item, num_id=1))

    body.append(page_break())
    body.append(p("4. Design System Workflow", style="Heading1"))
    body.append(p("The design system should begin with brand-level decisions, then flow into reusable tokens, components, page sections, portals, and quality checks."))
    body.append(image_paragraph("rIdImage1", "Design System Workflow", "Design system workflow diagram", 1))

    body.append(p("5. Color System", style="Heading1"))
    body.append(table([
        ["Category", "Tokens"],
        ["Primary Brand", "Smart Orange #FF7A00; Deep Orange #F97316"],
        ["Secondary", "Electric Blue #2563EB; Emerald Green #22C55E; Purple #8B5CF6"],
        ["Neutral", "White #FFFFFF; Off White #FAFAFA; Light Gray #F3F4F6; Border Gray #E5E7EB; Medium Gray #6B7280; Dark Gray #374151; Black #111827"],
        ["Status", "Success Green; Warning Amber; Error Red; Info Blue; Live Match Bright Red"],
    ], [2500, 6860]))

    body.append(p("6. Typography", style="Heading1"))
    body.append(table([
        ["Role", "Specification"],
        ["Primary Font", "Inter"],
        ["Fallbacks", "System UI, Helvetica Neue, Arial"],
        ["Hero", "64px to 72px"],
        ["Section Heading", "48px to 56px"],
        ["Page Heading", "36px to 42px"],
        ["Card Title", "24px"],
        ["Body", "16px to 18px"],
        ["Caption", "14px"],
        ["Small", "12px"],
    ], [2500, 6860]))

    body.append(p("7. Iconography and Spacing", style="Heading1"))
    body.append(p("Use Lucide React icons throughout the application. Icons should use an outline style, consistent stroke width, rounded appearance, and scalable sizing."))
    body.append(p("The spacing scale should include 4px, 8px, 12px, 16px, 24px, 32px, 40px, 48px, 64px, 80px, 96px, and 128px. Every page should maintain consistent spacing."))

    body.append(p("8. Component Design", style="Heading1"))
    body.append(table([
        ["Component", "Requirements"],
        ["Buttons", "Primary orange with white text, pill radius, hover animation, shadow, secondary border variant, ghost variant, danger, success, and loading states."],
        ["Cards", "White background, large radius, thin border, soft shadow, and subtle hover lift."],
        ["Forms", "Rounded inputs, focus ring, icons, validation, password toggle, helper text, and error messages."],
        ["Tables", "Rounded container, sticky header, search, pagination, sorting, filtering, bulk selection, and export."],
        ["Modals", "Blur background, rounded panel, keyboard support, ESC close, and animation."],
        ["Toast Notifications", "Top-right placement, animated entry, auto-dismiss behavior, and variants for success, warning, error, and info."],
    ], [2200, 7160]))

    body.append(p("9. Responsive Breakpoints and Motion", style="Heading1"))
    body.append(p("The frontend should support mobile, tablet, laptop, desktop, and ultra-wide layouts. Every component must adapt automatically."))
    body.append(p("Use Framer Motion for fade, slide, scale, stagger, hover, and page transition animations. Cards should animate naturally and avoid distracting movement."))

    body.append(page_break())
    body.append(p("10. Landing Page Architecture", style="Heading1"))
    body.append(p("The homepage should behave like a premium SaaS landing page while clearly expressing the sports tournament identity of Smart Sportz."))
    body.append(image_paragraph("rIdImage2", "Landing Page Architecture", "Landing page architecture diagram", 2))

    body.append(p("11. Landing Page Sections", style="Heading1"))
    body.append(table([
        ["Section", "Specification"],
        ["Floating Navigation", "Sticky rounded navigation with logo, Home, Live Tournament, Tournaments, Sports, Gallery, About, Contact, Admin Login, and Register Tournament CTA."],
        ["Hero Banner", "Full viewport hero with sports-tech gradient background, headline, subheading, primary CTA, secondary CTA, and floating dashboard preview."],
        ["Live Tournament Ticker", "Continuous scrolling ticker for live matches such as Basketball Finals, Cricket League, Football Championship, Chess Open, and Volleyball Semi-Finals."],
        ["Featured Tournaments", "Responsive cards with banner, sport icon, title, date, venue, registration deadline, entry fee, prize pool, register button, and view details action."],
        ["Sports Categories", "Interactive cards for Cricket, Football, Basketball, Volleyball, Badminton, Chess, Tennis, Kabaddi, Hockey, and Athletics."],
        ["Platform Features", "Six premium cards for Live Scores, Instant Registration, Online Payments, Auto Fixtures, Leaderboards, and Analytics."],
        ["Statistics", "Animated counters for active tournaments, registered teams, players, live matches, organizations, and visitors."],
        ["How It Works", "Timeline with Create Tournament, Register Teams, Play Matches, and View Live Results."],
    ], [2400, 6960]))
    body.append(table([
        ["Section", "Specification"],
        ["Upcoming Events", "Large carousel with banner, countdown, registration status, sport, venue, and register button."],
        ["Sponsors", "Auto-scrolling sponsor logos grouped into Platinum, Gold, and Silver."],
        ["Gallery", "Masonry layout for photos, videos, and event highlights with lightbox support."],
        ["Testimonials", "Slider containing organizer, coach, and player reviews with profile photo, name, role, rating, and review."],
        ["FAQ", "Accordion covering registration, payments, live scores, refunds, and rules."],
        ["Newsletter", "Simple email subscription form with validation."],
        ["Contact", "Address, phone, email, social links, embedded map, and contact form."],
        ["Footer", "Company, products, support, legal, social media, privacy policy, terms, refund policy, cookies, and copyright."],
    ], [2400, 6960]))

    body.append(page_break())
    body.append(p("12. Admin and Management Dashboard Design", style="Heading1"))
    body.append(p("Admin and management portals should share the same interface language, while optimizing each portal for its role-specific workflow."))
    body.append(image_paragraph("rIdImage3", "Dashboard UI Structure", "Dashboard UI structure diagram", 3))

    body.append(p("Admin Portal Design Language", style="Heading2"))
    for item in [
        "Left collapsible sidebar",
        "Sticky top navigation",
        "Dashboard widgets and KPI cards",
        "Interactive charts and modern tables",
        "Breadcrumb navigation",
        "Notification center",
        "User profile menu",
    ]:
        body.append(p(item, num_id=1))

    body.append(p("Management Dashboard Design", style="Heading2"))
    for item in [
        "Assigned tournaments",
        "Live match controls",
        "Pending actions",
        "Match schedule",
        "Notifications",
        "Quick actions",
        "Performance widgets",
    ]:
        body.append(p(item, num_id=1))

    body.append(p("13. Common UI Component Library", style="Heading1"))
    components = [
        "Buttons, inputs, selects, date pickers, time pickers, file uploads, and image cropper",
        "Cards, tables, pagination, tabs, accordions, drawers, modals, tooltips, badges, and chips",
        "Breadcrumbs, skeleton loaders, empty states, error states, success messages, charts, calendar, and timeline",
        "Avatar, dropdown menu, notification bell, command palette, and search bar",
    ]
    for item in components:
        body.append(p(item, num_id=1))
    body.append(rich_callout("Component Requirement", [
        "Every reusable component must support both dark mode and light mode, accessible states, responsive behavior, and predictable keyboard interaction."
    ]))

    body.append(p("14. Frontend AI Coding Instructions", style="Heading1"))
    for item in [
        "Use React 19, Vite, and TypeScript.",
        "Style exclusively with Tailwind CSS.",
        "Build every section as an independent reusable component.",
        "Ensure WCAG accessibility compliance.",
        "Optimize for performance with lazy loading, code splitting, and image optimization.",
        "Include loading, error, and empty states.",
        "Add smooth Framer Motion animations.",
        "Use semantic HTML and ARIA attributes.",
        "Maintain consistent spacing, typography, and component behavior across the application.",
    ]:
        body.append(p(item, num_id=1))

    body.append(rich_callout("Phase 2 Completion Criteria", [
        "Phase 2 is complete when the design language, landing-page structure, shared component expectations, dashboard layout direction, responsive behavior, and frontend generation rules are clear enough to guide implementation."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase2_design_system_workflow.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase2_landing_page_architecture.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase2_dashboard_layout.png"/>
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
  <dc:title>Smart Sportz - Phase 2 Design System and Landing Page Specification</dc:title>
  <dc:subject>UI/UX design language, landing page structure, and reusable component specification</dc:subject>
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
        "word/media/phase2_design_system_workflow.png": ASSET_DIR / "phase2_design_system_workflow.png",
        "word/media/phase2_landing_page_architecture.png": ASSET_DIR / "phase2_landing_page_architecture.png",
        "word/media/phase2_dashboard_layout.png": ASSET_DIR / "phase2_dashboard_layout.png",
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
