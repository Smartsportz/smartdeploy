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
    $brushBlack = New-Object System.Drawing.SolidBrush($black)
    $brushGray = New-Object System.Drawing.SolidBrush($gray)
    $pen = New-Object System.Drawing.Pen($line, 3)

    $g.DrawString($title, $fontTitle, $brushBlack, 70, 42)
    $g.DrawString($subtitle, $fontSub, $brushGray, 72, 95)
    $g.DrawLine($pen, 70, 140, 1530, 140)

    & $drawCallback $g $black $gray $line $soft

    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

function Draw-Box($g, $x, $y, $w, $h, $title, $body, $fillColor, $borderColor) {
    $rect = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
    $brush = New-Object System.Drawing.SolidBrush($fillColor)
    $pen = New-Object System.Drawing.Pen($borderColor, 3)
    $g.FillRectangle($brush, $rect)
    $g.DrawRectangle($pen, $rect)

    $fontT = New-Object System.Drawing.Font("Times New Roman", 20, [System.Drawing.FontStyle]::Bold)
    $fontB = New-Object System.Drawing.Font("Times New Roman", 15, [System.Drawing.FontStyle]::Regular)
    $blackBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(18,18,18))
    $grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(70,70,70))
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = [System.Drawing.RectangleF]::new([float]($x + 10), [float]($y + 12), [float]($w - 20), [float]32)
    $bodyRect = [System.Drawing.RectangleF]::new([float]($x + 14), [float]($y + 46), [float]($w - 28), [float]($h - 56))
    $g.DrawString($title, $fontT, $blackBrush, $titleRect, $sf)
    $g.DrawString($body, $fontB, $grayBrush, $bodyRect, $sf)
}

function Draw-Arrow($g, $x1, $y1, $x2, $y2, $color) {
    $pen = New-Object System.Drawing.Pen($color, 3)
    $cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 7)
    $pen.CustomEndCap = $cap
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
}

New-Canvas (Join-Path $outDir "phase1_tournament_lifecycle.png") `
    "Tournament Lifecycle Workflow" `
    "End-to-end operating path for Smart Sportz" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 230 210 120 "Create" "Tournament`nSports`nVenue" $soft $line
        Draw-Box $g 340 230 210 120 "Publish" "Public page`nRegistration open" $soft $line
        Draw-Box $g 600 230 210 120 "Register" "Teams`nPlayers`nDocuments" $soft $line
        Draw-Box $g 860 230 210 120 "Payment" "Razorpay`nReceipt`nConfirmation" $soft $line
        Draw-Box $g 1120 230 210 120 "Fixtures" "League`nKnockout`nHybrid" $soft $line
        Draw-Arrow $g 290 290 340 290 $line
        Draw-Arrow $g 550 290 600 290 $line
        Draw-Arrow $g 810 290 860 290 $line
        Draw-Arrow $g 1070 290 1120 290 $line
        Draw-Box $g 250 520 240 120 "Assign" "Management users`nPermissions" $soft $line
        Draw-Box $g 560 520 240 120 "Live Match" "Start`nScore`nTimeline" $soft $line
        Draw-Box $g 870 520 240 120 "Results" "Winners`nReports`nCertificates" $soft $line
        Draw-Arrow $g 1225 350 370 520 $line
        Draw-Arrow $g 490 580 560 580 $line
        Draw-Arrow $g 800 580 870 580 $line
    }

New-Canvas (Join-Path $outDir "phase1_rbac_model.png") `
    "Role-Based Access Control Model" `
    "Azure-style permissions across admin, management, and public surfaces" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 620 185 330 100 "Super Admin" "Global control, users, tournaments, payments, CMS, reports" $soft $line
        Draw-Box $g 185 385 320 130 "Permissions" "Create, edit, publish, approve, verify, refund, export" $soft $line
        Draw-Box $g 620 385 330 130 "Management User" "Assigned tournaments, match control, live scoring, verification" $soft $line
        Draw-Box $g 1065 385 320 130 "Public User" "Browse, register, pay, view schedules, live scores, results" $soft $line
        Draw-Box $g 510 610 540 95 "Scope Rules" "Tournament, sport, venue, module, and action-level access control" $soft $line
        Draw-Arrow $g 785 285 350 385 $line
        Draw-Arrow $g 785 285 785 385 $line
        Draw-Arrow $g 950 435 1065 435 $line
        Draw-Arrow $g 350 515 650 610 $line
        Draw-Arrow $g 785 515 785 610 $line
    }

New-Canvas (Join-Path $outDir "phase1_system_architecture.png") `
    "High-Level System Architecture" `
    "Frontend, backend services, real-time scoring, data, and external providers" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 190 270 130 "Users" "Public website`nAdmin portal`nManagement portal" $soft $line
        Draw-Box $g 460 190 270 130 "Nginx" "Reverse proxy`nHTTPS routing" $soft $line
        Draw-Box $g 825 190 270 130 "React Frontend" "Vite`nTypeScript`nTailwind" $soft $line
        Draw-Box $g 460 405 270 130 "Express Backend" "REST APIs`nJWT/RBAC`nValidation" $soft $line
        Draw-Box $g 825 405 270 130 "Socket.IO" "Live scores`nMatch status`nTimeline" $soft $line
        Draw-Box $g 1190 405 270 130 "Services" "Payments`nNotifications`nReports" $soft $line
        Draw-Box $g 375 625 250 95 "PostgreSQL" "Primary data" $soft $line
        Draw-Box $g 675 625 250 95 "Redis" "Cache and jobs" $soft $line
        Draw-Box $g 975 625 250 95 "External APIs" "Razorpay, S3, Email, SMS, WhatsApp" $soft $line
        Draw-Arrow $g 365 250 460 250 $line
        Draw-Arrow $g 730 250 825 250 $line
        Draw-Arrow $g 595 305 595 405 $line
        Draw-Arrow $g 730 465 825 465 $line
        Draw-Arrow $g 1095 465 1190 465 $line
        Draw-Arrow $g 595 525 500 625 $line
        Draw-Arrow $g 730 525 800 625 $line
        Draw-Arrow $g 1190 525 1100 625 $line
    }
