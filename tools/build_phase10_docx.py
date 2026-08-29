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


OUT = Path("docs/Smart_Sportz_Phase_10_Frontend_Architecture_React_Application_Design.docx")
ASSET_DIR = Path("docs/assets")


def bullets(items: list[str]) -> list[str]:
    return [p(item, num_id=1) for item in items]


def document_xml() -> str:
    body: list[str] = []

    body.append(p("PHASE 10 - FRONTEND ARCHITECTURE & REACT APPLICATION DESIGN", style="Title"))
    body.append(p("", style="Subtitle"))
    body.append(p("Enterprise AI Coding Master Prompt", style="Subtitle"))
    body.append(p("Smart Sportz - React Frontend Engineering Blueprint", style="Heading2"))
    body.append(p(""))
    body.append(table([
        ["Document", "Phase 10 Frontend Architecture and React Application Design"],
        ["Project", "Smart Sportz"],
        ["Focus", "React, Vite, TypeScript, Tailwind, reusable component system, nested routing, portals, forms, server state, client state, Socket.IO, accessibility, performance, theming, and testing"],
        ["Reference Style", "Same compact spacing, alignment, borders, margins, and black document treatment as the approved Phase documents"],
        ["Date", "July 5, 2026"],
        ["Version", "1.0"],
    ], [2400, 6960], header=False, fill="FFFFFF"))
    body.append(p(""))
    body.append(rich_callout("Phase 10 Intent", [
        "This document converts the frontend prompt into a production-ready React application architecture for the public website, authentication flow, Super Admin Portal, Management User Portal, and live score experience.",
        "The frontend must be fast, responsive, accessible, modular, reusable, SEO-friendly for public pages, and optimized for real-time tournament operations."
    ]))

    body.append(p("1. Module Objective", style="Heading1"))
    body.append(p("Build a modern frontend using React, Vite, and TypeScript that powers the Smart Sportz public website, Super Admin Portal, Management User Portal, authentication screens, and live score interfaces."))
    body.extend(bullets([
        "Keep public pages SEO-friendly and portal pages workflow-focused.",
        "Use feature-based organization while centralizing shared UI, services, types, assets, hooks, providers, and utilities.",
        "Support loading, empty, success, error, forbidden, unauthorized, and retry states across all user journeys.",
        "Optimize real-time score updates without mixing live server data into permanent client state.",
    ]))

    body.append(p("2. Technology Stack", style="Heading1"))
    body.append(table([
        ["Layer", "Technology"],
        ["Framework", "React 19 with Vite."],
        ["Language", "TypeScript with strict typing and no any usage."],
        ["Styling and Motion", "Tailwind CSS, reusable design tokens, Framer Motion."],
        ["Routing", "React Router with nested route layouts and permission guards."],
        ["State", "Redux Toolkit for cross-cutting client state; TanStack Query for server state."],
        ["Forms and Validation", "React Hook Form and Zod."],
        ["UI Utilities", "Lucide React, Recharts, React Big Calendar, TanStack Table, Sonner, dnd-kit."],
        ["Real Time", "Socket.IO Client through a reusable provider and hooks."],
    ], [2400, 6960]))

    body.append(p("3. React Frontend Application Architecture", style="Heading1"))
    body.append(p("The frontend should be composed around layout shells, shared UI modules, providers, service modules, and feature pages. Each portal should feel dedicated to its workflow while sharing the same design system and engineering foundations."))
    body.append(image_paragraph("rIdImage1", "React Frontend Application Architecture", "React frontend application architecture diagram", 1))

    body.append(p("4. Application Structure", style="Heading1"))
    body.append(table([
        ["Folder", "Responsibility"],
        ["src/app", "Application bootstrap, provider composition, global configuration, app-level boundaries."],
        ["src/assets", "Images, icons, fonts, and illustrations."],
        ["src/components", "Shared common, form, table, chart, card, layout, live-score, and UI components."],
        ["src/layouts", "Public, auth, admin, and management layout shells."],
        ["src/pages", "Public, admin, management, and auth pages."],
        ["src/routes", "Route objects, lazy imports, guards, layout nesting, route metadata."],
        ["src/hooks", "Reusable hooks for UI, auth, data access, sockets, and responsive behavior."],
        ["src/services and src/api", "Typed HTTP clients, resource service modules, upload and export services."],
        ["src/store", "Redux slices for authentication, profile, theme, notifications, command palette, and live match selection."],
        ["src/providers and src/contexts", "QueryClient, Redux, theme, sockets, toasts, error boundaries, and app contexts."],
        ["src/sockets", "Socket client setup, event contracts, room subscription helpers, and live hooks."],
        ["src/constants, src/types, src/utils, src/styles", "Shared configuration, TypeScript contracts, helpers, and global CSS."],
    ], [2600, 6760]))

    body.append(p("5. Routing Strategy", style="Heading1"))
    body.append(p("Use nested routing so layouts own navigation, chrome, and shared context while pages stay focused on feature behavior. Public routes should remain crawlable and fast; portal routes should enforce authentication and permissions."))
    body.append(image_paragraph("rIdImage2", "Routing and Permission Guard Flow", "Routing and permission guard flow diagram", 2))
    body.append(table([
        ["Route Group", "Pages"],
        ["Public Layout", "/, /live, /tournaments, /sports, /results, /contact."],
        ["Auth Layout", "/login, /forgot-password, /reset-password."],
        ["Admin Layout", "/admin/dashboard, /admin/tournaments, /admin/matches, /admin/payments, /admin/reports."],
        ["Management Layout", "/management/dashboard, /management/live-score, /management/results."],
    ], [2400, 6960]))

    body.append(p("6. Layouts", style="Heading1"))
    body.append(table([
        ["Layout", "Required Experience"],
        ["Public Layout", "Sticky navigation, footer, newsletter, global search, public page polish, SEO-friendly metadata."],
        ["Authentication Layout", "Login, forgot password, reset password, minimal distraction, clear validation, safe redirects."],
        ["Admin Layout", "Sidebar, top bar, breadcrumbs, notifications, command palette, dense dashboard workflows."],
        ["Management Layout", "Operational shell with quick access to live matches, score controls, results, and announcements."],
    ], [2400, 6960]))

    body.append(p("7. Design System Implementation", style="Heading1"))
    body.append(p("Expose reusable design tokens through Tailwind configuration and utility classes. The system should define colors, typography, spacing, border radius, shadows, animations, breakpoints, dark mode behavior, and component variants."))
    body.append(image_paragraph("rIdImage4", "Reusable Component and Experience System", "Reusable component and experience system diagram", 4))

    body.append(p("8. Shared Component Library", style="Heading1"))
    body.append(table([
        ["Component Group", "Components"],
        ["Inputs", "Input, TextArea, Select, MultiSelect, Checkbox, Radio, Switch, Date Picker, Time Picker, File Upload."],
        ["Actions and Feedback", "Button, Tooltip, Dropdown, Modal, Drawer, Toast Notifications, Loading Spinner."],
        ["Navigation", "Tabs, Accordion, Pagination, Breadcrumb, Command Palette."],
        ["Display", "Avatar, Badge, Chip, Skeleton Loader, Empty State, Error State."],
        ["Quality Requirements", "Variants, sizes, disabled state, loading state, keyboard navigation, dark mode, accessibility."],
    ], [2600, 6760]))

    body.append(p("9. Dashboard Widgets", style="Heading1"))
    body.extend(bullets([
        "Statistic Card, Revenue Card, Tournament Card, Live Match Card, Activity Feed, Recent Registrations.",
        "Upcoming Matches, Calendar Widget, Notifications Widget, and Leaderboard Widget.",
        "Widgets must accept data through props, avoid hidden data fetching, and remain presentation-focused.",
    ]))

    body.append(p("10. Form Architecture", style="Heading1"))
    body.append(table([
        ["Form Concern", "Requirement"],
        ["Form Engine", "React Hook Form for state, submission, and field registration."],
        ["Validation", "Zod schemas with inline error messages and typed payloads."],
        ["Shared Fields", "Reusable field wrappers for labels, help text, errors, disabled states, and layout."],
        ["Advanced Flows", "Async validation, autosave for long forms, dynamic arrays such as player lists, and file uploads."],
    ], [2400, 6960]))

    body.append(p("11. Data Fetching", style="Heading1"))
    body.append(p("Use TanStack Query for all server interactions. API calls should live in dedicated service modules and expose typed request and response contracts."))
    body.extend(bullets([
        "Use caching, background refetch, pagination, infinite scrolling, mutations, and optimistic updates.",
        "Keep server data in TanStack Query rather than Redux.",
        "Use query keys consistently by resource, tenant scope, tournament scope, filters, and pagination cursor.",
    ]))

    body.append(p("12. Global State", style="Heading1"))
    body.append(p("Use Redux Toolkit only for cross-cutting client state such as authentication, user profile, theme, notifications, command palette, and live match selection. Avoid storing server resources in Redux."))
    body.append(image_paragraph("rIdImage3", "State, Server Data, and Real-Time Flow", "State server data and real-time flow diagram", 3))

    body.append(p("13. Socket.IO Client", style="Heading1"))
    body.append(table([
        ["Responsibility", "Requirement"],
        ["Connection", "Central provider owns connection management and connection status."],
        ["Recovery", "Automatic reconnect and safe re-subscription to active rooms."],
        ["Rooms", "Tournament feed, live match, notifications, and operational event rooms."],
        ["Hooks", "Expose useLiveMatch, useTournamentFeed, and useNotifications."],
        ["Boundary", "Socket events update live UI and TanStack Query cache where appropriate; they should not bypass typed service contracts."],
    ], [2400, 6960]))

    body.append(p("14. Table System", style="Heading1"))
    body.append(p("Build a generic data table used across admin and management modules. It must support server-side pagination, sorting, filtering, search, column visibility, row selection, bulk actions, export, responsive layout, and reusable empty/error/loading states."))

    body.append(p("15. File Management", style="Heading1"))
    body.append(table([
        ["Capability", "Requirement"],
        ["Upload", "Drag-and-drop upload components for images, PDFs, and documents."],
        ["Preview", "Image previews, selected file metadata, validation errors, and retry states."],
        ["Progress", "Progress indicator, cancellation where practical, remove action, and upload status."],
        ["Validation", "File type, file size, count limits, and feature-specific requirements."],
    ], [2400, 6960]))

    body.append(p("16. Accessibility", style="Heading1"))
    body.extend(bullets([
        "Use semantic HTML and keyboard-accessible interactions.",
        "Manage focus for modals, drawers, menus, command palette, and route transitions.",
        "Use ARIA attributes only where semantic HTML is insufficient.",
        "Maintain color contrast compliance and screen reader support.",
        "Ensure all custom interactive components are fully accessible.",
    ]))

    body.append(p("17. Performance", style="Heading1"))
    body.append(table([
        ["Performance Area", "Implementation"],
        ["Code Splitting", "Lazy load route groups, portal sections, heavy charts, calendars, and tables."],
        ["Assets", "Optimize images and avoid loading noncritical media on first paint."],
        ["Large Lists", "Virtualize long lists and tables where needed."],
        ["Rendering", "Use memoization where appropriate and avoid unnecessary re-renders."],
        ["Delivery", "Run bundle analysis, prefetch critical routes, and keep shared chunks intentional."],
    ], [2400, 6960]))

    body.append(p("18. Error Handling", style="Heading1"))
    body.append(p("Provide error boundaries, retry UI, network error pages, unauthorized pages, forbidden pages, and not found pages. User-facing copy should be clear while technical details are logged through the application logging strategy."))

    body.append(p("19. Theme Support", style="Heading1"))
    body.append(p("Support light mode and dark mode. Persist user preference and allow theme switching from top navigation or user settings while keeping system preference as a sensible fallback."))

    body.append(p("20. Testing Strategy", style="Heading1"))
    body.append(table([
        ["Test Level", "Focus"],
        ["Unit", "Reusable components, hooks, validators, utilities, and reducers."],
        ["Integration", "Feature flows such as authentication, registration, payment, live score update, and admin actions."],
        ["End-to-End", "Critical user journeys across public, admin, management, and live score experiences."],
        ["Regression Focus", "Authentication, registration, payments, live score updates, permission guards, and major dashboard flows."],
    ], [2400, 6960]))

    body.append(p("21. AI Coding Instructions", style="Heading1"))
    body.extend(bullets([
        "Create reusable component library modules rather than page-specific one-off components.",
        "Use feature-based organization with shared UI modules.",
        "Keep business logic out of presentation components.",
        "Build forms with React Hook Form and Zod.",
        "Use TanStack Query for all server interactions.",
        "Integrate Socket.IO through a dedicated provider and custom hooks.",
        "Implement responsive layouts for mobile, tablet, desktop, and large displays.",
        "Optimize bundle size using lazy loading and code splitting.",
        "Follow strict TypeScript typing and avoid any.",
        "Ensure every page includes loading, empty, success, and error states.",
    ]))
    body.append(rich_callout("Phase 10 Completion Criteria", [
        "Phase 10 is complete when the frontend objective, technology stack, folder structure, route strategy, layout shells, design system, shared component library, dashboard widgets, forms, data fetching, global state, Socket.IO integration, table system, file management, accessibility, performance, error handling, theme support, testing strategy, and coding rules are clear enough for implementation planning."
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
  <Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase10_frontend_architecture.png"/>
  <Relationship Id="rIdImage2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase10_route_guard_flow.png"/>
  <Relationship Id="rIdImage3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase10_state_data_flow.png"/>
  <Relationship Id="rIdImage4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/phase10_component_system.png"/>
</Relationships>'''


def core_xml() -> str:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Smart Sportz - Phase 10 Frontend Architecture and React Application Design</dc:title>
  <dc:subject>Enterprise React frontend architecture for public website, admin portal, management portal, authentication, live scores, shared components, routing, state, sockets, accessibility, performance, theming, and testing</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assets = {
        "word/media/phase10_frontend_architecture.png": ASSET_DIR / "phase10_frontend_architecture.png",
        "word/media/phase10_route_guard_flow.png": ASSET_DIR / "phase10_route_guard_flow.png",
        "word/media/phase10_state_data_flow.png": ASSET_DIR / "phase10_state_data_flow.png",
        "word/media/phase10_component_system.png": ASSET_DIR / "phase10_component_system.png",
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
