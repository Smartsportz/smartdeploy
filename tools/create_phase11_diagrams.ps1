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

New-Canvas (Join-Path $outDir "phase11_environment_strategy.png") `
    "Environment Strategy and Promotion Flow" `
    "Each environment owns isolated configuration, data stores, credentials, storage, and logging" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 110 250 250 110 "Development" "Local/dev config, sample data, isolated API keys" $black $gray $line $soft
        Draw-Box $g 470 250 250 110 "Testing" "Automated tests, disposable data, CI validation" $black $gray $line $soft
        Draw-Box $g 830 250 250 110 "Staging" "Production-like config, smoke tests, release approval" $black $gray $line $soft
        Draw-Box $g 1190 250 250 110 "Production" "Live traffic, protected secrets, backups, alerts" $black $gray $line $soft
        Draw-Box $g 300 520 280 100 "Isolation Rules" "Separate database, bucket, logs, keys, and secrets" $black $gray $line $soft
        Draw-Box $g 980 520 280 100 "Promotion Gate" "No production credentials in non-production environments" $black $gray $line $soft
        Draw-Arrow $g 360 305 470 305 $line
        Draw-Arrow $g 720 305 830 305 $line
        Draw-Arrow $g 1080 305 1190 305 $line
        Draw-Arrow $g 445 360 445 520 $line
        Draw-Arrow $g 970 360 1120 520 $line
    }

New-Canvas (Join-Path $outDir "phase11_cicd_pipeline.png") `
    "CI/CD Pipeline and Release Gates" `
    "Fail-fast validation moves code from pull request to staging, approval, and production deployment" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 75 230 205 100 "Pull Request" "Branch checks, review, protected main" $black $gray $line $soft
        Draw-Box $g 345 230 205 100 "Quality Gates" "Install, lint, type check, unit tests" $black $gray $line $soft
        Draw-Box $g 615 230 205 100 "Build & Scan" "Frontend, backend, integration, security scan" $black $gray $line $soft
        Draw-Box $g 885 230 205 100 "Package" "Docker images, tags, release artifacts" $black $gray $line $soft
        Draw-Box $g 1155 230 205 100 "Staging" "Deploy, smoke tests, verification" $black $gray $line $soft
        Draw-Box $g 660 510 240 100 "Approval" "Manual production approval and checklist" $black $gray $line $soft
        Draw-Box $g 1045 510 240 100 "Production" "Rolling or blue/green release, rollback-ready" $black $gray $line $soft
        Draw-Arrow $g 280 280 345 280 $line
        Draw-Arrow $g 550 280 615 280 $line
        Draw-Arrow $g 820 280 885 280 $line
        Draw-Arrow $g 1090 280 1155 280 $line
        Draw-Arrow $g 1260 330 790 510 $line
        Draw-Arrow $g 900 560 1045 560 $line
    }

New-Canvas (Join-Path $outDir "phase11_production_infrastructure.png") `
    "Production Infrastructure Topology" `
    "Nginx, Dockerized services, Postgres, Redis, storage, CDN, and Socket.IO scaling boundaries" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 230 210 100 "Users & CDN" "Static assets, cache, HTTPS-only access" $black $gray $line $soft
        Draw-Box $g 360 230 210 100 "Nginx" "TLS, HTTP/2, compression, security headers" $black $gray $line $soft
        Draw-Box $g 645 180 230 100 "Frontend" "Static app container or CDN artifact" $black $gray $line $soft
        Draw-Box $g 645 390 230 100 "Backend Pool" "Stateless API instances, health checks" $black $gray $line $soft
        Draw-Box $g 970 180 220 100 "PostgreSQL" "Backups, migrations, slow query monitoring" $black $gray $line $soft
        Draw-Box $g 970 390 220 100 "Redis" "Cache, sessions, queues, Socket.IO adapter" $black $gray $line $soft
        Draw-Box $g 1245 285 220 100 "Cloud Storage" "Uploads, signed URLs, lifecycle policies" $black $gray $line $soft
        Draw-Arrow $g 295 280 360 280 $line
        Draw-Arrow $g 570 260 645 230 $line
        Draw-Arrow $g 570 300 645 440 $line
        Draw-Arrow $g 875 230 970 230 $line
        Draw-Arrow $g 875 440 970 440 $line
        Draw-Arrow $g 875 420 1245 335 $line
    }

New-Canvas (Join-Path $outDir "phase11_observability_dr.png") `
    "Observability, Alerting, and Recovery Model" `
    "Structured telemetry and tested recovery processes protect live tournaments and payment operations" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 110 225 235 100 "Health Signals" "Latency, errors, CPU, memory, disk, sockets" $black $gray $line $soft
        Draw-Box $g 430 225 235 100 "Structured Logs" "App, access, auth, payment, score, jobs" $black $gray $line $soft
        Draw-Box $g 750 225 235 100 "Alerts" "Deploy, DB, Redis, webhooks, SSL, backups" $black $gray $line $soft
        Draw-Box $g 1070 225 235 100 "Operations Team" "Configurable channels and escalation" $black $gray $line $soft
        Draw-Box $g 310 505 250 100 "Backups" "Daily automation, PITR, verification" $black $gray $line $soft
        Draw-Box $g 710 505 250 100 "Recovery Runbooks" "RPO, RTO, restore drills, rollback plans" $black $gray $line $soft
        Draw-Box $g 1110 505 250 100 "Continuity" "Read-only mode, queue drain, maintenance windows" $black $gray $line $soft
        Draw-Arrow $g 345 275 430 275 $line
        Draw-Arrow $g 665 275 750 275 $line
        Draw-Arrow $g 985 275 1070 275 $line
        Draw-Arrow $g 560 555 710 555 $line
        Draw-Arrow $g 960 555 1110 555 $line
        Draw-Arrow $g 865 325 835 505 $line
    }
