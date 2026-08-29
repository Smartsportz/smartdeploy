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

    $fontT = New-Object System.Drawing.Font("Times New Roman", 19, [System.Drawing.FontStyle]::Bold)
    $fontB = New-Object System.Drawing.Font("Times New Roman", 13, [System.Drawing.FontStyle]::Regular)
    $blackBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(18,18,18))
    $grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(70,70,70))
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = [System.Drawing.RectangleF]::new([float]($x + 10), [float]($y + 12), [float]($w - 20), [float]30)
    $bodyRect = [System.Drawing.RectangleF]::new([float]($x + 14), [float]($y + 44), [float]($w - 28), [float]($h - 54))
    $g.DrawString($title, $fontT, $blackBrush, $titleRect, $sf)
    $g.DrawString($body, $fontB, $grayBrush, $bodyRect, $sf)
}

function Draw-Arrow($g, $x1, $y1, $x2, $y2, $color) {
    $pen = New-Object System.Drawing.Pen($color, 3)
    $cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 7)
    $pen.CustomEndCap = $cap
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
}

New-Canvas (Join-Path $outDir "phase3_public_site_architecture.png") `
    "Public Website Information Architecture" `
    "Discovery, live scores, registration, content, and support surfaces" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 650 175 300 90 "Home" "Hero, live ticker, featured tournaments, stats, CTA" $soft $line
        Draw-Box $g 120 330 260 110 "Discovery" "Tournaments`nSports`nTeams`nPlayers" $soft $line
        Draw-Box $g 450 330 260 110 "Match Center" "Fixtures`nLive Scores`nResults`nLeaderboards" $soft $line
        Draw-Box $g 780 330 260 110 "Registration" "Team registration`nIndividual registration`nPayment" $soft $line
        Draw-Box $g 1110 330 260 110 "Content" "Gallery`nSponsors`nNews & Blogs" $soft $line
        Draw-Box $g 450 540 260 130 "Support" "About`nContact`nFAQ`nPolicies" $soft $line
        Draw-Box $g 780 540 260 130 "Global Tools" "Search`nBreadcrumbs`nSEO`nNewsletter" $soft $line
        Draw-Arrow $g 650 220 380 360 $line
        Draw-Arrow $g 725 265 580 330 $line
        Draw-Arrow $g 850 265 910 330 $line
        Draw-Arrow $g 950 220 1110 360 $line
        Draw-Arrow $g 580 440 580 540 $line
        Draw-Arrow $g 910 440 910 540 $line
    }

New-Canvas (Join-Path $outDir "phase3_registration_payment_flow.png") `
    "Public Registration and Payment Journey" `
    "From tournament discovery to confirmed registration" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 230 225 120 "Discover" "Search, filters, featured cards, tournament details" $soft $line
        Draw-Box $g 355 230 225 120 "Choose" "Tournament, sport, category, registration type" $soft $line
        Draw-Box $g 630 230 225 120 "Register" "Team/player form, documents, validation" $soft $line
        Draw-Box $g 905 230 225 120 "Pay" "Razorpay, UPI, cards, net banking" $soft $line
        Draw-Box $g 1180 230 225 120 "Confirm" "Receipt, email, status, dashboard update" $soft $line
        Draw-Arrow $g 305 290 355 290 $line
        Draw-Arrow $g 580 290 630 290 $line
        Draw-Arrow $g 855 290 905 290 $line
        Draw-Arrow $g 1130 290 1180 290 $line
        Draw-Box $g 280 520 310 115 "Validation States" "Loading, empty, error, success, retry" $soft $line
        Draw-Box $g 690 520 360 115 "Post-Registration" "Fixtures, notifications, live match reminders, downloads" $soft $line
        Draw-Arrow $g 740 350 435 520 $line
        Draw-Arrow $g 1290 350 870 520 $line
    }

New-Canvas (Join-Path $outDir "phase3_live_match_experience.png") `
    "Live Match Page Experience" `
    "Real-time match view powered by Socket.IO updates" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 105 190 280 110 "Match Header" "Tournament, sport, venue, round, match number, status" $soft $line
        Draw-Box $g 500 190 280 110 "Scoreboard" "Teams, score, timer, quarter, overs, sets, rounds" $soft $line
        Draw-Box $g 895 190 280 110 "Socket.IO" "Automatic live updates, match status, score events" $soft $line
        Draw-Box $g 105 405 280 120 "Statistics" "Possession, fouls, rebounds, overs, wickets, cards" $soft $line
        Draw-Box $g 500 405 280 120 "Timeline" "Goals, wickets, timeouts, cards, three pointers" $soft $line
        Draw-Box $g 895 405 280 120 "Commentary" "Newest updates, event feed, match notes" $soft $line
        Draw-Box $g 1280 300 220 130 "Standings" "Match info, rankings, points table, next fixtures" $soft $line
        Draw-Arrow $g 385 245 500 245 $line
        Draw-Arrow $g 780 245 895 245 $line
        Draw-Arrow $g 640 300 245 405 $line
        Draw-Arrow $g 640 300 640 405 $line
        Draw-Arrow $g 1035 300 1035 405 $line
        Draw-Arrow $g 1175 465 1280 365 $line
    }

New-Canvas (Join-Path $outDir "phase3_seo_performance_pipeline.png") `
    "SEO and Performance Pipeline" `
    "Technical requirements for fast, discoverable public pages" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 120 220 250 120 "Page Metadata" "Unique title, meta description, canonical URL" $soft $line
        Draw-Box $g 450 220 250 120 "Social Preview" "Open Graph, Twitter cards, optimized images" $soft $line
        Draw-Box $g 780 220 250 120 "Structured Data" "JSON-LD for tournaments, events, sports content" $soft $line
        Draw-Box $g 1110 220 250 120 "Indexing" "XML sitemap, robots.txt, internal links" $soft $line
        Draw-Arrow $g 370 280 450 280 $line
        Draw-Arrow $g 700 280 780 280 $line
        Draw-Arrow $g 1030 280 1110 280 $line
        Draw-Box $g 285 520 310 115 "Performance" "Lazy images, route splitting, compression, cache static content" $soft $line
        Draw-Box $g 735 520 310 115 "User Experience" "Skeleton loaders, prefetch, responsive images, accessibility" $soft $line
        Draw-Arrow $g 630 340 440 520 $line
        Draw-Arrow $g 930 340 890 520 $line
    }
