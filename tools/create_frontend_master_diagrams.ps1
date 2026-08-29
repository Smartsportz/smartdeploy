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
    $fontTitle = New-Object System.Drawing.Font("Times New Roman", 32, [System.Drawing.FontStyle]::Bold)
    $fontSub = New-Object System.Drawing.Font("Times New Roman", 17, [System.Drawing.FontStyle]::Regular)
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
    $fontHead = New-Object System.Drawing.Font("Times New Roman", 16, [System.Drawing.FontStyle]::Bold)
    $fontBody = New-Object System.Drawing.Font("Times New Roman", 12, [System.Drawing.FontStyle]::Regular)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = New-Object System.Drawing.RectangleF(($x + 10), ($y + 9), ($w - 20), 32)
    $bodyRect = New-Object System.Drawing.RectangleF(($x + 12), ($y + 43), ($w - 24), ($h - 50))
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

New-Canvas (Join-Path $outDir "frontend_master_experience_map.png") `
    "Smart Sportz Frontend Experience Map" `
    "Public discovery, registration, admin control, management operations, and live score experiences" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 105 210 250 105 "Public Website" "Landing, tournaments, sports, live, results, gallery, blogs, contact" $black $gray $line $soft
        Draw-Box $g 440 210 250 105 "Registration" "Team/player onboarding, documents, payment, approval" $black $gray $line $soft
        Draw-Box $g 775 210 250 105 "Super Admin" "Users, RBAC, tournaments, finance, CMS, reports, audit" $black $gray $line $soft
        Draw-Box $g 1110 210 250 105 "Management Portal" "Assigned tournaments, matches, players, live score, reports" $black $gray $line $soft
        Draw-Box $g 280 500 250 105 "Live Match Center" "Scoreboard, timeline, commentary, stats, leaderboard" $black $gray $line $soft
        Draw-Box $g 675 500 250 105 "Shared Platform" "Auth, layouts, components, query, Redux, sockets, theme" $black $gray $line $soft
        Draw-Box $g 1070 500 250 105 "Production UX" "Responsive, accessible, fast, error-safe, deployable" $black $gray $line $soft
        Draw-Arrow $g 355 260 440 260 $line
        Draw-Arrow $g 690 260 775 260 $line
        Draw-Arrow $g 1025 260 1110 260 $line
        Draw-Arrow $g 440 315 405 500 $line
        Draw-Arrow $g 900 315 800 500 $line
        Draw-Arrow $g 1235 315 1195 500 $line
    }

New-Canvas (Join-Path $outDir "frontend_registration_payment_workflow.png") `
    "Public Registration and Payment Workflow" `
    "Visitor discovery flows into registration, Razorpay payment, approval, notification, and dashboard state" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 75 245 210 95 "Discover" "Landing, tournaments, sport filters, details" $black $gray $line $soft
        Draw-Box $g 350 245 210 95 "Register" "Team or player form, category, documents" $black $gray $line $soft
        Draw-Box $g 625 245 210 95 "Validate" "Zod rules, slots, documents, coupons" $black $gray $line $soft
        Draw-Box $g 900 245 210 95 "Pay" "Razorpay checkout, order, receipt" $black $gray $line $soft
        Draw-Box $g 1175 245 210 95 "Review" "Approval, waitlist, rejection, refund" $black $gray $line $soft
        Draw-Box $g 360 520 230 95 "User Updates" "Email, SMS, WhatsApp, push, status page" $black $gray $line $soft
        Draw-Box $g 815 520 230 95 "Admin Queue" "Search, filters, approve, verify, audit log" $black $gray $line $soft
        Draw-Arrow $g 285 292 350 292 $line
        Draw-Arrow $g 560 292 625 292 $line
        Draw-Arrow $g 835 292 900 292 $line
        Draw-Arrow $g 1110 292 1175 292 $line
        Draw-Arrow $g 455 340 475 520 $line
        Draw-Arrow $g 1280 340 930 520 $line
    }

New-Canvas (Join-Path $outDir "frontend_admin_management_workflow.png") `
    "Admin and Management Operations Workflow" `
    "Super Admin configures the platform while Management Users operate assigned tournaments and matches" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 220 230 100 "Super Admin" "Organizations, users, RBAC, master data" $black $gray $line $soft
        Draw-Box $g 405 220 230 100 "Tournament Setup" "Sports, venues, categories, fees, rules, CMS" $black $gray $line $soft
        Draw-Box $g 715 220 230 100 "Assign Access" "Managers, scorers, finance, report users" $black $gray $line $soft
        Draw-Box $g 1025 220 230 100 "Management User" "Assigned tournaments, teams, matches" $black $gray $line $soft
        Draw-Box $g 280 500 250 100 "Operational Actions" "Verify players, control matches, publish updates" $black $gray $line $soft
        Draw-Box $g 675 500 250 100 "Audit & Reports" "Activity logs, exports, finance, participation" $black $gray $line $soft
        Draw-Box $g 1070 500 250 100 "Public Output" "Fixtures, live scores, results, announcements" $black $gray $line $soft
        Draw-Arrow $g 325 270 405 270 $line
        Draw-Arrow $g 635 270 715 270 $line
        Draw-Arrow $g 945 270 1025 270 $line
        Draw-Arrow $g 1140 320 405 500 $line
        Draw-Arrow $g 530 550 675 550 $line
        Draw-Arrow $g 925 550 1070 550 $line
    }

