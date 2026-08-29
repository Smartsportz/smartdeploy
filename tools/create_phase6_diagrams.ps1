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

function Draw-Box($g, $x, $y, $w, $h, $title, $body, $fillColor, $borderColor) {
    $rect = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
    $g.FillRectangle((New-Object System.Drawing.SolidBrush($fillColor)), $rect)
    $g.DrawRectangle((New-Object System.Drawing.Pen($borderColor, 3)), $rect)
    $fontT = New-Object System.Drawing.Font("Times New Roman", 19, [System.Drawing.FontStyle]::Bold)
    $fontB = New-Object System.Drawing.Font("Times New Roman", 13, [System.Drawing.FontStyle]::Regular)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = [System.Drawing.RectangleF]::new([float]($x + 10), [float]($y + 12), [float]($w - 20), [float]30)
    $bodyRect = [System.Drawing.RectangleF]::new([float]($x + 14), [float]($y + 44), [float]($w - 28), [float]($h - 54))
    $g.DrawString($title, $fontT, (New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(18,18,18))), $titleRect, $sf)
    $g.DrawString($body, $fontB, (New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(70,70,70))), $bodyRect, $sf)
}

function Draw-Arrow($g, $x1, $y1, $x2, $y2, $color) {
    $pen = New-Object System.Drawing.Pen($color, 3)
    $pen.CustomEndCap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 7)
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
}

New-Canvas (Join-Path $outDir "phase6_management_portal_layout.png") `
    "Management User Portal Layout" `
    "Role-scoped operations dashboard for assigned tournaments, venues, sports, and actions" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 185 1410 85 "Top Navigation" "Tournament switcher, search, notifications, live match status, profile, connection status" $soft $line
        Draw-Box $g 95 320 280 390 "Collapsible Sidebar" "Dashboard, matches, teams, players, live score, fixtures, results, reports, documents" $soft $line
        Draw-Box $g 430 320 455 165 "Assigned Dashboard" "Active tournament, today's matches, live matches, pending verifications, venue occupancy" $soft $line
        Draw-Box $g 940 320 565 165 "Operations Workspace" "Tables, filters, forms, match controls, score inputs, verification queues" $soft $line
        Draw-Box $g 430 545 455 165 "Quick Actions" "Start match, verify team, publish result, send announcement" $soft $line
        Draw-Box $g 940 545 565 165 "Activity and Reports" "User activity log, performance metrics, exports, notifications, profile history" $soft $line
        Draw-Arrow $g 235 270 235 320 $line
        Draw-Arrow $g 375 515 430 405 $line
        Draw-Arrow $g 375 515 430 625 $line
    }

New-Canvas (Join-Path $outDir "phase6_access_control_scope.png") `
    "Management User Access Scope" `
    "Every route, button, API call, and dataset is filtered by assignment and permission" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 105 240 235 120 "Management User" "Assigned role, active status, login session" $soft $line
        Draw-Box $g 420 205 235 115 "Assignments" "Tournaments, venues, sports" $soft $line
        Draw-Box $g 420 365 235 115 "Permissions" "Granted modules and actions" $soft $line
        Draw-Box $g 750 285 250 125 "Policy Decision" "Combine assignment scope, permission, status, and revocation state" $soft $line
        Draw-Box $g 1100 205 300 115 "Frontend Guard" "Hide routes, buttons, menus, and disabled actions immediately" $soft $line
        Draw-Box $g 1100 365 300 115 "Backend Guard" "Reject API calls, apply query filters, write audit logs" $soft $line
        Draw-Box $g 750 560 300 110 "Revocation Event" "Permission change invalidates UI cache and active access" $soft $line
        Draw-Arrow $g 340 300 420 260 $line
        Draw-Arrow $g 340 300 420 425 $line
        Draw-Arrow $g 655 260 750 335 $line
        Draw-Arrow $g 655 425 750 350 $line
        Draw-Arrow $g 1000 330 1100 260 $line
        Draw-Arrow $g 1000 350 1100 425 $line
        Draw-Arrow $g 900 560 900 410 $line
    }

New-Canvas (Join-Path $outDir "phase6_live_match_score_sync.png") `
    "Live Match and Score Synchronization" `
    "Venue score updates flow through validation, Socket.IO, public displays, and audit history" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 230 230 120 "Score Operator" "Tablet or mobile scoring interface at venue" $soft $line
        Draw-Box $g 380 230 230 120 "Permission Check" "Can update, override, reset, or reverse score event" $soft $line
        Draw-Box $g 670 230 230 120 "Live Score API" "Validate sport rules, timestamp event, persist change" $soft $line
        Draw-Box $g 960 230 230 120 "Socket.IO" "Broadcast score, timer, status, timeline, statistics" $soft $line
        Draw-Box $g 1250 230 230 120 "Public Website" "Live match page, scoreboard, timeline, Smart TV display" $soft $line
        Draw-Box $g 380 520 290 120 "Event History" "All score changes are reversible with permission" $soft $line
        Draw-Box $g 810 520 290 120 "Audit Log" "User, action, tournament, match, timestamp, device" $soft $line
        Draw-Arrow $g 320 290 380 290 $line
        Draw-Arrow $g 610 290 670 290 $line
        Draw-Arrow $g 900 290 960 290 $line
        Draw-Arrow $g 1190 290 1250 290 $line
        Draw-Arrow $g 785 350 525 520 $line
        Draw-Arrow $g 785 350 955 520 $line
    }

New-Canvas (Join-Path $outDir "phase6_offline_venue_workflow.png") `
    "Offline-Ready Venue Workflow" `
    "Intermittent connectivity support for live scoring and tournament operations" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 230 230 120 "Venue Device" "Scorekeeper uses tablet or phone during match" $soft $line
        Draw-Box $g 385 230 230 120 "Local Cache" "Autosave score updates, check-ins, and match events" $soft $line
        Draw-Box $g 675 230 230 120 "Offline Queue" "Store ordered updates while network is unavailable" $soft $line
        Draw-Box $g 965 230 230 120 "Reconnect" "Detect connectivity and send queued updates" $soft $line
        Draw-Box $g 1255 230 230 120 "Server Sync" "Validate sequence, resolve conflicts, broadcast final state" $soft $line
        Draw-Box $g 385 520 300 120 "Conflict Review" "Detect duplicate, stale, or conflicting score events" $soft $line
        Draw-Box $g 820 520 300 120 "Operator Feedback" "Synced, pending, failed, retry, or manual review status" $soft $line
        Draw-Arrow $g 325 290 385 290 $line
        Draw-Arrow $g 615 290 675 290 $line
        Draw-Arrow $g 905 290 965 290 $line
        Draw-Arrow $g 1195 290 1255 290 $line
        Draw-Arrow $g 1370 350 535 520 $line
        Draw-Arrow $g 685 580 820 580 $line
    }
