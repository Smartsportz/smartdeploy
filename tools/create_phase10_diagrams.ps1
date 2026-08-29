Add-Type -AssemblyName System.Drawing

$outDir = Join-Path (Get-Location) "docs\assets"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

function New-Canvas($path, $title, $subtitle, $drawCallback) {
    $w = 1600
    $h = 820
    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
    $white = [System.Drawing.Color]::White
    $black = [System.Drawing.Color]::FromArgb(18,18,18)
    $gray = [System.Drawing.Color]::FromArgb(90,90,90)
    $line = [System.Drawing.Color]::FromArgb(35,35,35)
    $soft = [System.Drawing.Color]::FromArgb(248,248,248)
    $g.Clear($white)
    $fontTitle = New-Object System.Drawing.Font("Times New Roman", 34, [System.Drawing.FontStyle]::Bold)
    $fontSub = New-Object System.Drawing.Font("Times New Roman", 18, [System.Drawing.FontStyle]::Regular)
    $g.DrawString($title, $fontTitle, (New-Object System.Drawing.SolidBrush($black)), 70, 42)
    $g.DrawString($subtitle, $fontSub, (New-Object System.Drawing.SolidBrush($gray)), 72, 95)
    $g.DrawLine((New-Object System.Drawing.Pen($line, 3)), 70, 140, 1530, 140)
    & $drawCallback $g $black $gray $line $soft
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

function Draw-Box {
    param(
        [System.Drawing.Graphics]$g,
        [single]$x,
        [single]$y,
        [single]$w,
        [single]$h,
        [string]$title,
        [string]$body,
        [System.Drawing.Color]$black,
        [System.Drawing.Color]$gray,
        [System.Drawing.Color]$line,
        [System.Drawing.Color]$soft
    )
    $rect = New-Object System.Drawing.RectangleF($x, $y, $w, $h)
    $g.FillRectangle((New-Object System.Drawing.SolidBrush($soft)), $rect)
    $g.DrawRectangle((New-Object System.Drawing.Pen($line, 3)), $x, $y, $w, $h)
    $fontHead = New-Object System.Drawing.Font("Times New Roman", 17, [System.Drawing.FontStyle]::Bold)
    $fontBody = New-Object System.Drawing.Font("Times New Roman", 13, [System.Drawing.FontStyle]::Regular)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = New-Object System.Drawing.RectangleF(($x + 10), ($y + 10), ($w - 20), 32)
    $bodyRect = New-Object System.Drawing.RectangleF(($x + 14), ($y + 45), ($w - 28), ($h - 55))
    $g.DrawString($title, $fontHead, (New-Object System.Drawing.SolidBrush($black)), $titleRect, $sf)
    $g.DrawString($body, $fontBody, (New-Object System.Drawing.SolidBrush($black)), $bodyRect, $sf)
}

function Draw-Arrow {
    param(
        [System.Drawing.Graphics]$g,
        [single]$x1,
        [single]$y1,
        [single]$x2,
        [single]$y2,
        [System.Drawing.Color]$line
    )
    $pen = New-Object System.Drawing.Pen($line, 3)
    $pen.CustomEndCap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 8)
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
}

New-Canvas (Join-Path $outDir "phase10_frontend_architecture.png") `
    "React Frontend Application Architecture" `
    "Public website, admin portal, management portal, authentication, and live score experience" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 215 260 105 "Public Layout" "SEO pages, tournaments, sports, results, gallery, contact" $black $gray $line $soft
        Draw-Box $g 455 215 260 105 "Auth Layout" "Login, forgot password, reset password, protected redirects" $black $gray $line $soft
        Draw-Box $g 815 215 260 105 "Admin Layout" "Sidebar, top bar, dashboards, reports, payments" $black $gray $line $soft
        Draw-Box $g 1175 215 260 105 "Management Layout" "Live score controls, match operations, announcements" $black $gray $line $soft
        Draw-Box $g 230 475 260 105 "Shared UI" "Buttons, forms, tables, charts, cards, modals, states" $black $gray $line $soft
        Draw-Box $g 670 475 260 105 "Providers" "Router, QueryClient, Redux, Theme, Socket, ErrorBoundary" $black $gray $line $soft
        Draw-Box $g 1110 475 260 105 "Services" "API clients, auth service, uploads, exports, notifications" $black $gray $line $soft
        Draw-Arrow $g 225 320 340 475 $line
        Draw-Arrow $g 585 320 490 475 $line
        Draw-Arrow $g 945 320 800 475 $line
        Draw-Arrow $g 1305 320 1235 475 $line
        Draw-Arrow $g 490 528 670 528 $line
        Draw-Arrow $g 930 528 1110 528 $line
    }

