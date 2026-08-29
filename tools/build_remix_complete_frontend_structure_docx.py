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


OUT = Path("docs/Smart_Sportz_Complete_Frontend_Structure_Remix_UI_Blueprint.docx")
ASSET_DIR = Path("docs/assets")


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def image_paragraph_actual(
    rel_id: str,
    name: str,
    descr: str,
    doc_pr_id: int,
    px_w: int = 1600,
    px_h: int = 1120,
    max_width_in: float = 6.8,
    max_height_in: float = 4.95,
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

    body.append(p("SMART SPORTZ - COMPLETE FRONTEND STRUCTURE BLUEPRINT", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Remix UI Analysis, Canonical Page Structure, Workflows, Components, Routes, and Implementation Guidance", style="Subtitle"))
    body.append(p("Reference-only document based on the Remix/Stitch UI folder and existing Smart Sportz phase documents", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Complete Frontend Structure Remix UI Blueprint"],
        ["Project", "Smart Sportz"],
        ["Source UI Folder", r"D:\JOB\Brillaris\Smart_Sportz\stitch_remix_of_smartsportz_enterprise_saas_platform"],
        ["Existing Docs Used", "Phase 2 Design System and Landing Page, Phase 3 Public Website, Phase 4 Registration and Payment, Phase 5 Super Admin, Phase 6 Management User Portal, Phase 7 Live Score Engine, Phase 10 Frontend Architecture, API Master, Database Master, Backend Master, and earlier Stitch frontend reference."],
        ["Output Scope", "Frontend structure only: page map, route tree, shell model, component inventory, workflow mapping, UI state model, folder structure, and implementation rules."],
        ["Instruction", "Do not implement frontend code. Use this document as the correct structure for future frontend implementation."],
        ["Date", "July 22, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Frontend Blueprint Intent", [
        "This document analyzes the full Remix UI reference folder, resolves duplicate page variants into a clean canonical structure, and combines those findings with the existing Smart Sportz phase documents.",
        "The result is an implementation-ready frontend structure document without building or modifying the frontend application."
    ]))

    body.append(p("1. Source UI Inventory", style="Heading1"))
    body.append(p("The Remix folder contains a broader and more mature frontend reference set than the earlier Stitch folder. It includes public pages, auth pages, dashboard pages, management pages, tournament pages, live score pages, media/content pages, and image-only sports assets."))
    body.append(table([
        ["Group", "Reference Folders"],
        ["Public Website", "smartsportz_premium_landing_page_light, smartsportz_premium_landing_page, smartsportz_landing_page, tournament_listing_page, tournament_detail_page, sports_categories_explorer, about_smartsportz_our_story_mission, premium_contact_center, premium_sponsorship_center."],
        ["Content and Support", "professional_sports_media_gallery, professional_sports_news_blog, premium_article_detail_page, professional_faq_center, smartsportz_enterprise_footer_showcase."],
        ["Authentication", "minimal_premium_login_page, interactive_password_recovery_flow, premium_password_recovery, refined_premium_password_recovery."],
        ["Tournament and Live", "professional_tournament_registration, 03_one_tournament_card, 07_live_tournaments_hub, smartsportz_live_match_center, 06_tournaments_live_match, live_score_dashboard_premium_dark, professional_leaderboard_center, professional_team_directory."],
        ["Dashboards and Operations", "01_user_dashboard, professional_user_dashboard_1, professional_user_dashboard_2, 04_analysis_dashboard, tournament_management, 05_teams_and_players, professional_athlete_profile, 02_tournaments."],
        ["Image Assets", "Cricket, football, basketball, and volleyball professional sports photography folders are visual assets, not standalone frontend routes."],
    ], [2300, 7060]))

    body.append(p("2. Visual Reference Sheets", style="Heading1"))
    body.append(p("The four contact sheets below summarize the analyzed Remix screens and provide visual evidence for the page structure decisions."))
    body.append(image_paragraph_actual("rIdPublic", "Remix Public Pages Contact Sheet", "Smart Sportz public website UI reference sheet", 1, 1600, 1120))
    body.append(image_paragraph_actual("rIdContent", "Remix Content and Authentication Contact Sheet", "Smart Sportz content and authentication UI reference sheet", 2, 1600, 1120))
    body.append(image_paragraph_actual("rIdTournament", "Remix Tournament and Live Contact Sheet", "Smart Sportz tournament and live UI reference sheet", 3, 1600, 1120))
    body.append(image_paragraph_actual("rIdDashboard", "Remix Dashboard and Operations Contact Sheet", "Smart Sportz dashboard and operations UI reference sheet", 4, 1600, 1120))

    body.append(p("3. Correct Structure Decisions", style="Heading1"))
    body.append(p("The folder includes overwritten and duplicate page variants. The correct implementation structure should not create duplicate products. It should choose canonical pages and keep variants as visual references or theme alternates."))
    body.append(table([
        ["Area", "Decision"],
        ["Landing Pages", "Use smartsportz_premium_landing_page_light as the canonical public landing page because the new folder is primarily premium light theme. Keep smartsportz_premium_landing_page and smartsportz_landing_page as dark/campaign references."],
        ["Password Recovery", "Use refined_premium_password_recovery as the final visual direction. Use interactive_password_recovery_flow for step behavior and OTP/recovery states."],
        ["User Dashboard", "Use 01_user_dashboard as the canonical participant dashboard. Use professional_user_dashboard_1 and professional_user_dashboard_2 as premium/dark variants for future personalization or role-specific views."],
        ["Admin Dashboard", "Use 04_analysis_dashboard as the Super Admin analytics/dashboard reference. Use tournament_management as Management User portal reference for tournament-specific operations."],
        ["Tournament Pages", "Use tournament_listing_page for public discovery, tournament_detail_page for public tournament detail, professional_tournament_registration for registration wizard, and 03_one_tournament_card as reusable card behavior."],
        ["Live Pages", "Use smartsportz_live_match_center for public live match viewing, 07_live_tournaments_hub for live tournament discovery, and live_score_dashboard_premium_dark for internal live score control."],
        ["Teams and Players", "Use professional_team_directory for teams list/search, professional_athlete_profile for public/player profile detail, and 05_teams_and_players for internal team/player operations."],
        ["Theme Strategy", "Use Premium Light as default for public, auth, registration, and most dashboards. Use Dark Athletic theme for live scoring, media-heavy pages, and high-focus operations."],
    ], [2300, 7060]))

    body.append(p("4. Frontend Application Shells", style="Heading1"))
    body.append(table([
        ["Shell", "Purpose and Included Routes"],
        ["PublicSiteShell", "Marketing, discovery, live public viewing, content, sponsors, contact, FAQ, and public tournament pages. Includes Header, Footer, Search, CTA areas, and public navigation."],
        ["AuthShell", "Login, forgot password, OTP verification, reset password, remember-me state, and auth error/success screens. Should be visually calm and premium."],
        ["ParticipantShell", "Player/team/user dashboard routes: profile, registrations, certificates, payments, performance, match history, notifications, and settings."],
        ["ManagementShell", "Tournament-specific operations for management users: assigned tournaments, registrations, match control, players, announcements, reports, and live scoring."],
        ["SuperAdminShell", "Platform-wide admin: dashboards, users, RBAC, tournaments, teams, payments, CMS, reports, logs, integrations, and settings."],
        ["LiveOpsShell", "Dark high-focus shell for live score control, match timeline, commentary, match intelligence, real-time state, and Socket.IO connection status."],
    ], [2300, 7060]))

    body.append(p("5. Canonical Route Tree", style="Heading1"))
    body.append(table([
        ["Route Group", "Canonical Routes"],
        ["Public", "/, /tournaments, /tournaments/:slug, /sports, /live, /live/:matchId, /leaderboards, /teams, /teams/:slug, /athletes/:slug, /gallery, /blog, /blog/:slug, /about, /contact, /sponsors, /faq"],
        ["Registration and Payment", "/tournaments/:slug/register, /registration/:id/review, /registration/:id/payment, /registration/:id/status, /payments/:paymentId/receipt"],
        ["Authentication", "/login, /forgot-password, /otp, /reset-password, /verify-email, /auth/callback"],
        ["Participant Portal", "/user/dashboard, /user/profile, /user/tournaments, /user/registrations, /user/payments, /user/certificates, /user/notifications, /user/settings"],
        ["Management Portal", "/management/dashboard, /management/tournaments, /management/tournaments/:id, /management/registrations, /management/matches, /management/matches/:id/control, /management/players, /management/announcements, /management/reports, /management/settings"],
        ["Super Admin", "/admin/dashboard, /admin/users, /admin/roles, /admin/permissions, /admin/tournaments, /admin/tournaments/:id, /admin/teams, /admin/players, /admin/payments, /admin/cms, /admin/reports, /admin/logs, /admin/integrations, /admin/settings"],
        ["Live Operations", "/live-ops/dashboard, /live-ops/matches/:id, /live-ops/matches/:id/timeline, /live-ops/matches/:id/statistics, /live-ops/matches/:id/commentary"],
    ], [2300, 7060]))

    body.append(p("6. Public Website Page Structure", style="Heading1"))
    body.append(table([
        ["Page", "Required Sections and Behaviors"],
        ["Home", "Hero, product value, live tournament preview, tournament cards, stats, feature modules, sponsor preview, testimonials, CTA, footer. Canonical visual reference: light premium landing."],
        ["Tournament Listing", "Search, sport/category filters, status tabs, location/date filters, tournament cards, pagination, empty state, loading skeleton, advanced filters."],
        ["Tournament Detail", "Hero, status badge, key metrics, registration CTA, rules, schedule, prize pool, venue/map, teams, gallery, FAQs, organizer/contact, related tournaments."],
        ["Sports Categories", "Sport category grid, active counts, icons, filters, sport details, and transition to tournament listing."],
        ["Live Hub", "Active live match cards, live now status, team/score previews, sport filters, and route to live match center."],
        ["Live Match Center", "Public score view, team cards, innings/quarter/set state, timeline, statistics, officials, standings impact, refresh/socket status."],
        ["Leaderboards", "Tournament selector, category/season filters, team/player rankings, points table, stats, export/share actions."],
        ["Teams Directory", "Search, region/sport/ranking filters, team cards, roster preview, profile link, empty and loading states."],
        ["Athlete Profile", "Hero, player stats, team, achievements, media gallery, upcoming matches, performance history."],
        ["Gallery", "Media filters, image/video cards, highlights, training/gallery tabs, load more, lightbox."],
        ["Blog and Article", "Featured article, category filters, article cards, article detail, author/date, related posts, newsletter CTA."],
        ["About, Contact, Sponsors, FAQ", "Mission/story, contact form and corporate hub, sponsorship tiers, partner logos, FAQ categories, support CTA."],
    ], [2300, 7060]))

    body.append(p("7. Authentication and Recovery Structure", style="Heading1"))
    body.append(table([
        ["Screen", "Required States"],
        ["Login", "Email/password, remember me, forgot password, Google/social optional, error, loading, locked account, pending verification, and redirect after login."],
        ["Forgot Password", "Email input, send OTP/link, validation error, success confirmation, resend timer, back to login."],
        ["OTP Verification", "OTP input, auto focus, resend timer, attempt limit, expired code, success state, and loading state."],
        ["Reset Password", "New password, confirm password, strength rules, token expired, success, and automatic login/redirect option."],
        ["Role Redirect", "Super Admin to /admin/dashboard, Management User to /management/dashboard, Participant/User to /user/dashboard, public users back to requested route."],
    ], [2300, 7060]))

    body.append(p("8. Registration and Payment Flow", style="Heading1"))
    body.extend(bullets([
        "The professional_tournament_registration reference should become the canonical multi-step wizard: personal/team info, roster, documents, payment, review.",
        "Registration must support team mode and individual player mode with dynamic validation based on tournament sport and category.",
        "The payment step must connect to the internal Razorpay order API, display secure payment copy, handle verification, and route to receipt/status pages.",
        "Every step needs draft save, validation, loading, upload progress, payment pending, payment failed, approval pending, approved, rejected, and waitlist states.",
    ]))
    body.append(table([
        ["Step", "Frontend Requirements"],
        ["Step 1: Personal/Team", "Team name, captain/manager, contact email, phone, organization, category, country/state/city, terms acceptance."],
        ["Step 2: Roster", "Player list, captain marker, jersey number, age/date of birth where required, add/remove player, min/max roster validation."],
        ["Step 3: Documents", "Upload IDs, roster proof, payment documents if needed, drag/drop, file validation, progress, preview, remove."],
        ["Step 4: Payment", "Entry fee summary, coupon if enabled, Razorpay checkout trigger, payment status, failure retry, receipt/invoice link."],
        ["Step 5: Review", "Final summary, submission confirmation, registration code, approval status, notification confirmation."],
    ], [2300, 7060]))

    body.append(p("9. Participant Dashboard Structure", style="Heading1"))
    body.append(table([
        ["Module", "Purpose"],
        ["Dashboard Overview", "Welcome card, active registrations, upcoming matches, performance index, action center, notifications."],
        ["Profile", "Personal details, avatar, team membership, documents, verified badges, sport categories."],
        ["My Tournaments", "Registered tournaments, status, payment status, schedule, match results, cancel/withdraw where allowed."],
        ["Performance", "Charts, recent performance, stats cards, certifications, achievements, match history."],
        ["Payments", "Order history, receipts, invoices, refunds, failed payments, retry action."],
        ["Certificates", "Award/certificate list, download action, verification QR/link."],
        ["Settings", "Password, sessions, notification preferences, privacy settings."],
    ], [2300, 7060]))

    body.append(p("10. Management Portal Structure", style="Heading1"))
    body.append(table([
        ["Page", "Required Controls"],
        ["Management Dashboard", "Assigned tournaments, live matches, registration queue, upcoming schedule, recent activity, alerts."],
        ["Tournament Workspace", "Tournament overview, teams, players, fixtures, brackets, rules, venues, announcements, reports."],
        ["Registration Control", "Pending approvals, document verification, payment status, approve/reject/waitlist actions, notes, filters."],
        ["Match Control", "Start/pause/resume/end match, update score, add match event, edit correction with reason, publish result."],
        ["Player Control", "Roster editing, player status, substitutions, documents, player statistics, eligibility review."],
        ["Announcements", "Create/publish announcements, target audience, schedule, pin/unpin, notification delivery."],
        ["Reports", "Tournament summary, registrations, payments, live score logs, player/team stats, export CSV/PDF."],
    ], [2300, 7060]))

    body.append(p("11. Super Admin Portal Structure", style="Heading1"))
    body.append(table([
        ["Page", "Required Controls"],
        ["Executive Dashboard", "System health, revenue, active players, today matches, upcoming matches, registration analytics, global activity."],
        ["Users and RBAC", "User list, create/edit user, roles, permissions, scope, status, password reset, session revoke."],
        ["Tournament Management", "Create/edit/publish tournament, sports, venues, stages, fixtures, brackets, registrations, prize pools."],
        ["Teams and Players", "Global team directory, player profiles, documents, statistics, duplicate checks, eligibility."],
        ["Payments", "Orders, transactions, webhooks, refunds, receipts, invoices, payment reconciliation."],
        ["CMS", "Homepage sections, sponsors, gallery, blogs, FAQs, about/contact content, footer links."],
        ["Reports", "Revenue, participation, tournament performance, registrations, payment exports, platform KPIs."],
        ["Logs and Audit", "Login logs, software events, API logs, webhook logs, score correction audit, admin change history."],
        ["Integrations and Settings", "Razorpay, SMS, WhatsApp, email, push, storage, maps, OpenAI optional, feature flags, security policy."],
    ], [2300, 7060]))

    body.append(p("12. Live Score and Real-Time Frontend Structure", style="Heading1"))
    body.append(table([
        ["Area", "Frontend Requirement"],
        ["Public Live Center", "Read-only match score, timeline, team cards, status, statistics, standings impact, share/follow actions."],
        ["Live Operations Dashboard", "Dark theme scoring console with scoreboard, scoring controls, commentary, event history, correction workflow, and match state."],
        ["Socket State", "Connected, reconnecting, offline, stale data, synced, conflict, and failed update states."],
        ["Sports Variants", "Basketball quarters/points/fouls, cricket overs/wickets/runs, football goals/cards/possession, volleyball sets/points, generic event model."],
        ["Timeline", "Event tags, timestamp/period, actor/player, score impact, commentary, correction marker, admin notes."],
        ["Permissions", "Public can view; Management can score assigned matches; Super Admin can override/correct with reason."],
    ], [2300, 7060]))

    body.append(p("13. Reusable Component Inventory", style="Heading1"))
    body.append(table([
        ["Component Group", "Components"],
        ["Layout", "PublicHeader, PublicFooter, SidebarShell, DashboardTopbar, Breadcrumbs, PageHeader, SectionHeader, EmptyState, ErrorState."],
        ["Navigation", "NavTabs, SportTabs, FilterBar, SearchInput, Pagination, CommandSearch, MobileMenu, ProfileMenu."],
        ["Cards", "TournamentCard, LiveMatchCard, MetricCard, SponsorCard, TeamCard, PlayerCard, ArticleCard, GalleryCard, FixtureCard, PrizeCard."],
        ["Forms", "TextField, SelectField, DateField, PhoneField, FileUpload, OTPInput, PasswordField, FormStepper, FormSummary, TermsCheckbox."],
        ["Tables", "DataTable, SortHeader, RowActions, StatusCell, ProgressCell, ExportButton, BulkActionBar, FilterDrawer."],
        ["Live Score", "Scoreboard, ScoreControls, MatchClock, TimelineRail, CommentaryInput, StatBars, RosterPanel, OfficialsPanel, SocketStatus."],
        ["Charts", "BarChartCard, LineChartCard, ProgressRing, TrendBadge, MiniSparkline, KPIGrid."],
        ["Feedback", "Toast, Modal, ConfirmDialog, Drawer, Tooltip, LoadingSkeleton, InlineAlert, PermissionDenied."],
    ], [2300, 7060]))

    body.append(p("14. State and Permission Model", style="Heading1"))
    body.extend(bullets([
        "Every page must define loading, empty, error, success, offline, permission denied, and responsive mobile states.",
        "All mutation actions must show pending, success, failed, retry, and optimistic-update rollback behavior where useful.",
        "Role-based UI must hide unavailable actions and also show clear blocked states when a user reaches a page without permission.",
        "Public routes are mostly read-only; participant routes allow self-service actions; management routes are tournament-scoped; super admin routes are platform-scoped.",
        "Dark live operations screens must show connection quality and unsynced local action warnings.",
    ]))

    body.append(p("15. API and Data Mapping", style="Heading1"))
    body.append(table([
        ["Frontend Area", "Internal API Namespace"],
        ["Public Website", "/api/v1/public/*, /api/v1/tournaments/public/*, /api/v1/cms/*"],
        ["Authentication", "/api/v1/auth/login, /api/v1/auth/otp/*, /api/v1/auth/refresh, /api/v1/auth/logout, /api/v1/auth/reset-password"],
        ["Registration", "/api/v1/registrations/*, /api/v1/uploads/*, /api/v1/payments/orders, /api/v1/payments/verify"],
        ["Participant Portal", "/api/v1/user/*, /api/v1/registrations/me, /api/v1/payments/me, /api/v1/certificates/me"],
        ["Management Portal", "/api/v1/management/*, /api/v1/matches/*, /api/v1/announcements/*, /api/v1/reports/*"],
        ["Super Admin", "/api/v1/admin/*, /api/v1/reports/*, /api/v1/logs/*, /api/v1/integrations/*"],
        ["Live Score", "REST: /api/v1/matches/* and Socket.IO rooms/events for match/tournament updates."],
    ], [2300, 7060]))

    body.append(p("16. Recommended Frontend Folder Structure", style="Heading1"))
    body.append(table([
        ["Folder", "Purpose"],
        ["src/app", "Application bootstrap, router, providers, error boundary, auth bootstrap."],
        ["src/routes/public", "Home, tournaments, tournament detail, sports, live hub, live match, gallery, blog, article, about, contact, sponsors, FAQ."],
        ["src/routes/auth", "Login, forgot password, OTP, reset password, verification callback."],
        ["src/routes/user", "Participant dashboard, profile, registrations, payments, certificates, settings."],
        ["src/routes/management", "Management dashboard, tournament workspace, registrations, matches, match control, players, announcements, reports."],
        ["src/routes/admin", "Super admin dashboard, users, RBAC, tournaments, teams, players, payments, CMS, reports, logs, integrations, settings."],
        ["src/components/common", "Buttons, inputs, modals, cards, tables, tabs, filters, loaders, alerts, tooltips."],
        ["src/components/domain", "Tournament, registration, payment, team, player, live-score, CMS, notification, report components."],
        ["src/features", "Feature modules with hooks, API clients, store slices, validation schemas, and page-specific components."],
        ["src/services/api", "Axios/fetch client, endpoint modules, interceptors, token refresh, error normalization."],
        ["src/services/socket", "Socket.IO client, room subscriptions, event types, reconnect behavior."],
        ["src/store", "Redux slices for auth/session/UI plus small global state only; server state stays in React Query."],
        ["src/styles", "Tailwind theme, design tokens, typography, light/dark theme variables."],
        ["src/types", "Shared request/response types, domain types, route params, Socket.IO event payloads."],
        ["src/assets", "Images, icons, logos, empty state visuals, sport photography references."],
        ["src/tests", "Unit, component, integration, E2E test helpers and fixtures."],
    ], [2300, 7060]))

    body.append(p("17. Design System Implementation Rules", style="Heading1"))
    body.extend(bullets([
        "Use the light Elite Athletic Management system as the default: white canvas, emerald green primary, deep slate text, Poppins/Be Vietnam Pro, 18px cards, 8px controls.",
        "Use the dark Elite Athletic Management system for live score, media-heavy, and operations screens: dark navy/charcoal surfaces, championship green, subtle glassmorphism, JetBrains Mono for scores/tables.",
        "Do not mix every variant on one route. Each route must have one canonical visual identity and optional dark mode only when useful.",
        "Cards should feel premium but operational: soft shadows in light theme, tonal layering in dark theme, no crowded nested cards.",
        "All filters, tabs, buttons, forms, tables, cards, and live score widgets must be reusable components with predictable spacing.",
    ]))

    body.append(p("18. Build Order Recommendation", style="Heading1"))
    body.append(table([
        ["Order", "Frontend Build Package"],
        ["1", "Design tokens, Tailwind theme, app providers, router, auth provider, API client, Socket.IO client, base layout shells."],
        ["2", "Public website routes: home, tournaments, detail, sports, live hub, gallery, blog, about, contact, sponsors, FAQ."],
        ["3", "Authentication routes and protected-route behavior."],
        ["4", "Registration/payment wizard and receipt/status pages."],
        ["5", "Participant dashboard and profile/payment/certificate modules."],
        ["6", "Management portal with tournament workspace, registration approval, match control, announcements, reports."],
        ["7", "Super Admin portal with users/RBAC, tournament builder, payments, CMS, reports, logs, settings."],
        ["8", "Live score real-time dashboard, public live center, Socket.IO state handling, correction workflow, sport-specific score controls."],
        ["9", "Testing, accessibility pass, responsive QA, performance optimization, empty/error/loading states, final polish."],
    ], [1100, 8260]))

    body.append(p("19. Acceptance Criteria", style="Heading1"))
    body.extend(bullets([
        "The frontend implementation must follow the canonical route tree and avoid duplicate route variants for the same page.",
        "Every UI route must map to a documented internal API namespace and use React Query for server state.",
        "Every dashboard, table, form, live score surface, and public page must include loading, empty, error, success, permission, and mobile states.",
        "Public and registration pages should default to the premium light theme; live scoring and high-focus operations can use the dark theme.",
        "Super Admin and Management portals must clearly separate platform-wide permissions from tournament-scoped permissions.",
        "The final frontend must preserve the premium SaaS design direction while remaining practical for repeated tournament operations.",
    ]))
    body.append(rich_callout("Frontend Structure Completion Criteria", [
        "This document is complete when the frontend team can implement Smart Sportz from a single source of truth: canonical page structure, route tree, shells, workflows, components, state rules, API mapping, theme decisions, and folder structure."
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
  <Relationship Id="rIdPublic" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/remix_public_pages_contact_sheet.png"/>
  <Relationship Id="rIdContent" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/remix_content_auth_contact_sheet.png"/>
  <Relationship Id="rIdTournament" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/remix_tournament_live_contact_sheet.png"/>
  <Relationship Id="rIdDashboard" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/remix_dashboard_operations_contact_sheet.png"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Complete Frontend Structure Remix UI Blueprint</dc:title>
  <dc:subject>Canonical frontend page structure, routes, shells, components, workflows, state rules, API mapping, and theme decisions based on Remix UI references and existing phase documents</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/remix_public_pages_contact_sheet.png": ASSET_DIR / "remix_public_pages_contact_sheet.png",
        "word/media/remix_content_auth_contact_sheet.png": ASSET_DIR / "remix_content_auth_contact_sheet.png",
        "word/media/remix_tournament_live_contact_sheet.png": ASSET_DIR / "remix_tournament_live_contact_sheet.png",
        "word/media/remix_dashboard_operations_contact_sheet.png": ASSET_DIR / "remix_dashboard_operations_contact_sheet.png",
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
