from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from build_phase1_docx import empty, p, rich_callout, style_xml, table, tag
from build_phase2_docx import image_paragraph


OUT = Path("docs/Smart_Sportz_Phase_7_Live_Score_Engine_Match_Intelligence.docx")
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

    body.append(p("PHASE 7 - LIVE SCORE ENGINE & MATCH INTELLIGENCE", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - Real-Time Scoring, Match Intelligence & Analytics", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 7 Live Score Engine and Match Intelligence"],
        ["Project", "Smart Sportz"],
        ["Focus", "Universal event-driven live scoring, match lifecycle, sport adapters, timers, timelines, commentary, statistics, leaderboards, score corrections, Socket.IO communication, Redis caching, scalability, and error recovery"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved Phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 7 Intent", [
        "This document defines the Smart Sportz Live Score Engine and Match Intelligence layer. It converts the live scoring prompt into a structured specification for event-driven scoring, real-time broadcasting, sport-specific adapters, analytics, correction workflows, and scalable public live experiences.",
        "The engine must support multiple sports and many simultaneous live matches without hard-coding sport logic into the core platform."
    ]))

    body.append(p("1. Module Objective", style="Heading1"))
    body.append(p("Build a universal, event-driven Live Score Engine capable of handling multiple sports simultaneously with low-latency updates."))
    body.extend(bullets([
        "Support unlimited concurrent live matches.",
        "Deliver real-time public updates using WebSockets through Socket.IO.",
        "Maintain complete event history and audit trails.",
        "Automatically update standings, leaderboards, and statistics after scoring events.",
        "Allow authorized corrections with mandatory reason capture and logging.",
    ]))

    body.append(p("2. High-Level Architecture", style="Heading1"))
    body.append(p("The architecture separates operator input, validation, live score service logic, immutable event storage, match state calculation, Redis active-state caching, and Socket.IO broadcasting."))
    body.append(image_paragraph("rIdImage1", "Live Score Engine Architecture", "Live Score Engine architecture diagram", 1))

    body.append(p("3. Match Lifecycle", style="Heading1"))
    body.append(p("Every match follows the same lifecycle. Each transition must be validated, authorized where required, logged, and broadcast to connected clients."))
    body.append(image_paragraph("rIdImage2", "Universal Match Lifecycle", "Universal match lifecycle diagram", 2))
    body.append(table([
        ["Lifecycle Area", "States"],
        ["Pre-Match", "Scheduled, team check-in, warm-up, ready."],
        ["Live Operation", "Live, paused, delayed, interrupted."],
        ["Post-Match", "Completed, verified, published, archived."],
        ["Validation", "Every transition checks sport rules, permission, current state, timing, and audit requirements."],
    ], [2400, 6960]))

    body.append(p("4. Universal Match Model", style="Heading1"))
    body.append(table([
        ["Model Group", "Fields"],
        ["Tournament Context", "Tournament, sport, category, round, group, match number."],
        ["Location and People", "Venue, court/ground, officials, Team A, Team B."],
        ["Timing", "Scheduled time, actual start time, actual end time, current status."],
        ["Live State", "Live score snapshot, timer, current period, recent events, statistics."],
    ], [2400, 6960]))

    body.append(p("5. Sport Adapter Architecture", style="Heading1"))
    body.append(p("The scoring engine must be modular. New sports should be added by implementing a new scoring adapter rather than changing the core engine."))
    body.append(image_paragraph("rIdImage3", "Sport Adapter Architecture", "Sport adapter architecture diagram", 3))
    body.append(table([
        ["Adapter Responsibility", "Details"],
        ["Scoring Rules", "Validate scoring commands and allowed event types for the sport."],
        ["Match Periods", "Define quarters, halves, overs, sets, games, time controls, or custom periods."],
        ["Statistics", "Update sport-specific player and team metrics."],
        ["Winner Calculation", "Determine winner, draw, tie-break, shootout, NRR, or set-based result."],
    ], [2600, 6760]))

    body.append(p("6. Sport-Specific Scoring", style="Heading1"))
    body.append(table([
        ["Sport", "Tracked Data"],
        ["Cricket", "Runs, wickets, overs, balls, extras, fours, sixes, partnerships, strike rate, economy rate; supports limited overs, T20, ODI, and future Test mode."],
        ["Football", "Goals, assists, yellow cards, red cards, substitutions, corners, possession, offside, shots, saves; supports extra time and penalty shootout."],
        ["Basketball", "2-point field goals, 3-point field goals, free throws, fouls, rebounds, assists, steals, blocks, timeouts, quarter."],
        ["Volleyball", "Points, sets, timeouts, aces, blocks, errors."],
        ["Badminton", "Points, games, match, service changes."],
        ["Chess", "White player, black player, moves, time remaining, result, future PGN support."],
        ["Kabaddi", "Raid points, tackle points, bonus points, all out, super raid, super tackle."],
    ], [2100, 7260]))

    body.append(p("7. Match Timer", style="Heading1"))
    body.append(p("Provide a configurable timer that supports count up, count down, multiple periods, halftime, timeout, injury time, and overtime. Timer state must synchronize across all connected clients and recover after reconnects."))

    body.append(p("8. Event Timeline and Commentary", style="Heading1"))
    body.append(table([
        ["Feature", "Specification"],
        ["Immutable Timeline", "Every scoring action becomes an event such as goal, yellow card, timeout, three pointer, wicket, or match paused."],
        ["Filtering", "Timeline supports filtering by event type, team, player, period, and time range."],
        ["Commentary Fields", "Time, author, commentary text, match reference."],
        ["Display", "Newest commentary entries first with auto-refresh and public live dashboard support."],
    ], [2400, 6960]))

    body.append(p("9. Player and Team Statistics", style="Heading1"))
    body.append(table([
        ["Statistics Type", "Examples"],
        ["Cricket Player", "Runs, balls, boundaries, strike rate, wickets, economy."],
        ["Football Player", "Goals, assists, cards, pass accuracy."],
        ["Basketball Player", "Points, rebounds, assists, steals, blocks."],
        ["Team Statistics", "Possession, shots, accuracy, fouls, timeouts, win percentage."],
        ["Availability", "Statistics should be available during and after matches and update automatically from match events."],
    ], [2400, 6960]))

    body.append(p("10. Public Live Dashboard", style="Heading1"))
    body.append(p("The public dashboard should show current score, match timer, current period, team logos, recent events, live commentary, team statistics, player highlights, standings, share match, and future full-screen mode. Updates should appear without page reload."))

    body.append(p("11. Leaderboard Automation", style="Heading1"))
    body.append(table([
        ["After Match Completion", "Automatic Updates"],
        ["Team Results", "Team points, wins, losses, draws, and qualification status."],
        ["Sport Metrics", "Goal difference, net run rate, rankings, set differences, or sport-specific tie-breakers."],
        ["No Manual Calculation", "Leaderboard changes are computed from verified match results and scoring events."],
    ], [2600, 6760]))

    body.append(p("12. Score Correction", style="Heading1"))
    body.append(p("Authorized users can undo the last event, edit an event, delete an event, or add a missed event. Corrections require a mandatory reason, optional approval workflow, and audit logging."))
    body.append(image_paragraph("rIdImage4", "Correction, Replay, and Broadcast Flow", "Correction replay and broadcast flow diagram", 4))

    body.append(p("13. Socket.IO Communication", style="Heading1"))
    body.append(table([
        ["Socket Area", "Specification"],
        ["Namespaces", "/live, /admin, /management."],
        ["Rooms", "Tournament, match, and venue rooms for efficient broadcasting."],
        ["Events", "Match started, score updated, timer updated, event added, match paused, match completed."],
        ["Reconnect", "Clients reconnect automatically after connection loss and resync current match state."],
    ], [2400, 6960]))

    body.append(p("14. Redis Caching", style="Heading1"))
    body.append(p("Cache current score, timer, match state, and leaderboards. Cache must be invalidated or refreshed after every scoring event to reduce database load while keeping active match state accurate."))

    body.append(p("15. Performance and Scalability", style="Heading1"))
    body.extend(bullets([
        "Handle thousands of concurrent spectators.",
        "Support hundreds of simultaneous live matches.",
        "Minimize latency for score, timer, and timeline updates.",
        "Batch non-critical updates where appropriate.",
        "Support horizontal scalability for the Socket.IO gateway.",
        "Transmit only changed data to clients where possible.",
    ]))

    body.append(p("16. Error Handling", style="Heading1"))
    body.append(table([
        ["Error Type", "Required Handling"],
        ["Network Interruptions", "Reconnect, resync state, and show operator/client feedback."],
        ["Duplicate Submissions", "Detect by command ID, sequence number, or idempotency key."],
        ["Out-of-Order Events", "Validate sequence and rebuild state from event history when needed."],
        ["Timer Issues", "Detect drift and resynchronize timer state across clients."],
        ["Unauthorized Updates", "Reject request, show meaningful feedback, and record audit entry."],
    ], [2600, 6760]))

    body.append(p("17. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Build a universal event-driven architecture rather than hard-coding sport logic.",
        "Separate sport rules into reusable scoring adapters.",
        "Use Socket.IO namespaces and rooms for efficient broadcasting.",
        "Store all match events in PostgreSQL while caching active match state in Redis.",
        "Design APIs to support replaying match history from stored events.",
        "Optimize updates so only changed data is transmitted to clients.",
        "Ensure all score changes are validated, authorized, and auditable.",
        "Structure the code so adding a new sport requires a new adapter without modifying the core engine.",
    ]))
    body.append(rich_callout("Phase 7 Completion Criteria", [
        "Phase 7 is complete when the live score objective, high-level architecture, match lifecycle, universal match model, sport adapters, scoring rules, timer, event timeline, commentary, player/team statistics, public live dashboard, leaderboard automation, corrections, Socket.IO communication, Redis caching, scalability, error handling, and implementation rules are clear enough for production planning."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase7_live_score_architecture.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase7_match_lifecycle.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase7_sport_adapter_architecture.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase7_correction_replay_flow.png"/>
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
  <dc:title>Smart Sportz - Phase 7 Live Score Engine and Match Intelligence</dc:title>
  <dc:subject>Event-driven live scoring, sport adapters, match state, analytics, Socket.IO, Redis, corrections, and public live experience specification</dc:subject>
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
        "word/media/phase7_live_score_architecture.png": ASSET_DIR / "phase7_live_score_architecture.png",
        "word/media/phase7_match_lifecycle.png": ASSET_DIR / "phase7_match_lifecycle.png",
        "word/media/phase7_sport_adapter_architecture.png": ASSET_DIR / "phase7_sport_adapter_architecture.png",
        "word/media/phase7_correction_replay_flow.png": ASSET_DIR / "phase7_correction_replay_flow.png",
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