New-Canvas (Join-Path $outDir "phase10_route_guard_flow.png") `
    "Routing and Permission Guard Flow" `
    "Nested layouts protect portal routes with authentication, role checks, permissions, and user-friendly errors" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 245 220 95 "URL Request" "React Router route match" $black $gray $line $soft
        Draw-Box $g 385 245 220 95 "Layout Match" "Public, Auth, Admin, Management" $black $gray $line $soft
        Draw-Box $g 680 245 220 95 "Auth Guard" "Token, session, profile" $black $gray $line $soft
        Draw-Box $g 975 245 220 95 "Permission Guard" "Role and permission keys" $black $gray $line $soft
        Draw-Box $g 1270 245 220 95 "Page Render" "Loading, empty, success, error states" $black $gray $line $soft
        Draw-Box $g 535 520 230 95 "Unauthorized" "Redirect to login" $black $gray $line $soft
        Draw-Box $g 875 520 230 95 "Forbidden" "403 page with safe action" $black $gray $line $soft
        Draw-Arrow $g 310 292 385 292 $line
        Draw-Arrow $g 605 292 680 292 $line
        Draw-Arrow $g 900 292 975 292 $line
        Draw-Arrow $g 1195 292 1270 292 $line
        Draw-Arrow $g 790 340 660 520 $line
        Draw-Arrow $g 1085 340 990 520 $line
    }

New-Canvas (Join-Path $outDir "phase10_state_data_flow.png") `
    "State, Server Data, and Real-Time Flow" `
    "Redux owns cross-cutting client state while TanStack Query and Socket.IO manage server and live data" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 235 235 105 "UI Components" "Pages, widgets, forms, tables, live score views" $black $gray $line $soft
        Draw-Box $g 430 180 245 105 "Redux Toolkit" "Auth, profile, theme, notifications, command palette" $black $gray $line $soft
        Draw-Box $g 430 385 245 105 "TanStack Query" "Caching, pagination, mutations, optimistic updates" $black $gray $line $soft
        Draw-Box $g 790 180 245 105 "Socket Provider" "Reconnect, room subscriptions, live events" $black $gray $line $soft
        Draw-Box $g 790 385 245 105 "Service Modules" "HTTP API clients, uploads, exports, validation" $black $gray $line $soft
        Draw-Box $g 1170 235 260 105 "Backend APIs" "REST endpoints and Socket.IO channels" $black $gray $line $soft
        Draw-Arrow $g 325 265 430 232 $line
        Draw-Arrow $g 325 310 430 435 $line
        Draw-Arrow $g 675 232 790 232 $line
        Draw-Arrow $g 675 435 790 435 $line
        Draw-Arrow $g 1035 232 1170 265 $line
        Draw-Arrow $g 1035 435 1170 310 $line
    }

New-Canvas (Join-Path $outDir "phase10_component_system.png") `
    "Reusable Component and Experience System" `
    "Design tokens power accessible primitives, domain widgets, forms, tables, and polished page states" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 100 210 250 105 "Design Tokens" "Colors, type, spacing, radius, shadow, motion, breakpoints" $black $gray $line $soft
        Draw-Box $g 440 210 250 105 "UI Primitives" "Button, input, select, badge, tabs, modal, toast" $black $gray $line $soft
        Draw-Box $g 780 210 250 105 "Form System" "React Hook Form, Zod, arrays, upload, autosave" $black $gray $line $soft
        Draw-Box $g 1120 210 250 105 "Table System" "Sorting, filters, pagination, selection, export" $black $gray $line $soft
        Draw-Box $g 280 500 250 105 "Dashboard Widgets" "Statistic, revenue, live match, activity, calendar" $black $gray $line $soft
        Draw-Box $g 665 500 250 105 "Accessibility" "Keyboard, focus, ARIA, contrast, screen readers" $black $gray $line $soft
        Draw-Box $g 1050 500 250 105 "Page States" "Loading, empty, success, error, retry, forbidden" $black $gray $line $soft
        Draw-Arrow $g 350 262 440 262 $line
        Draw-Arrow $g 690 262 780 262 $line
        Draw-Arrow $g 1030 262 1120 262 $line
        Draw-Arrow $g 565 315 405 500 $line
        Draw-Arrow $g 905 315 790 500 $line
        Draw-Arrow $g 1245 315 1175 500 $line
    }
