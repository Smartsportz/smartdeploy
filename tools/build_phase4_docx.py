from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, page_break, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_4_Registration_Payment_System.docx")
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

    body.append(p("PHASE 4 - TOURNAMENT REGISTRATION & PAYMENT SYSTEM", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Registration, Payments & Participant Management", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 4 Tournament Registration and Payment System"],
        ["Project", "Smart Sportz"],
        ["Focus", "Individual/team registration, tournament configuration, Razorpay payments, approvals, waitlists, refunds, receipts, notifications, dashboards, and audit logs"],
        ["Reference Style", "Same spacing, alignment, borders, margins, and black document treatment as the approved Phase 1 document"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 4 Intent", [
        "This document defines the Smart Sportz registration and payment system. It turns the registration/payment prompt into a structured module specification for future frontend, backend, database, payment, notification, and admin-dashboard implementation.",
        "The module must be configurable so different tournaments can use different registration rules without code changes."
    ]))

    body.append(p("1. Module Objective", style="Heading1"))
    body.append(p("Build a complete, secure, and scalable registration system that supports participant onboarding, online payments, approval workflows, waitlists, refunds, receipts, invoices, and audit trails."))
    body.extend(bullets([
        "Support individual player registrations, team registrations, and hybrid registration modes.",
        "Support multiple tournament categories and tournament-specific registration settings.",
        "Integrate Razorpay for secure payments and webhook verification.",
        "Support coupons, discounts, refunds, automated receipts, and invoices.",
        "Provide role-based admin approval and refund controls.",
    ]))

    body.append(p("2. Registration Types", style="Heading1"))
    body.append(table([
        ["Mode", "Use Cases"],
        ["Individual Registration", "Chess, Athletics, Table Tennis, Tennis, and Badminton Singles."],
        ["Team Registration", "Cricket, Football, Basketball, Volleyball, Kabaddi, Hockey, and other team sports."],
        ["Hybrid Registration", "Allows both individual and team registration when enabled by the organizer."],
    ], [2600, 6760]))

    body.append(p("3. Tournament Configuration", style="Heading1"))
    body.append(table([
        ["Configuration Area", "Fields"],
        ["Basic Information", "Tournament name, sport, organizer, venue, dates, registration window, maximum teams, maximum players, team size limits, age category, and gender category."],
        ["Registration Settings", "Individual/team/hybrid mode, approval required, auto approve, waitlist, late registration, ID verification, team logo, medical certificate, and parent consent for minors."],
        ["Payment Settings", "Entry fee, currency, GST/tax, coupon support, early bird discount, refund policy, and payment deadline."],
    ], [2600, 6760]))

    body.append(page_break())
    body.append(p("4. Registration Lifecycle", style="Heading1"))
    body.append(p("The public registration lifecycle starts with tournament configuration and moves through registration, document collection, review, payment or approval, capacity handling, and confirmation."))
    body.append(image_paragraph("rIdImage1", "Registration Lifecycle", "Registration lifecycle diagram", 1))

    body.append(p("5. Team Registration Form", style="Heading1"))
    body.append(table([
        ["Group", "Fields"],
        ["Team Details", "Team name, team logo, team short name, coach, manager, captain, vice captain, team email, team phone, organization or club, district, state, and country."],
        ["Team Address", "Address line 1, address line 2, city, state, and postal code."],
        ["Team Documents", "Team logo, authorization letter, and optional registration certificate."],
    ], [2400, 6960]))

    body.append(p("6. Player Details", style="Heading1"))
    body.append(p("Each team registration should allow players to be added dynamically. The interface should support drag-and-drop reordering and bulk import from Excel or CSV."))
    body.extend(bullets([
        "Player photo, full name, jersey number, date of birth, age, gender, and position.",
        "Mobile number, email, Aadhaar or passport where applicable, emergency contact, blood group, and optional medical notes.",
        "Validation should enforce tournament-specific player limits and required fields.",
    ]))

    body.append(p("7. Individual Registration Form", style="Heading1"))
    body.append(p("Individual registration should collect full name, photo, gender, date of birth, sport, category, email, mobile, address, city, state, country, emergency contact, ID proof upload, and consent checkbox."))

    body.append(p("8. Document Management", style="Heading1"))
    body.extend(bullets([
        "Supported uploads: JPG, PNG, and PDF.",
        "Maximum file size should be configurable.",
        "Features: preview, replace, delete, cloud storage support, and future-ready virus scan integration.",
    ]))

    body.append(page_break())
    body.append(p("9. Payment Gateway", style="Heading1"))
    body.append(p("Integrate Razorpay for UPI, credit card, debit card, net banking, and wallet payments. Payment success must be confirmed only after secure webhook signature verification."))
    body.append(image_paragraph("rIdImage2", "Razorpay Payment and Webhook Flow", "Razorpay payment and webhook flow diagram", 2))

    body.append(p("10. Payment Statuses", style="Heading1"))
    body.append(p("Payment statuses should include Pending, Processing, Paid, Failed, Cancelled, Refunded, Partially Refunded, and Expired. Every status change must be recorded in the audit trail."))

    body.append(p("11. Coupons and Discounts", style="Heading1"))
    body.append(table([
        ["Discount Type", "Description"],
        ["Percentage Discount", "Percentage-based discount against eligible amount."],
        ["Fixed Amount Discount", "Flat discount amount."],
        ["Early Bird Pricing", "Date-bound reduced price before configured deadline."],
        ["Group Discount", "Discount based on team/player count or registration group size."],
        ["Promo Codes", "Code-based campaign discounts."],
    ], [2600, 6760]))
    body.append(p("Coupon configuration should include code, description, start date, end date, usage limit, minimum amount, and applicable tournaments."))

    body.append(page_break())
    body.append(p("12. Registration Approval, Waitlist, and Refund Workflow", style="Heading1"))
    body.append(p("When approval is enabled, admins can approve, reject, request additional documents, or put a registration on the waitlist. Refund management must support full, partial, manual, and future automated refunds."))
    body.append(image_paragraph("rIdImage3", "Approval, Waitlist, and Refund Workflow", "Approval waitlist and refund workflow diagram", 3))
    body.extend(bullets([
        "Approval actions should trigger notifications to participants.",
        "Waitlists should activate automatically when maximum capacity is reached.",
        "Participants should see current waitlist position where applicable.",
        "When slots become available, users should be promoted automatically where rules allow.",
        "Refund tracking should store reason, amount, processed by, status, and transaction ID.",
    ]))

    body.append(p("13. Receipts and Invoices", style="Heading1"))
    body.append(p("Generate registration receipts, tax invoices, and payment receipts. Documents should include QR code, invoice number, tournament details, participant details, payment details, organizer information, and PDF download support."))

    body.append(p("14. Notifications", style="Heading1"))
    body.append(p("Email, SMS, and WhatsApp notifications should be sent automatically for registration submitted, payment successful, payment failed, registration approved, registration rejected, waitlist updated, tournament reminder, fixture published, and match schedule updated. Templates should be editable by the Super Admin."))

    body.append(page_break())
    body.append(p("15. Admin Registration Dashboard", style="Heading1"))
    body.append(table([
        ["Widget / Area", "Purpose"],
        ["Total Registrations", "High-level count across selected tournament or platform scope."],
        ["Pending Approvals", "Queue requiring admin review."],
        ["Approved Participants", "Confirmed participants and teams."],
        ["Rejected Registrations", "Rejected entries with reasons."],
        ["Waitlisted Participants", "Capacity-based pending participants."],
        ["Revenue Collected", "Paid registration revenue."],
        ["Refund Requests", "Pending or processed refund queue."],
        ["Registration Trends", "Charts over time with export options."],
    ], [2600, 6760]))

    body.append(p("16. Registration Management Page", style="Heading1"))
    body.extend(bullets([
        "Search by participant, team, tournament, or payment ID.",
        "Advanced filters by status, sport, date, and payment.",
        "View full registration details and edit registration when permitted.",
        "Approve, reject, download documents, export CSV/Excel/PDF, and perform bulk actions.",
    ]))

    body.append(p("17. Audit Logs", style="Heading1"))
    body.append(p("Record every important action: registration created, registration updated, documents uploaded, payment initiated, payment verified, approval status changed, and refund processed. Store user, timestamp, IP address, action, previous value, and new value."))

    body.append(p("18. Registration and Payment Data Model", style="Heading1"))
    body.append(p("The module should keep registrations, participants, documents, payments, invoices, and audit logs consistent through transactional database operations."))
    body.append(image_paragraph("rIdImage4", "Registration and Payment Data Model", "Registration and payment data model diagram", 4))

    body.append(p("19. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Build reusable registration forms with React Hook Form and Zod validation.",
        "Support dynamic player lists for team registrations.",
        "Integrate Razorpay securely with backend webhook verification.",
        "Store uploaded files in Cloudinary or AWS S3.",
        "Generate PDF invoices and receipts.",
        "Use transactional database operations to avoid inconsistent payment states.",
        "Provide loading, success, error, and retry states.",
        "Implement role-based access so only authorized users can approve registrations or process refunds.",
        "Expose REST APIs for registration, payments, approvals, waitlists, and reports.",
        "Ensure all payment and registration events are logged for auditing.",
    ]))
    body.append(rich_callout("Phase 4 Completion Criteria", [
        "Phase 4 is complete when registration modes, tournament configuration, forms, documents, Razorpay flow, payment statuses, coupons, approvals, waitlists, receipts, notifications, dashboards, refunds, audit logs, and implementation rules are clear enough for development."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase4_registration_lifecycle.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase4_payment_webhook_flow.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase4_approval_waitlist_refund.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase4_registration_data_model.png"/>
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
  <dc:title>Smart Sportz - Phase 4 Registration and Payment System</dc:title>
  <dc:subject>Tournament registration, payment, approval, waitlist, refund, receipt, notification, and audit specification</dc:subject>
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
        "word/media/phase4_registration_lifecycle.png": ASSET_DIR / "phase4_registration_lifecycle.png",
        "word/media/phase4_payment_webhook_flow.png": ASSET_DIR / "phase4_payment_webhook_flow.png",
        "word/media/phase4_approval_waitlist_refund.png": ASSET_DIR / "phase4_approval_waitlist_refund.png",
        "word/media/phase4_registration_data_model.png": ASSET_DIR / "phase4_registration_data_model.png",
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
