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

New-Canvas (Join-Path $outDir "phase9_data_domain_map.png") `
    "Enterprise Data Domain Map" `
    "Normalized Prisma schema domains for tournament operations, payments, CMS, audit, and analytics" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 650 325 300 130 "Organization" "Tenant-ready root for users, tournaments, venues, branding, settings" $soft $line
        Draw-Box $g 120 205 235 105 "Identity" "User, Role, Permission, Session, Tokens, AuditLog" $soft $line
        Draw-Box $g 420 205 235 105 "Tournament" "Tournament, Category, Rule, Stage, Announcement" $soft $line
        Draw-Box $g 945 205 235 105 "Sports & Venues" "Sport, SportRule, Venue, Area, Court, Equipment" $soft $line
        Draw-Box $g 1245 205 235 105 "CMS" "Page, Gallery, Sponsor, Blog, FAQ" $soft $line
        Draw-Box $g 120 560 235 105 "Registration" "Registration, Documents, Waitlist, Coupons" $soft $line
        Draw-Box $g 420 560 235 105 "Teams & Players" "Team, Member, Coach, Player, Statistics" $soft $line
        Draw-Box $g 945 560 235 105 "Matches" "Fixture, Match, Period, Event, Commentary" $soft $line
        Draw-Box $g 1245 560 235 105 "Finance & Reports" "Payment, Refund, Invoice, Reports, Settings" $soft $line
        Draw-Arrow $g 650 350 355 257 $line
        Draw-Arrow $g 690 325 655 257 $line
        Draw-Arrow $g 950 350 1060 310 $line
        Draw-Arrow $g 950 390 1245 257 $line
        Draw-Arrow $g 650 430 355 612 $line
        Draw-Arrow $g 690 455 655 612 $line
        Draw-Arrow $g 950 430 1060 560 $line
        Draw-Arrow $g 950 390 1245 612 $line
    }

New-Canvas (Join-Path $outDir "phase9_rbac_data_model.png") `
    "User and RBAC Data Model" `
    "Many-to-many role and permission mapping with sessions, tokens, and immutable audit logs" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 225 230 115 "User" "Identity, contact, status, profile, login info" $soft $line
        Draw-Box $g 385 225 230 115 "UserRole" "Junction table for user-role assignment" $soft $line
        Draw-Box $g 675 225 230 115 "Role" "Super Admin, Manager, Scorer, Finance, Read Only" $soft $line
        Draw-Box $g 965 225 230 115 "RolePermission" "Junction table for role-permission mapping" $soft $line
        Draw-Box $g 1255 225 230 115 "Permission" "tournament.create, live.update, report.export" $soft $line
        Draw-Box $g 230 525 250 115 "Session & Token" "Session, refresh token, password reset, verification" $soft $line
        Draw-Box $g 675 525 250 115 "AuditLog" "User, module, entity, action, JSON diff, IP, device" $soft $line
        Draw-Box $g 1100 525 250 115 "Organization Scope" "Future tenant and resource ownership filtering" $soft $line
        Draw-Arrow $g 325 282 385 282 $line
        Draw-Arrow $g 615 282 675 282 $line
        Draw-Arrow $g 905 282 965 282 $line
        Draw-Arrow $g 1195 282 1255 282 $line
        Draw-Arrow $g 210 340 355 525 $line
        Draw-Arrow $g 790 340 800 525 $line
        Draw-Arrow $g 790 340 1225 525 $line
    }

New-Canvas (Join-Path $outDir "phase9_match_event_live_model.png") `
    "Match, Event, and Live Score Model" `
    "Persistent event history powers live state, replay, statistics, results, and leaderboard updates" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 230 230 115 "Tournament" "Sport, category, rules, stages, schedule" $soft $line
        Draw-Box $g 380 230 230 115 "Fixture" "Round, group, venue, scheduled match setup" $soft $line
        Draw-Box $g 670 230 230 115 "Match" "Teams, officials, status, score summary" $soft $line
        Draw-Box $g 960 230 230 115 "MatchEvent" "Timestamp, type, team, player, value, metadata" $soft $line
        Draw-Box $g 1250 230 230 115 "LiveScore" "Current score, timer, period, state, last update" $soft $line
        Draw-Box $g 380 520 250 115 "Commentary" "Time, author, text, match reference" $soft $line
        Draw-Box $g 720 520 250 115 "ScoreSnapshot" "Point-in-time state for recovery and display" $soft $line
        Draw-Box $g 1060 520 250 115 "Result & Standing" "Winner, ranking, points, qualification" $soft $line
        Draw-Arrow $g 320 287 380 287 $line
        Draw-Arrow $g 610 287 670 287 $line
        Draw-Arrow $g 900 287 960 287 $line
        Draw-Arrow $g 1190 287 1250 287 $line
        Draw-Arrow $g 780 345 505 520 $line
        Draw-Arrow $g 1075 345 845 520 $line
        Draw-Arrow $g 1365 345 1185 520 $line
    }

New-Canvas (Join-Path $outDir "phase9_database_lifecycle.png") `
    "Database Lifecycle, Indexing, and Reporting" `
    "Schema design flows through migrations, seed data, indexed operations, reporting, and immutable history" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 220 230 115 "Prisma Schema" "Grouped models, enums, relations, indexes" $soft $line
        Draw-Box $g 375 220 230 115 "Migrations" "Small, incremental, backward-compatible changes" $soft $line
        Draw-Box $g 665 220 230 115 "Seed Data" "Roles, permissions, sports, demo orgs, users" $soft $line
        Draw-Box $g 955 220 230 115 "Indexes" "Search, filters, composite reporting indexes" $soft $line
        Draw-Box $g 1245 220 230 115 "Operations" "Pagination, pooling, transactions, soft delete" $soft $line
        Draw-Box $g 375 520 270 115 "Reporting" "Revenue, participation, utilization, rankings" $soft $line
        Draw-Box $g 805 520 270 115 "Performance" "Materialized views, Redis live data, heavy query isolation" $soft $line
        Draw-Box $g 1210 520 270 115 "Immutable History" "Payments, results, match events, audit logs" $soft $line
        Draw-Arrow $g 315 277 375 277 $line
        Draw-Arrow $g 605 277 665 277 $line
        Draw-Arrow $g 895 277 955 277 $line
        Draw-Arrow $g 1185 277 1245 277 $line
        Draw-Arrow $g 1070 335 510 520 $line
        Draw-Arrow $g 1070 335 940 520 $line
        Draw-Arrow $g 1360 335 1345 520 $line
    }
