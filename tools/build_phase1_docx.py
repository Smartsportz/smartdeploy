from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


OUT = Path("docs/Smart_Sportz_Phase_1_Foundation.docx")

NS_W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def x(text: object) -> str:
    return escape(str(text), {'"': "&quot;"})


def tag(name: str, attrs: dict[str, object] | None = None, body: str = "") -> str:
    attrs = attrs or {}
    attr_text = "".join(f' {k}="{x(v)}"' for k, v in attrs.items())
    return f"<{name}{attr_text}>{body}</{name}>"


def empty(name: str, attrs: dict[str, object] | None = None) -> str:
    attrs = attrs or {}
    attr_text = "".join(f' {k}="{x(v)}"' for k, v in attrs.items())
    return f"<{name}{attr_text}/>"


def r(text: str, bold: bool = False, italic: bool = False, color: str | None = None,
      size: int | None = None, font: str | None = None, break_before: bool = False) -> str:
    props = []
    if bold:
        props.append(empty("w:b"))
    if italic:
        props.append(empty("w:i"))
    props.append(empty("w:color", {"w:val": color or "auto"}))
    if size:
        props.append(empty("w:sz", {"w:val": size * 2}))
        props.append(empty("w:szCs", {"w:val": size * 2}))
    props.append(empty("w:rFonts", {"w:ascii": font or "Times New Roman", "w:hAnsi": font or "Times New Roman", "w:cs": font or "Times New Roman"}))
    rpr = tag("w:rPr", body="".join(props)) if props else ""
    br = empty("w:br") if break_before else ""
    preserve = " xml:space=\"preserve\"" if text.startswith(" ") or text.endswith(" ") else ""
    return f"<w:r>{rpr}{br}<w:t{preserve}>{x(text)}</w:t></w:r>"


def p(text: str = "", style: str | None = None, align: str | None = None,
      before: int | None = None, after: int | None = None, keep_next: bool = False,
      num_id: int | None = None, ilvl: int = 0, runs: list[str] | None = None,
      border_bottom: bool = False, page_break_before: bool = False) -> str:
    props = []
    if style:
        props.append(empty("w:pStyle", {"w:val": style}))
    if keep_next:
        props.append(empty("w:keepNext"))
    if page_break_before:
        props.append(empty("w:pageBreakBefore"))
    if num_id is not None:
        props.append(tag("w:numPr", body=empty("w:ilvl", {"w:val": ilvl}) + empty("w:numId", {"w:val": num_id})))
    spacing_attrs = {}
    if before is not None:
        spacing_attrs["w:before"] = before
    if after is not None:
        spacing_attrs["w:after"] = after
    if spacing_attrs:
        props.append(empty("w:spacing", spacing_attrs))
    if align:
        props.append(empty("w:jc", {"w:val": align}))
    if border_bottom:
        props.append(tag("w:pBdr", body=empty("w:bottom", {
            "w:val": "single", "w:sz": "8", "w:space": "1", "w:color": "000000"
        })))
    ppr = tag("w:pPr", body="".join(props)) if props else ""
    body = "".join(runs) if runs is not None else (r(text) if text else "")
    return f"<w:p>{ppr}{body}</w:p>"


def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def cell(text: str | list[str], width: int, fill: str | None = None,
         bold: bool = False, align: str | None = None, color: str | None = None) -> str:
    tc_pr = [
        empty("w:tcW", {"w:w": width, "w:type": "dxa"}),
        tag("w:tcMar", body="".join([
            empty("w:top", {"w:w": "100", "w:type": "dxa"}),
            empty("w:left", {"w:w": "120", "w:type": "dxa"}),
            empty("w:bottom", {"w:w": "100", "w:type": "dxa"}),
            empty("w:right", {"w:w": "120", "w:type": "dxa"}),
        ])),
        empty("w:vAlign", {"w:val": "center"}),
    ]
    if fill:
        tc_pr.append(empty("w:shd", {"w:fill": fill}))
    paragraphs: list[str] = []
    if isinstance(text, list):
        for item in text:
            paragraphs.append(p(runs=[r(item, bold=bold, color=color)], after=60, align=align))
    else:
        paragraphs.append(p(runs=[r(text, bold=bold, color=color)], after=0, align=align))
    return tag("w:tc", body=tag("w:tcPr", body="".join(tc_pr)) + "".join(paragraphs))


