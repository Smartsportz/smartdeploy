from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, page_break, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_3_Public_Website_Specification.docx")
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

    body.append(p("PHASE 3 - PUBLIC WEBSITE SPECIFICATION", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Public Website", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 3 Public Website Specification"],
        ["Project", "Smart Sportz"],
        ["Focus", "SEO-friendly public website, tournament discovery, registration, live scores, content pages, and public user experience"],
        ["Reference Style", "Same spacing, alignment, borders, margins, and black document treatment as the approved Phase 1 document"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 3 Intent", [
        "This document defines the public website for Smart Sportz. It turns the public-facing product idea into a structured website specification covering navigation, pages, live match viewing, registration, SEO, performance, and reusable frontend behavior.",
        "The public website must feel modern, fast, engaging, responsive, and optimized for both desktop and mobile visitors."
    ]))

    body.append(p("1. Public Website Objective", style="Heading1"))
    body.append(p("Build a premium, SEO-friendly, responsive public website that acts as the primary entry point for tournament discovery, team and player registration, live score viewing, sponsor visibility, organizer branding, event promotion, and online payments."))
    body.extend(bullets([
        "Help visitors discover live and upcoming tournaments quickly.",
        "Make registration and payment simple for teams and individuals.",
        "Expose live scores, fixtures, results, leaderboards, and match details.",
        "Support organizer branding, sponsor visibility, gallery content, news, and policies.",
        "Keep every page responsive, accessible, performant, and search-engine friendly.",
    ]))

    body.append(p("2. Public Website Information Architecture", style="Heading1"))
    body.append(p("The website should be organized around public discovery, live match access, registration, content, support, and global utilities such as search, breadcrumbs, SEO metadata, and newsletter conversion."))
    body.append(image_paragraph("rIdImage1", "Public Website Information Architecture", "Public website information architecture diagram", 1))
    body.append(table([
        ["Area", "Pages"],
        ["Discovery", "Home, Live Tournaments, Upcoming Tournaments, Tournament Details, Sports, Teams, Players"],
        ["Match Center", "Fixtures, Live Scores, Results, Leaderboards, Live Match Page"],
        ["Registration", "Team Registration, Individual Registration, Payment"],
        ["Content", "Gallery, Sponsors, News & Blogs, About Us"],
        ["Support", "Contact, FAQs, Privacy Policy, Terms & Conditions, Refund Policy, Cookie Policy, Disclaimer"],
    ], [2200, 7160]))

    body.append(p("3. Global Navigation and Components", style="Heading1"))
    body.append(p("Sticky navigation should remain visible during scrolling and provide fast access to the main public website areas."))
    body.extend(bullets([
        "Navigation items: Home, Live Tournament, Tournaments, Sports, Results, Gallery, About, and Contact.",
        "Right side actions: Search, optional notifications, Register Tournament, and Admin Login.",
        "Every public page should include sticky navigation, breadcrumbs, search, footer, CTA banner, newsletter, contact links, and social links.",
    ]))

    body.append(p("4. Home Page Specification", style="Heading1"))
    body.append(table([
        ["Section", "Requirements"],
        ["Hero Section", "Hero headline, subheading, CTA buttons, dashboard preview, and animated sports graphics."],
        ["Live Tournament Ticker", "Continuously scrolling live tournament items such as Basketball Finals, Cricket League, Football Cup, and Badminton Open. Each item links to the live match page."],
        ["Featured Tournament Carousel", "Cards with banner, sport, venue, date, registration status, entry fee, prize, register action, and view details action."],
        ["Sports Categories", "Interactive cards with image, icon, sport name, and active tournament count."],
        ["Statistics", "Animated counters for tournaments, teams, players, matches, and visitors."],
        ["Upcoming Events", "Large responsive carousel with countdown timer and register button."],
        ["Why Choose Smart Sportz", "Feature cards for live score, secure payments, easy registration, fast fixtures, reports, and analytics."],
        ["Trust and Content", "Sponsors, gallery, testimonials, FAQs, contact section, and footer."],
    ], [2400, 6960]))

    body.append(page_break())
    body.append(p("5. Registration and Payment Journey", style="Heading1"))
    body.append(p("The public registration flow should guide visitors from tournament discovery to validated registration, online payment, receipt generation, and post-registration follow-up."))
    body.append(image_paragraph("rIdImage2", "Public Registration and Payment Journey", "Public registration and payment journey diagram", 2))
    body.extend(bullets([
        "Visitors discover tournaments through search, filters, featured cards, and tournament details.",
        "Users choose tournament, sport, category, and team or individual registration type.",
        "Forms should support validation, document upload, loading states, empty states, error states, and success states.",
        "Payment should support Razorpay and related online payment methods.",
        "Confirmation should provide receipt, email status, and downstream tournament updates.",
    ]))

    body.append(p("6. Live Tournament Page", style="Heading1"))
    body.append(p("The Live Tournament page displays all currently running tournaments and should allow visitors to filter and open tournament-level live dashboards."))
    body.extend(bullets([
        "Top filters: sport, location, organization, and status.",
        "Each live tournament card should show banner, tournament name, sport, venue, live badge, and active match count.",
        "Clicking a card opens the tournament live dashboard.",
    ]))

    body.append(p("7. Live Match Page", style="Heading1"))
    body.append(p("The Live Match page is the most important public match-viewing surface. It should present match identity, scoreboard, timers, sport-specific statistics, timeline, commentary, match info, and standings."))
    body.append(image_paragraph("rIdImage3", "Live Match Page Experience", "Live match page experience diagram", 3))
    body.append(table([
        ["Area", "Requirements"],
        ["Header", "Tournament name, sport, venue, round, match number, and status."],
        ["Scoreboard", "Teams, score, VS layout, timer, and sport-dependent period such as quarter, overs, sets, or rounds."],
        ["Statistics", "Basketball: fouls, rebounds, assists. Football: possession, corners, yellow cards. Cricket: overs, wickets, run rate."],
        ["Timeline", "Chronological events such as goals, timeouts, three pointers, red cards, and wickets."],
        ["Commentary", "Live commentary feed with newest updates at the top."],
        ["Real Time", "Socket.IO-ready sections for automatic score and match status updates."],
    ], [2200, 7160]))

    body.append(page_break())
    body.append(p("8. Tournament Details Page", style="Heading1"))
    body.append(p("The Tournament Details page should provide everything needed to understand and enter a tournament."))
    body.extend(bullets([
        "Banner, description, rules, eligibility, schedule, venue, map, organizer, contacts, gallery, sponsors, downloads, and register button.",
        "Registration status, entry fee, and prize pool should be visible and easy to scan.",
        "The page should be SEO-ready and shareable through social previews.",
    ]))

    body.append(p("9. Directory and Match Pages", style="Heading1"))
    body.append(table([
        ["Page", "Requirements"],
        ["Sports Page", "Grid layout with image, description, active tournaments, upcoming tournaments, and view details action."],
        ["Team Directory", "Search and filters for sport, district, organization, and ranking. Cards show logo, team name, coach, captain, wins, losses, and details."],
        ["Player Directory", "Cards with photo, name, team, sport, age, position, achievements, and statistics."],
        ["Fixtures Page", "Calendar style with daily, weekly, monthly views and filters for venue, tournament, and sport."],
        ["Results Page", "Completed match cards showing winner, score, highlights, statistics, and download scorecard action."],
        ["Leaderboard", "Tournament leaderboard, overall leaderboard, team rankings, player rankings, and points table."],
    ], [2400, 6960]))

    body.append(p("10. Content and Support Pages", style="Heading1"))
    body.append(table([
        ["Page", "Requirements"],
        ["Gallery", "Masonry layout for images, videos, albums, event filtering, and lightbox preview."],
        ["Sponsors", "Grouped by Platinum, Gold, Silver, and Community with logo, website, and description."],
        ["News & Blogs", "Articles, announcements, tournament updates, search, categories, and share buttons."],
        ["About Us", "Mission, vision, story, team, partners, and achievements."],
        ["Contact", "Address, phone, email, map, inquiry form, social media, and support hours."],
        ["FAQ", "Accordion grouped by registration, payment, tournament rules, live scores, refund, and certificates."],
        ["Policies", "Privacy Policy, Terms & Conditions, Refund Policy, Cookie Policy, and Disclaimer."],
    ], [2400, 6960]))

    body.append(p("11. Search Experience", style="Heading1"))
    body.append(p("Global search should find tournaments, teams, players, matches, venues, organizers, and news. It should provide instant suggestions and keyboard navigation."))

    body.append(p("12. SEO and Performance Requirements", style="Heading1"))
    body.append(p("The public website must be discoverable, fast, and accessible. SEO and performance should be designed into every route, not added at the end."))
    body.append(image_paragraph("rIdImage4", "SEO and Performance Pipeline", "SEO and performance pipeline diagram", 4))
    body.append(table([
        ["Area", "Requirements"],
        ["SEO", "Unique page title, meta description, Open Graph tags, Twitter cards, structured JSON-LD data, canonical URL, XML sitemap, robots.txt, and image alt text."],
        ["Performance", "Lazy-load images, route-based code splitting, responsive images, skeleton loaders, important-route prefetching, asset compression, and static content caching."],
        ["Accessibility", "Semantic HTML, keyboard support, readable content hierarchy, useful labels, alt text, and accessible loading/error states."],
    ], [2200, 7160]))

    body.append(p("13. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Build each page as a reusable React route.",
        "Use React Router with nested layouts.",
        "Implement responsive behavior for mobile, tablet, and desktop.",
        "Use reusable components for cards, filters, badges, carousels, and forms.",
        "Ensure all live score sections are ready to receive Socket.IO updates.",
        "Provide proper loading, empty, and error states.",
        "Optimize pages for SEO and accessibility.",
        "Avoid duplicate UI patterns by creating shared component libraries.",
    ]))
    body.append(rich_callout("Phase 3 Completion Criteria", [
        "Phase 3 is complete when the public website page map, global navigation, home page, live match experience, registration/payment journey, public directories, content pages, search behavior, SEO, performance, and frontend implementation rules are clear enough for development."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase3_public_site_architecture.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase3_registration_payment_flow.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase3_live_match_experience.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase3_seo_performance_pipeline.png"/>
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
  <dc:title>Smart Sportz - Phase 3 Public Website Specification</dc:title>
  <dc:subject>Public website, live scores, registration, SEO, performance, and frontend route specification</dc:subject>
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
        "word/media/phase3_public_site_architecture.png": ASSET_DIR / "phase3_public_site_architecture.png",
        "word/media/phase3_registration_payment_flow.png": ASSET_DIR / "phase3_registration_payment_flow.png",
        "word/media/phase3_live_match_experience.png": ASSET_DIR / "phase3_live_match_experience.png",
        "word/media/phase3_seo_performance_pipeline.png": ASSET_DIR / "phase3_seo_performance_pipeline.png",
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
