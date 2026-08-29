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
    $soft = [System.Drawing.Color]::FromArgb(245,245,245)

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

    $fontT = New-Object System.Drawing.Font("Times New Roman", 21, [System.Drawing.FontStyle]::Bold)
    $fontB = New-Object System.Drawing.Font("Times New Roman", 16, [System.Drawing.FontStyle]::Regular)
    $blackBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(18,18,18))
    $grayBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(70,70,70))
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = [System.Drawing.RectangleF]::new([float]($x + 12), [float]($y + 14), [float]($w - 24), [float]34)
    $bodyRect = [System.Drawing.RectangleF]::new([float]($x + 18), [float]($y + 52), [float]($w - 36), [float]($h - 64))
    $g.DrawString($title, $fontT, $blackBrush, $titleRect, $sf)
    $g.DrawString($body, $fontB, $grayBrush, $bodyRect, $sf)
}

function Draw-Arrow($g, $x1, $y1, $x2, $y2, $color) {
    $pen = New-Object System.Drawing.Pen($color, 3)
    $cap = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(6, 7)
    $pen.CustomEndCap = $cap
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
}

New-Canvas (Join-Path $outDir "phase2_design_system_workflow.png") `
    "Design System Workflow" `
    "From brand language to reusable product UI" `
    {
        param($g, $black, $gray, $line, $soft)
        $fill = [System.Drawing.Color]::FromArgb(248,248,248)
        $boxes = @(
            @(80,230,215,150,"Brand","Energy`nPrecision`nTrust"),
            @(340,230,215,150,"Tokens","Colors`nType`nSpacing"),
            @(600,230,215,150,"Components","Buttons`nCards`nForms"),
            @(860,230,215,150,"Sections","Hero`nTicker`nGallery"),
            @(1120,230,215,150,"Portals","Public`nAdmin`nManager")
        )
        foreach($b in $boxes){ Draw-Box $g $b[0] $b[1] $b[2] $b[3] $b[4] $b[5] $fill $line }
        Draw-Arrow $g 295 305 340 305 $line
        Draw-Arrow $g 555 305 600 305 $line
        Draw-Arrow $g 815 305 860 305 $line
        Draw-Arrow $g 1075 305 1120 305 $line
        Draw-Box $g 420 520 760 135 "Quality Gate" "Accessibility, responsive behavior, loading states, empty states, error states, animation consistency, and performance checks" $fill $line
        Draw-Arrow $g 1225 380 870 520 $line
    }

New-Canvas (Join-Path $outDir "phase2_landing_page_architecture.png") `
    "Landing Page Architecture" `
    "A premium SaaS homepage with sports-tech conversion flow" `
    {
        param($g, $black, $gray, $line, $soft)
        $fill = [System.Drawing.Color]::FromArgb(248,248,248)
        Draw-Box $g 95 195 330 105 "Navigation" "Sticky rounded nav, logo, links, admin login, CTA" $fill $line
        Draw-Box $g 95 340 330 125 "Hero" "Headline, subheading, CTAs, floating dashboard preview" $fill $line
        Draw-Box $g 95 505 330 100 "Live Ticker" "Scrolling live tournament updates" $fill $line
        Draw-Box $g 510 195 330 105 "Discovery" "Featured tournaments, sports categories, upcoming events" $fill $line
        Draw-Box $g 510 340 330 125 "Trust" "Stats, sponsors, testimonials, FAQ" $fill $line
        Draw-Box $g 510 505 330 100 "Engagement" "Gallery, newsletter, contact, map" $fill $line
        Draw-Box $g 925 255 330 150 "Conversion" "Register Tournament, Explore Live Matches, View Details, Contact Organizer" $fill $line
        Draw-Box $g 925 475 330 105 "Footer" "Company, products, support, legal, social, policies" $fill $line
        Draw-Arrow $g 425 247 510 247 $line
        Draw-Arrow $g 425 402 510 402 $line
        Draw-Arrow $g 425 555 510 555 $line
        Draw-Arrow $g 840 325 925 325 $line
        Draw-Arrow $g 840 555 925 530 $line
    }

New-Canvas (Join-Path $outDir "phase2_dashboard_layout.png") `
    "Dashboard UI Structure" `
    "Shared interface language for admin and management portals" `
    {
        param($g, $black, $gray, $line, $soft)
        $fill = [System.Drawing.Color]::FromArgb(248,248,248)
        Draw-Box $g 90 205 250 430 "Sidebar" "Collapsible navigation`nModules`nPermissions`nProfile" $fill $line
        Draw-Box $g 390 205 850 80 "Top Bar" "Breadcrumbs, search, notification center, user menu" $fill $line
        Draw-Box $g 390 330 245 130 "KPI Cards" "Revenue`nLive matches`nRegistrations" $fill $line
        Draw-Box $g 690 330 245 130 "Charts" "Participation`nPayments`nTournament trends" $fill $line
        Draw-Box $g 995 330 245 130 "Quick Actions" "Create`nApprove`nPublish" $fill $line
        Draw-Box $g 390 510 850 145 "Data Table" "Search, filter, sort, pagination, bulk actions, export" $fill $line
        Draw-Arrow $g 340 420 390 420 $line
        Draw-Arrow $g 815 285 815 330 $line
        Draw-Arrow $g 815 460 815 510 $line
    }