def table(rows: list[list[str | list[str]]], widths: list[int], header: bool = True,
          fill: str = "FFFFFF") -> str:
    grid = tag("w:tblGrid", body="".join(empty("w:gridCol", {"w:w": w}) for w in widths))
    borders = tag("w:tblBorders", body="".join([
        empty(f"w:{side}", {"w:val": "single", "w:sz": "4", "w:space": "0", "w:color": "000000"})
        for side in ("top", "left", "bottom", "right", "insideH", "insideV")
    ]))
    tbl_pr = tag("w:tblPr", body="".join([
        empty("w:tblW", {"w:w": "9360", "w:type": "dxa"}),
        empty("w:tblInd", {"w:w": "120", "w:type": "dxa"}),
        empty("w:tblLayout", {"w:type": "fixed"}),
        borders,
        tag("w:tblCellMar", body="".join([
            empty("w:top", {"w:w": "80", "w:type": "dxa"}),
            empty("w:left", {"w:w": "120", "w:type": "dxa"}),
            empty("w:bottom", {"w:w": "80", "w:type": "dxa"}),
            empty("w:right", {"w:w": "120", "w:type": "dxa"}),
        ])),
    ]))
    tr_xml = []
    for idx, row in enumerate(rows):
        is_header = idx == 0 and header
        tr_pr = tag("w:trPr", body=empty("w:tblHeader")) if is_header else ""
        cells = "".join(cell(value, widths[i], fill if is_header else None, bold=is_header) for i, value in enumerate(row))
        tr_xml.append(tag("w:tr", body=tr_pr + cells))
    return tag("w:tbl", body=tbl_pr + grid + "".join(tr_xml))


def callout(title: str, body: list[str]) -> str:
    content = [p(runs=[r(title, bold=True, color="1F4D78")], after=80)]
    for line in body:
        content.append(p(line, after=60))
    return table([[content_to_text(content)]], [9360], header=False, fill="F4F6F9")


def content_to_text(_content: list[str]) -> str:
    # Placeholder holder for API compatibility is intentionally unused.
    # Callouts are built with a dedicated richer helper below.
    return ""


def rich_callout(title: str, lines: list[str]) -> str:
    tc_pr = tag("w:tcPr", body="".join([
        empty("w:tcW", {"w:w": "9360", "w:type": "dxa"}),
        tag("w:tcMar", body="".join([
            empty("w:top", {"w:w": "160", "w:type": "dxa"}),
            empty("w:left", {"w:w": "180", "w:type": "dxa"}),
            empty("w:bottom", {"w:w": "140", "w:type": "dxa"}),
            empty("w:right", {"w:w": "180", "w:type": "dxa"}),
        ])),
        empty("w:shd", {"w:fill": "F4F6F9"}),
    ]))
    body = p(runs=[r(title, bold=True, color="auto")], after=80)
    for line in lines:
        body += p(line, after=60)
    return tag("w:tbl", body="".join([
        tag("w:tblPr", body="".join([
            empty("w:tblW", {"w:w": "9360", "w:type": "dxa"}),
            empty("w:tblInd", {"w:w": "120", "w:type": "dxa"}),
            empty("w:tblLayout", {"w:type": "fixed"}),
            tag("w:tblBorders", body="".join([
                empty(f"w:{side}", {"w:val": "single", "w:sz": "4", "w:space": "0", "w:color": "000000"})
                for side in ("top", "left", "bottom", "right", "insideH", "insideV")
            ])),
        ])),
        tag("w:tblGrid", body=empty("w:gridCol", {"w:w": "9360"})),
        tag("w:tr", body=tag("w:tc", body=tc_pr + body)),
    ]))


def style_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{NS_W}">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="auto"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:b/><w:sz w:val="52"/><w:szCs w:val="52"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="240" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:b/><w:sz w:val="26"/><w:szCs w:val="26"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:keepNext/><w:spacing w:before="160" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="SmallMuted">
    <w:name w:val="Small Muted"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="20"/><w:szCs w:val="20"/><w:color w:val="auto"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock">
    <w:name w:val="Code Block"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="auto"/></w:rPr>
  </w:style>
</w:styles>'''


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
  <w:abstractNum w:abstractNumId="2">
    <w:multiLevelType w:val="hybridMultilevel"/>
    <w:lvl w:ilvl="0">
      <w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/>
      <w:lvlJc w:val="left"/>
      <w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    </w:lvl>
  </w:abstractNum>
  <w:num w:numId="2"><w:abstractNumId w:val="2"/></w:num>
</w:numbering>'''


def header_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="{NS_W}" xmlns:r="{NS_R}">
  <w:p>
    <w:pPr><w:jc w:val="right"/><w:spacing w:after="0"/></w:pPr>
    {r("Smart Sportz - Phase 1 Foundation", color="6B7280", size=9)}
  </w:p>
