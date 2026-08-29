Add-Type -AssemblyName System.Drawing

$root = Join-Path (Get-Location) "stitch_remix_of_smartsportz_enterprise_saas_platform"
$outDir = Join-Path (Get-Location) "docs\assets"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

function New-ContactSheet {
    param(
        [string]$Output,
        [string]$Title,
        [array]$Items
    )

    $w = 1600
    $thumbW = 360
    $thumbH = 360
    $gap = 34
    $marginX = 70
    $top = 150
    $cols = 4
    $rows = [Math]::Ceiling($Items.Count / $cols)
    $h = [int]($top + ($rows * ($thumbH + 84)) + 48)

    $bmp = New-Object System.Drawing.Bitmap($w, $h)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::ClearTypeGridFit
    $white = [System.Drawing.Color]::White
    $black = [System.Drawing.Color]::FromArgb(18,18,18)
    $gray = [System.Drawing.Color]::FromArgb(80,80,80)
    $line = [System.Drawing.Color]::FromArgb(35,35,35)
    $soft = [System.Drawing.Color]::FromArgb(248,248,248)
    $g.Clear($white)

    $fontTitle = New-Object System.Drawing.Font("Times New Roman", 30, [System.Drawing.FontStyle]::Bold)
    $fontLabel = New-Object System.Drawing.Font("Times New Roman", 15, [System.Drawing.FontStyle]::Bold)
    $fontSmall = New-Object System.Drawing.Font("Times New Roman", 11, [System.Drawing.FontStyle]::Regular)
    $brushBlack = New-Object System.Drawing.SolidBrush($black)
    $brushGray = New-Object System.Drawing.SolidBrush($gray)
    $brushSoft = New-Object System.Drawing.SolidBrush($soft)
    $pen = New-Object System.Drawing.Pen($line, 3)
    $thinPen = New-Object System.Drawing.Pen($line, 1)

    $g.DrawString($Title, $fontTitle, $brushBlack, 70, 42)
    $g.DrawLine($pen, 70, 112, 1530, 112)

    for ($i = 0; $i -lt $Items.Count; $i++) {
        $item = $Items[$i]
        $col = $i % $cols
        $row = [Math]::Floor($i / $cols)
        $x = $marginX + ($col * ($thumbW + $gap))
        $y = $top + ($row * ($thumbH + 84))

        $screen = Join-Path (Join-Path $root $item.Folder) "screen.png"
        $img = [System.Drawing.Image]::FromFile($screen)
        $scale = [Math]::Min($thumbW / $img.Width, $thumbH / $img.Height)
        $drawW = [int]($img.Width * $scale)
        $drawH = [int]($img.Height * $scale)
        $dx = [int]($x + (($thumbW - $drawW) / 2))
        $dy = [int]($y + (($thumbH - $drawH) / 2))

        $g.FillRectangle($brushSoft, $x, $y, $thumbW, $thumbH)
        $g.DrawRectangle($thinPen, $x, $y, $thumbW, $thumbH)
        $g.DrawImage($img, $dx, $dy, $drawW, $drawH)
        $img.Dispose()

        $labelRect = New-Object System.Drawing.RectangleF($x, ($y + $thumbH + 12), $thumbW, 24)
        $noteRect = New-Object System.Drawing.RectangleF($x, ($y + $thumbH + 38), $thumbW, 40)
        $sf = New-Object System.Drawing.StringFormat
        $sf.Alignment = [System.Drawing.StringAlignment]::Center
        $sf.LineAlignment = [System.Drawing.StringAlignment]::Near
        $g.DrawString($item.Label, $fontLabel, $brushBlack, $labelRect, $sf)
        $g.DrawString($item.Note, $fontSmall, $brushGray, $noteRect, $sf)
    }

    $bmp.Save($Output, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

$public = @(
    @{Folder="smartsportz_premium_landing_page_light"; Label="Landing - Light"; Note="Canonical public landing"},
    @{Folder="smartsportz_premium_landing_page"; Label="Landing - Dark Variant"; Note="Marketing variant reference"},
    @{Folder="tournament_listing_page"; Label="Tournaments"; Note="Public tournament discovery"},
    @{Folder="tournament_detail_page"; Label="Tournament Detail"; Note="Public detail and CTA"},
    @{Folder="sports_categories_explorer"; Label="Sports Categories"; Note="Sports browsing hub"},
    @{Folder="about_smartsportz_our_story_mission"; Label="About"; Note="Story and mission page"},
    @{Folder="premium_contact_center"; Label="Contact"; Note="Support/contact hub"},
    @{Folder="premium_sponsorship_center"; Label="Sponsors"; Note="Sponsorship showcase"}
)

$content = @(
    @{Folder="professional_sports_media_gallery"; Label="Media Gallery"; Note="Public gallery and filters"},
    @{Folder="professional_sports_news_blog"; Label="News Blog"; Note="Insights listing"},
    @{Folder="premium_article_detail_page"; Label="Article Detail"; Note="Long-form content page"},
    @{Folder="professional_faq_center"; Label="FAQ Center"; Note="Help knowledge base"},
    @{Folder="minimal_premium_login_page"; Label="Login"; Note="Premium auth entry"},
    @{Folder="interactive_password_recovery_flow"; Label="Password Recovery"; Note="Interactive recovery flow"},
    @{Folder="refined_premium_password_recovery"; Label="Recovery Variant"; Note="Refined auth variant"},
    @{Folder="smartsportz_enterprise_footer_showcase"; Label="Footer"; Note="Enterprise footer system"}
)

$tournament = @(
    @{Folder="professional_tournament_registration"; Label="Registration"; Note="Tournament signup flow"},
    @{Folder="03_one_tournament_card"; Label="Tournament Card"; Note="Reusable tournament card"},
    @{Folder="07_live_tournaments_hub"; Label="Live Hub"; Note="Active tournament hub"},
    @{Folder="smartsportz_live_match_center"; Label="Live Match Center"; Note="Public live match center"},
    @{Folder="06_tournaments_live_match"; Label="Live Match"; Note="Tournament live match detail"},
    @{Folder="live_score_dashboard_premium_dark"; Label="Score Dashboard"; Note="Dark scoring dashboard"},
    @{Folder="professional_leaderboard_center"; Label="Leaderboard"; Note="Rankings and results"},
    @{Folder="professional_team_directory"; Label="Team Directory"; Note="Teams and search"}
)

$dashboard = @(
    @{Folder="01_user_dashboard"; Label="User Dashboard"; Note="Athlete/user dashboard"},
    @{Folder="professional_user_dashboard_1"; Label="Dashboard Variant 1"; Note="Performance dashboard"},
    @{Folder="professional_user_dashboard_2"; Label="Dashboard Variant 2"; Note="Elite dashboard variant"},
    @{Folder="04_analysis_dashboard"; Label="Admin Analytics"; Note="Enterprise admin analytics"},
    @{Folder="tournament_management"; Label="Management"; Note="Tournament management portal"},
    @{Folder="05_teams_and_players"; Label="Teams + Players"; Note="Player/team operations"},
    @{Folder="professional_athlete_profile"; Label="Athlete Profile"; Note="Player profile detail"},
    @{Folder="02_tournaments"; Label="Internal Tournaments"; Note="Dashboard tournament list"}
)

New-ContactSheet (Join-Path $outDir "remix_public_pages_contact_sheet.png") "Smart Sportz Remix UI - Public Website Pages" $public
New-ContactSheet (Join-Path $outDir "remix_content_auth_contact_sheet.png") "Smart Sportz Remix UI - Content and Authentication Pages" $content
New-ContactSheet (Join-Path $outDir "remix_tournament_live_contact_sheet.png") "Smart Sportz Remix UI - Tournament and Live Pages" $tournament
New-ContactSheet (Join-Path $outDir "remix_dashboard_operations_contact_sheet.png") "Smart Sportz Remix UI - Dashboard and Operations Pages" $dashboard
