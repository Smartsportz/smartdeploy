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

New-Canvas (Join-Path $outDir "phase8_backend_topology.png") `
    "Backend Architecture Topology" `
    "Node.js, Express, Socket.IO, PostgreSQL, Redis, storage, payments, notifications, and jobs" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 220 230 115 "Clients" "Public website, admin portal, management portal, Smart TV display" $soft $line
        Draw-Box $g 380 220 250 115 "Express API" "Versioned REST routes, middleware, controllers" $soft $line
        Draw-Box $g 705 220 250 115 "Service Layer" "Business rules, transactions, orchestration" $soft $line
        Draw-Box $g 1030 185 230 105 "Repositories" "Prisma data access and query isolation" $soft $line
        Draw-Box $g 1300 185 215 105 "PostgreSQL" "Primary relational database" $soft $line
        Draw-Box $g 1030 345 230 105 "Redis Cache" "Live scores, match state, leaderboards" $soft $line
        Draw-Box $g 705 545 250 110 "Socket.IO" "/live, /admin, /management namespaces" $soft $line
        Draw-Box $g 1030 545 230 110 "External Services" "Razorpay, Cloudinary or S3, Email, SMS, WhatsApp" $soft $line
        Draw-Box $g 1300 545 215 110 "Jobs" "Reports, retries, backups, reminders, waitlist" $soft $line
        Draw-Arrow $g 310 277 380 277 $line
        Draw-Arrow $g 630 277 705 277 $line
        Draw-Arrow $g 955 260 1030 235 $line
        Draw-Arrow $g 1260 235 1300 235 $line
        Draw-Arrow $g 955 292 1030 395 $line
        Draw-Arrow $g 830 335 830 545 $line
        Draw-Arrow $g 955 600 1030 600 $line
        Draw-Arrow $g 1260 600 1300 600 $line
    }

New-Canvas (Join-Path $outDir "phase8_clean_architecture_flow.png") `
    "Clean Architecture Request Flow" `
    "Thin controllers, validated input, service-owned business rules, repositories, Prisma, and PostgreSQL" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 250 205 105 "Client" "HTTP request or internal command" $soft $line
        Draw-Box $g 345 250 205 105 "Route" "Express route and middleware chain" $soft $line
        Draw-Box $g 600 250 205 105 "Controller" "Thin request/response adapter" $soft $line
        Draw-Box $g 855 250 205 105 "Validation" "Zod schema, DTO, field-level errors" $soft $line
        Draw-Box $g 1110 250 205 105 "Service" "Business rules and transactions" $soft $line
        Draw-Box $g 345 520 205 105 "Repository" "Query construction and persistence" $soft $line
        Draw-Box $g 600 520 205 105 "Prisma ORM" "Typed database client" $soft $line
        Draw-Box $g 855 520 205 105 "PostgreSQL" "Durable system of record" $soft $line
        Draw-Box $g 1110 520 205 105 "Response" "Consistent success or error shape" $soft $line
        Draw-Arrow $g 295 302 345 302 $line
        Draw-Arrow $g 550 302 600 302 $line
        Draw-Arrow $g 805 302 855 302 $line
        Draw-Arrow $g 1060 302 1110 302 $line
        Draw-Arrow $g 1215 355 448 520 $line
        Draw-Arrow $g 550 572 600 572 $line
        Draw-Arrow $g 805 572 855 572 $line
        Draw-Arrow $g 1060 572 1110 572 $line
    }

New-Canvas (Join-Path $outDir "phase8_auth_rbac_pipeline.png") `
    "Authentication and RBAC Pipeline" `
    "Every request is authenticated, authorized, scoped, validated, executed, and audited" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 235 220 110 "Request" "JWT access token, route, method, resource" $soft $line
        Draw-Box $g 365 235 220 110 "Auth Guard" "Verify token, session, refresh/logout state" $soft $line
        Draw-Box $g 640 235 220 110 "Permission" "Role, permission, module, action" $soft $line
        Draw-Box $g 915 235 220 110 "Ownership" "Tournament, venue, sport, organization scope" $soft $line
        Draw-Box $g 1190 235 220 110 "Controller" "Execute only after all guards pass" $soft $line
        Draw-Box $g 365 520 270 115 "Denied" "401/403 response, no business action" $soft $line
        Draw-Box $g 790 520 270 115 "Audit" "Permission failures and critical actions" $soft $line
        Draw-Box $g 1190 520 270 115 "Super Admin Config" "Roles and permissions are configurable" $soft $line
        Draw-Arrow $g 310 290 365 290 $line
        Draw-Arrow $g 585 290 640 290 $line
        Draw-Arrow $g 860 290 915 290 $line
        Draw-Arrow $g 1135 290 1190 290 $line
        Draw-Arrow $g 475 345 500 520 $line
        Draw-Arrow $g 1025 345 925 520 $line
        Draw-Arrow $g 1325 345 1325 520 $line
    }

New-Canvas (Join-Path $outDir "phase8_event_processing_pipeline.png") `
    "Event Processing and Integration Pipeline" `
    "Live actions, payments, notifications, jobs, Redis updates, and Socket.IO broadcasts" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 230 230 115 "Client Action" "Live score event, payment, upload, report, notification" $soft $line
        Draw-Box $g 375 230 230 115 "API + Validation" "Zod schemas, auth, idempotency, business checks" $soft $line
        Draw-Box $g 665 230 230 115 "Database" "Prisma transaction, audit log, immutable events" $soft $line
        Draw-Box $g 955 230 230 115 "Redis Update" "Write-through cache and invalidation" $soft $line
        Draw-Box $g 1245 230 230 115 "Broadcast" "Socket.IO rooms, changed data only" $soft $line
        Draw-Box $g 375 520 270 115 "Queue / Jobs" "Retries, reminders, reports, backup, waitlist" $soft $line
        Draw-Box $g 805 520 270 115 "External Providers" "Razorpay, S3 or Cloudinary, Email, SMS, WhatsApp" $soft $line
        Draw-Box $g 1210 520 270 115 "Observability" "Structured logs, correlation IDs, errors" $soft $line
        Draw-Arrow $g 315 287 375 287 $line
        Draw-Arrow $g 605 287 665 287 $line
        Draw-Arrow $g 895 287 955 287 $line
        Draw-Arrow $g 1185 287 1245 287 $line
        Draw-Arrow $g 780 345 510 520 $line
        Draw-Arrow $g 780 345 940 520 $line
        Draw-Arrow $g 1360 345 1345 520 $line
    }