</w:hdr>'''


def footer_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="{NS_W}" xmlns:r="{NS_R}">
  <w:p>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="0"/></w:pPr>
    {r("Smart Sportz | Enterprise Sports Tournament Management Platform | Page ", color="6B7280", size=9)}
    <w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>'''


def document_xml() -> str:
    body: list[str] = []

    body.append(p("PHASE 1 - FOUNDATION", style="Title"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Sports Tournament & Facility Management Platform", style="Heading2", after=0))
    body.append(table([
        ["Document", "Phase 1 Foundation Brief"],
        ["Project", "Smart Sportz"],
        ["Product Category", "Enterprise Sports Tournament and Event Management Platform"],
        ["Platform Type", "Multi-role SaaS web application"],
        ["Prepared For", "Product architecture, UI/UX design, backend engineering, database design, DevOps, security, and QA planning"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p("", after=0, border_bottom=True))
    body.append(rich_callout("Foundation Intent", [
        "This document defines the Phase 1 foundation for Smart Sportz. It converts the raw project idea into a structured architecture brief that can guide future production implementation.",
        "Phase 1 does not build the product. It establishes product scope, engineering roles, platform principles, target users, modules, technology choices, system architecture, non-functional requirements, and coding standards."
    ]))

    body.append(page_break())
    body.append(p("1. AI Role and Responsibilities", style="Heading1"))
    body.append(p("The AI should act as an elite cross-functional software engineering and product team with enterprise delivery experience. The expected perspective combines architecture, engineering, design, security, DevOps, QA, performance, and sports tournament domain knowledge."))
    body.append(p("Required expert roles", style="Heading2"))
    roles = [
        "Principal Software Architect",
        "Senior Full Stack Engineer",
        "React.js Architect",
        "Node.js Enterprise Backend Architect",
        "PostgreSQL Database Architect",
        "DevOps Engineer",
        "UI/UX Designer",
        "Product Designer",
        "Security Engineer",
        "Cloud Architect",
        "QA Automation Engineer",
        "Performance Engineer",
        "Sports Tournament Domain Expert",
    ]
    for item in roles:
        body.append(p(item, num_id=1))
    body.append(rich_callout("Delivery Standard", [
        "Every future feature should be designed as production-ready enterprise software. The implementation standard should avoid placeholder architecture, incomplete components, mock implementations, TODO comments, and temporary flows."
    ]))

    body.append(p("2. Project Overview", style="Heading1"))
    body.append(table([
        ["Field", "Definition"],
        ["Project Name", "Smart Sportz"],
        ["Product Category", "Sports Tournament and Event Management Platform"],
        ["Platform Type", "Multi-role SaaS web application"],
        ["Supported Devices", "Desktop, laptop, tablet, mobile, and Smart TV live score display"],
        ["Primary Users", "Sports organizations, schools, colleges, academies, clubs, corporate event teams, associations, federations, and private organizers"],
    ], [2400, 6960]))
    body.append(p("Primary purpose", style="Heading2"))
    body.append(p("Smart Sportz is a centralized platform that allows sports organizations, educational institutions, academies, clubs, associations, federations, and private organizers to create, manage, and broadcast sports tournaments in real time."))
    body.append(p("Tournament lifecycle coverage", style="Heading2"))
    lifecycle = [
        "Tournament creation and publishing",
        "Registration and team or player onboarding",
        "Online payment collection",
        "Fixture generation",
        "Live match management",
        "Live score updates",
        "Results, leaderboards, and certificates",
        "Reports, notifications, and website CMS management",
    ]
    for item in lifecycle:
        body.append(p(item, num_id=1))

    body.append(p("3. Product Goals and Business Objectives", style="Heading1"))
    body.append(p("Product goals", style="Heading2"))
    goals = [
        "Create unlimited tournaments across multiple sports.",
        "Support large-scale registrations and payment workflows.",
        "Manage live scoring and real-time tournament broadcasting.",
        "Automate fixtures and tournament progression where possible.",
        "Generate reports, certificates, leaderboards, and results.",
        "Control users, roles, and permissions through enterprise RBAC.",
        "Remain future-ready for multi-organization scaling.",
    ]
    for item in goals:
        body.append(p(item, num_id=1))
    body.append(p("Business objectives", style="Heading2"))
    objectives = [
        "Reduce manual tournament administration.",
        "Enable online registrations and digital payments.",
        "Improve organizer efficiency and operational visibility.",
        "Increase spectator engagement through live score tracking.",
        "Offer a polished digital experience for teams, players, and audiences.",
        "Support revenue through registration fees and sponsorship visibility.",
    ]
    for item in objectives:
        body.append(p(item, num_id=1))

    body.append(p("4. Target Users and Supported Sports", style="Heading1"))
    body.append(table([
        ["Target Segment", "Examples"],
        ["Education", "Schools, colleges, and universities"],
        ["Training and Clubs", "Sports academies, local clubs, and private coaching groups"],
        ["Events", "Corporate sports events and private tournament organizers"],
        ["Associations", "District, state, and national sports associations"],
        ["Government", "Government sports departments and public sports bodies"],
        ["Federations", "Large sports federations and league organizers"],
    ], [2600, 6760]))
    body.append(p("Default sports", style="Heading2"))
    sports = "Cricket, Football, Basketball, Volleyball, Badminton, Chess, Tennis, Table Tennis, Kabaddi, Hockey, Handball, Athletics, Throwball, Carrom, and Kho Kho."
    body.append(p(sports))
    body.append(rich_callout("Extensibility Requirement", [
        "The platform must support unlimited sports. A Super Admin should be able to add new sports without code changes."
    ]))

    body.append(p("5. Core Enterprise Modules", style="Heading1"))
    body.append(table([
        ["Area", "Modules"],
        ["Public Experience", "Landing Website, Public Tournament Portal, Live Tournament Portal, Gallery, Sponsors, CMS"],
        ["Tournament Operations", "Tournament Registration, Team Management, Player Management, Venue Management, Fixture Generator, Match Management, Results Management, Leaderboards"],
        ["Commercial", "Payment Gateway, Sponsorship visibility, Receipts and financial reports"],
        ["Administration", "Authentication, Role and Permission Management, Reports, Notifications, Audit Logs, Settings"],
        ["Real Time", "Live Score Engine, live match status, audience updates, and tournament monitor views"],
    ], [2200, 7160]))

    body.append(p("6. User Roles and RBAC", style="Heading1"))
    body.append(p("The platform must implement Azure-style Role-Based Access Control. Permissions should be assignable at a granular level and scoped to tournaments, sports, venues, and modules where applicable."))
    body.append(table([
        ["Role", "Scope", "Responsibilities"],
        ["Super Admin", "Highest privilege", "Create organizations, create tournaments, manage users, assign permissions, publish tournaments, manage payments, manage CMS, generate reports, monitor live matches, and configure settings."],
        ["Management User", "Assigned tournaments and granted permissions", "Manage assigned tournaments, start or pause or end matches, update live scores, verify teams and players, publish announcements, and upload results."],
        ["Public User", "No login required for browsing", "View tournaments, register, pay fees, view live matches, track scores, view schedules, and download results."],
    ], [1800, 2300, 5260]))
    body.append(p("Management User restriction", style="Heading2"))
    body.append(p("A Management User must not access global platform settings unless the Super Admin explicitly grants the relevant permission."))

    body.append(p("7. System Principles", style="Heading1"))
    principles = [
        "Modular architecture",
        "Reusable components",
        "SOLID principles",
        "Clean Architecture",
        "Repository Pattern",
        "Service Layer Pattern",
        "RESTful APIs",
        "Responsive design",
        "Accessibility aligned with WCAG",
        "Secure by default",
        "High performance",
    ]
    for item in principles:
        body.append(p(item, num_id=1))

    body.append(page_break())
    body.append(p("8. Technology Stack", style="Heading1"))
    body.append(table([
        ["Layer", "Selected Technologies"],
        ["Frontend", "React 19+, Vite, TypeScript, Tailwind CSS, Framer Motion, Redux Toolkit, TanStack Query, React Router, React Hook Form, Zod, Recharts, TanStack Table, Lucide Icons, Sonner, Day.js"],
        ["Backend", "Node.js LTS, Express.js, TypeScript, JWT, refresh tokens, Zod, Multer, Socket.IO, OpenAPI or Swagger, Winston, Redis, Node Cron"],
        ["Database", "PostgreSQL, Prisma ORM, Prisma Migrate"],
        ["Storage", "AWS S3 with Cloudinary as an alternative"],
        ["Payment", "Razorpay, future-ready for Stripe and PayPal"],
        ["Notifications", "Email, SMS, WhatsApp, and push notifications"],
        ["Deployment", "Docker, Docker Compose, Nginx, PM2, Ubuntu Linux"],
    ], [1900, 7460]))

    body.append(p("9. High-Level System Architecture", style="Heading1"))
    body.append(p("The Phase 1 architecture separates the public frontend, backend API, real-time Socket.IO layer, service modules, database, cache, storage, payment, and notification providers."))
    architecture_lines = [
        "Internet",
        "  -> Nginx Reverse Proxy",
        "      -> React Frontend",
        "      -> Express Backend",
        "          -> Authentication Service",
        "          -> RBAC Service",
        "          -> Tournament Service",
        "          -> Registration Service",
        "          -> Payment Service",
        "          -> Notification Service",
        "          -> Live Score Service",
        "          -> Socket.IO Server",
        "          -> Report Service",
        "              -> PostgreSQL Database",
        "              -> Redis Cache",
        "              -> AWS S3 or Cloudinary",
        "              -> Razorpay API",
        "              -> Email, SMS, WhatsApp, and Push providers",
    ]
    for line in architecture_lines:
        body.append(p(line, style="CodeBlock", after=20))

    body.append(p("10. Non-Functional Requirements", style="Heading1"))
    nfr = [
        "Fast page loading with a target below 2 seconds for core public pages.",
        "Responsive layouts across desktop, laptop, tablet, mobile, and live display screens.",
        "Secure authentication and enterprise-grade RBAC.",
        "Real-time synchronization for live scoring and match updates.",
        "Scalable architecture for large tournaments and future multi-organization growth.",
        "Maintainable codebase with clear separation of concerns.",
        "Accessibility support and SEO-friendly public pages.",
        "High availability, observability, and fault-tolerant deployment design.",
    ]
    for item in nfr:
        body.append(p(item, num_id=1))

    body.append(p("11. Coding Standards", style="Heading1"))
    standards = [
        "Use TypeScript throughout frontend and backend.",
        "Follow ESLint and Prettier conventions.",
        "Build reusable components and avoid duplicated logic.",
        "Keep business logic out of UI components.",
        "Use feature-based folder organization.",
        "Separate controllers, services, repositories, and models.",
        "Include proper error handling, validation, and authorization checks.",
        "Provide loading, empty, and error states for every page.",
        "Use environment variables for secrets and deployment configuration.",
        "Write clear, maintainable, and documented code.",
    ]
    for item in standards:
        body.append(p(item, num_id=1))

    body.append(p("12. Phase 1 Deliverables", style="Heading1"))
    body.append(table([
        ["Deliverable", "Purpose"],
        ["Foundation Architecture Brief", "Define product scope, roles, modules, stack, principles, and quality expectations."],
        ["Technology Baseline", "Confirm frontend, backend, database, real-time, payment, notification, and deployment technologies."],
        ["RBAC Baseline", "Define role boundaries and permission-driven access control expectations."],
        ["System Architecture Direction", "Set the target high-level structure for frontend, backend, services, database, cache, storage, and external providers."],
        ["Engineering Standards", "Define code quality expectations before production implementation begins."],
    ], [3000, 6360]))
    body.append(rich_callout("Phase 1 Completion Criteria", [
        "Phase 1 is complete when the project foundation is clear enough to guide detailed database design, API planning, UI/UX system design, folder structure, and implementation planning in later phases."
    ]))

    page_borders = tag("w:pgBorders", {"w:offsetFrom": "page"}, body="".join([
        empty("w:top", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
        empty("w:left", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
        empty("w:bottom", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
        empty("w:right", {"w:val": "single", "w:sz": "4", "w:space": "24", "w:color": "auto"}),
    ]))
    sect_pr = tag("w:sectPr", body="".join([
        empty("w:pgSz", {"w:w": "11906", "w:h": "16838"}),
        empty("w:pgMar", {"w:top": "720", "w:right": "720", "w:bottom": "720", "w:left": "720", "w:header": "720", "w:footer": "720", "w:gutter": "0"}),
        page_borders,
        empty("w:cols", {"w:space": "720"}),
        empty("w:docGrid", {"w:linePitch": "360"}),
    ]))
    body.append(sect_pr)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{NS_W}" xmlns:r="{NS_R}">
  <w:body>
    {''.join(body)}
  </w:body>
</w:document>'''


def content_types_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
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
  <w:font w:name="Calibri"><w:family w:val="swiss"/><w:pitch w:val="variable"/></w:font>
  <w:font w:name="Consolas"><w:family w:val="modern"/><w:pitch w:val="fixed"/></w:font>
  <w:font w:name="Symbol"><w:family w:val="roman"/><w:pitch w:val="variable"/></w:font>
</w:fonts>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Phase 1 Foundation</dc:title>
  <dc:subject>Enterprise sports tournament management platform foundation brief</dc:subject>
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
    print(OUT.resolve())


if __name__ == "__main__":
    build()