New-Canvas (Join-Path $outDir "frontend_live_score_workflow.png") `
    "Live Score Frontend Workflow" `
    "Operator actions create validated events that update scoreboards, timelines, statistics, and public viewers" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 235 220 100 "Scorer UI" "Start match, score event, correction, pause" $black $gray $line $soft
        Draw-Box $g 375 235 220 100 "Validation" "Permission, match state, sport adapter rules" $black $gray $line $soft
        Draw-Box $g 670 235 220 100 "Socket Event" "Room emit, reconnect, optimistic status" $black $gray $line $soft
        Draw-Box $g 965 235 220 100 "Public Live UI" "Scoreboard, commentary, timeline, stats" $black $gray $line $soft
        Draw-Box $g 1260 235 220 100 "Reports" "Results, standings, leaderboards, exports" $black $gray $line $soft
        Draw-Box $g 410 515 235 100 "Audit Trail" "Every score and correction logged with reason" $black $gray $line $soft
        Draw-Box $g 835 515 235 100 "Offline/Recovery" "Connection state, retry queue, sync feedback" $black $gray $line $soft
        Draw-Arrow $g 300 285 375 285 $line
        Draw-Arrow $g 595 285 670 285 $line
        Draw-Arrow $g 890 285 965 285 $line
        Draw-Arrow $g 1185 285 1260 285 $line
        Draw-Arrow $g 485 335 525 515 $line
        Draw-Arrow $g 780 335 950 515 $line
    }

New-Canvas (Join-Path $outDir "frontend_state_architecture.png") `
    "Frontend State and Data Architecture" `
    "React components use typed services, TanStack Query, Redux, and Socket.IO without mixing responsibilities" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 100 240 230 100 "Pages & Widgets" "Public, admin, management, auth, live views" $black $gray $line $soft
        Draw-Box $g 420 170 230 100 "Redux Toolkit" "Auth, profile, theme, notifications, selected match" $black $gray $line $soft
        Draw-Box $g 420 390 230 100 "TanStack Query" "Server cache, pagination, mutations, optimistic updates" $black $gray $line $soft
        Draw-Box $g 760 170 230 100 "Socket Provider" "Rooms, reconnect, live events, status" $black $gray $line $soft
        Draw-Box $g 760 390 230 100 "Service Modules" "HTTP API, uploads, exports, payment flows" $black $gray $line $soft
        Draw-Box $g 1100 280 260 100 "Backend Platform" "REST APIs, Socket.IO, Redis, PostgreSQL, storage" $black $gray $line $soft
        Draw-Arrow $g 330 270 420 220 $line
        Draw-Arrow $g 330 315 420 440 $line
        Draw-Arrow $g 650 220 760 220 $line
        Draw-Arrow $g 650 440 760 440 $line
        Draw-Arrow $g 990 220 1100 315 $line
        Draw-Arrow $g 990 440 1100 335 $line
    }

New-Canvas (Join-Path $outDir "frontend_route_state_model.png") `
    "Route Guards and Page State Model" `
    "Every protected page resolves auth, permission, data, page state, and recovery behavior consistently" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 240 210 95 "Route Match" "Public, auth, admin, management, live" $black $gray $line $soft
        Draw-Box $g 370 240 210 95 "Auth Check" "JWT, refresh, profile, session state" $black $gray $line $soft
        Draw-Box $g 650 240 210 95 "Permission" "RBAC keys, assigned tournament scope" $black $gray $line $soft
        Draw-Box $g 930 240 210 95 "Data State" "Loading, empty, success, stale, error" $black $gray $line $soft
        Draw-Box $g 1210 240 210 95 "Page UI" "Layout, actions, table, form, widgets" $black $gray $line $soft
        Draw-Box $g 410 520 230 95 "Unauthorized" "Login redirect, remembered destination" $black $gray $line $soft
        Draw-Box $g 730 520 230 95 "Forbidden" "403 page, safe back action, audit hint" $black $gray $line $soft
        Draw-Box $g 1050 520 230 95 "Recovery" "Retry, reconnect, toast, support context" $black $gray $line $soft
        Draw-Arrow $g 300 287 370 287 $line
        Draw-Arrow $g 580 287 650 287 $line
        Draw-Arrow $g 860 287 930 287 $line
        Draw-Arrow $g 1140 287 1210 287 $line
        Draw-Arrow $g 475 335 525 520 $line
        Draw-Arrow $g 755 335 845 520 $line
        Draw-Arrow $g 1035 335 1165 520 $line
    }
