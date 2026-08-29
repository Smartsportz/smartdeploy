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

New-Canvas (Join-Path $outDir "phase7_live_score_architecture.png") `
    "Live Score Engine Architecture" `
    "Event-driven scoring pipeline from operator input to public real-time display" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 75 215 225 115 "Scorer" "Management user score control panel" $soft $line
        Draw-Box $g 365 215 225 115 "Validation" "RBAC, sport rules, sequence, timer, duplicates" $soft $line
        Draw-Box $g 655 215 255 115 "Live Score Service" "Node.js service, scoring commands, event dispatch" $soft $line
        Draw-Box $g 1000 190 230 105 "Event Store" "Immutable PostgreSQL match events" $soft $line
        Draw-Box $g 1000 340 230 105 "State Engine" "Current score, timer, statistics, standings" $soft $line
        Draw-Box $g 1300 265 215 115 "Redis Cache" "Active match state and leaderboard cache" $soft $line
        Draw-Box $g 655 545 255 110 "Socket.IO Gateway" "/live, /admin, /management namespaces and rooms" $soft $line
        Draw-Box $g 1000 545 230 110 "Clients" "Public website, admin portal, management portal" $soft $line
        Draw-Arrow $g 300 272 365 272 $line
        Draw-Arrow $g 590 272 655 272 $line
        Draw-Arrow $g 910 260 1000 240 $line
        Draw-Arrow $g 910 285 1000 390 $line
        Draw-Arrow $g 1230 242 1300 315 $line
        Draw-Arrow $g 1230 392 1300 325 $line
        Draw-Arrow $g 780 330 780 545 $line
        Draw-Arrow $g 910 600 1000 600 $line
    }

New-Canvas (Join-Path $outDir "phase7_match_lifecycle.png") `
    "Universal Match Lifecycle" `
    "Validated state transitions with audit logs and real-time status broadcasts" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 210 210 95 "Scheduled" "Fixture exists, teams assigned" $soft $line
        Draw-Box $g 350 210 210 95 "Check-In" "Teams, players, officials verified" $soft $line
        Draw-Box $g 610 210 210 95 "Ready" "Warm-up complete and match can start" $soft $line
        Draw-Box $g 870 210 210 95 "Live" "Timer and scoring events active" $soft $line
        Draw-Box $g 1130 210 210 95 "Paused" "Timeout, injury, delay, interruption" $soft $line
        Draw-Box $g 350 505 210 95 "Completed" "Final event captured" $soft $line
        Draw-Box $g 610 505 210 95 "Verified" "Result reviewed and locked" $soft $line
        Draw-Box $g 870 505 210 95 "Published" "Public result and leaderboard update" $soft $line
        Draw-Box $g 1130 505 210 95 "Archived" "Historical record retained" $soft $line
        Draw-Arrow $g 300 257 350 257 $line
        Draw-Arrow $g 560 257 610 257 $line
        Draw-Arrow $g 820 257 870 257 $line
        Draw-Arrow $g 1080 257 1130 257 $line
        Draw-Arrow $g 1235 305 455 505 $line
        Draw-Arrow $g 560 552 610 552 $line
        Draw-Arrow $g 820 552 870 552 $line
        Draw-Arrow $g 1080 552 1130 552 $line
        Draw-Box $g 575 355 460 90 "Transition Guard" "Every transition is authorized, validated, timestamped, logged, and broadcast" $soft $line
    }

New-Canvas (Join-Path $outDir "phase7_sport_adapter_architecture.png") `
    "Sport Adapter Architecture" `
    "New sports plug into the universal engine without changing core scoring logic" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 600 180 360 115 "IScoringEngine" "Common adapter contract for commands, validation, statistics, winner calculation, tie-breaks" $soft $line
        Draw-Box $g 100 390 230 105 "Cricket Engine" "Runs, wickets, overs, extras, NRR" $soft $line
        Draw-Box $g 395 390 230 105 "Football Engine" "Goals, cards, possession, shootout" $soft $line
        Draw-Box $g 690 390 230 105 "Basketball" "2PT, 3PT, fouls, quarters, timeouts" $soft $line
        Draw-Box $g 985 390 230 105 "Volleyball Engine" "Points, sets, aces, blocks, errors" $soft $line
        Draw-Box $g 1280 390 230 105 "Custom Engine" "Rules, periods, stats, winner logic" $soft $line
        Draw-Box $g 395 590 230 95 "Statistics" "Player and team aggregates" $soft $line
        Draw-Box $g 690 590 230 95 "Leaderboard" "Points, ranking, qualification" $soft $line
        Draw-Box $g 985 590 230 95 "Timeline" "Immutable events and commentary" $soft $line
        Draw-Arrow $g 675 295 215 390 $line
        Draw-Arrow $g 720 295 510 390 $line
        Draw-Arrow $g 780 295 805 390 $line
        Draw-Arrow $g 840 295 1100 390 $line
        Draw-Arrow $g 900 295 1395 390 $line
        Draw-Arrow $g 805 495 510 590 $line
        Draw-Arrow $g 805 495 805 590 $line
        Draw-Arrow $g 805 495 1100 590 $line
    }

New-Canvas (Join-Path $outDir "phase7_correction_replay_flow.png") `
    "Correction, Replay, and Broadcast Flow" `
    "Authorized corrections preserve history, rebuild state, and update connected clients" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 220 230 115 "Correction" "Undo, edit, delete, or add missed event" $soft $line
        Draw-Box $g 375 220 230 115 "Authorization" "Permission check, mandatory reason, optional approval" $soft $line
        Draw-Box $g 665 220 230 115 "Append Event" "Correction event is written to PostgreSQL event store" $soft $line
        Draw-Box $g 955 220 230 115 "Replay Engine" "Rebuild score, timer, statistics, leaderboards" $soft $line
        Draw-Box $g 1245 220 230 115 "Broadcast" "Socket.IO sends changed data to rooms" $soft $line
        Draw-Box $g 375 520 270 115 "Audit Trail" "Who, what, when, reason, previous/new state" $soft $line
        Draw-Box $g 805 520 270 115 "Cache Invalidation" "Refresh Redis score, timer, match state, leaderboard" $soft $line
        Draw-Box $g 1210 520 270 115 "Operator Feedback" "Success, rejected, conflict, retry, or manual review" $soft $line
        Draw-Arrow $g 315 277 375 277 $line
        Draw-Arrow $g 605 277 665 277 $line
        Draw-Arrow $g 895 277 955 277 $line
        Draw-Arrow $g 1185 277 1245 277 $line
        Draw-Arrow $g 490 335 510 520 $line
        Draw-Arrow $g 1070 335 940 520 $line
        Draw-Arrow $g 1360 335 1345 520 $line
    }
