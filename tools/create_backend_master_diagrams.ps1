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

New-Canvas (Join-Path $outDir "backend_master_topology.png") `
    "Smart Sportz Backend System Topology" `
    "Versioned REST APIs, Socket.IO, services, repositories, PostgreSQL, Redis, storage, jobs, and providers" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 220 230 100 "Clients" "Public web, admin portal, management portal, live views" $black $gray $line $soft
        Draw-Box $g 405 220 230 100 "API Gateway" "Express routes, middleware, validation, rate limits" $black $gray $line $soft
        Draw-Box $g 715 220 230 100 "Services" "Auth, RBAC, tournaments, payments, live score" $black $gray $line $soft
        Draw-Box $g 1025 220 230 100 "Repositories" "Prisma data access, transactions, query scopes" $black $gray $line $soft
        Draw-Box $g 280 500 250 100 "Socket.IO" "Rooms, live score, notifications, reconnect" $black $gray $line $soft
        Draw-Box $g 675 500 250 100 "Data Stores" "PostgreSQL, Redis, cloud storage" $black $gray $line $soft
        Draw-Box $g 1070 500 250 100 "External Providers" "Razorpay, email, SMS, WhatsApp, push" $black $gray $line $soft
        Draw-Arrow $g 325 270 405 270 $line
        Draw-Arrow $g 635 270 715 270 $line
        Draw-Arrow $g 945 270 1025 270 $line
        Draw-Arrow $g 1120 320 800 500 $line
        Draw-Arrow $g 520 320 405 500 $line
        Draw-Arrow $g 925 550 1070 550 $line
    }

New-Canvas (Join-Path $outDir "backend_clean_architecture_flow.png") `
    "Clean Architecture Request Flow" `
    "Every REST request moves through middleware, validation, controller, service, repository, and audit boundaries" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 70 245 200 95 "HTTP Request" "Route, method, payload, token" $black $gray $line $soft
        Draw-Box $g 330 245 200 95 "Middleware" "Auth, RBAC, rate limit, correlation ID" $black $gray $line $soft
        Draw-Box $g 590 245 200 95 "Validation" "Zod schema, params, query, body" $black $gray $line $soft
        Draw-Box $g 850 245 200 95 "Controller" "Request mapping, response shape" $black $gray $line $soft
        Draw-Box $g 1110 245 200 95 "Service" "Business rules, transactions, events" $black $gray $line $soft
        Draw-Box $g 460 520 230 95 "Repository" "Prisma queries, scopes, indexes" $black $gray $line $soft
        Draw-Box $g 830 520 230 95 "Audit & Logs" "Action log, errors, correlation trace" $black $gray $line $soft
        Draw-Arrow $g 270 292 330 292 $line
        Draw-Arrow $g 530 292 590 292 $line
        Draw-Arrow $g 790 292 850 292 $line
        Draw-Arrow $g 1050 292 1110 292 $line
        Draw-Arrow $g 1210 340 575 520 $line
        Draw-Arrow $g 1210 340 945 520 $line
    }

New-Canvas (Join-Path $outDir "backend_auth_rbac_flow.png") `
    "Authentication, RBAC, and Scope Enforcement" `
    "JWT, refresh tokens, roles, permissions, assigned tournament scope, and audit logs protect every action" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 240 210 95 "Login" "Password check, user status, session policy" $black $gray $line $soft
        Draw-Box $g 370 240 210 95 "Tokens" "JWT access, refresh token, rotation" $black $gray $line $soft
        Draw-Box $g 650 240 210 95 "RBAC" "Roles, permissions, action keys" $black $gray $line $soft
        Draw-Box $g 930 240 210 95 "Scope" "Organization, tournament, venue, sport" $black $gray $line $soft
        Draw-Box $g 1210 240 210 95 "Decision" "Allow, deny, log, error response" $black $gray $line $soft
        Draw-Box $g 405 520 230 95 "Security Events" "Failed login, lockout, token revoke" $black $gray $line $soft
        Draw-Box $g 865 520 230 95 "Audit Log" "User, module, entity, action, before/after" $black $gray $line $soft
        Draw-Arrow $g 300 287 370 287 $line
        Draw-Arrow $g 580 287 650 287 $line
        Draw-Arrow $g 860 287 930 287 $line
        Draw-Arrow $g 1140 287 1210 287 $line
        Draw-Arrow $g 475 335 520 520 $line
        Draw-Arrow $g 1035 335 980 520 $line
    }

New-Canvas (Join-Path $outDir "backend_registration_payment_flow.png") `
    "Registration, Payment, and Approval Backend Workflow" `
    "Registration rules, documents, Razorpay orders, webhook verification, approval, refunds, and notifications" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 75 235 210 100 "Registration API" "Team/player form, category, slot checks" $black $gray $line $soft
        Draw-Box $g 350 235 210 100 "Validation" "Rules, documents, coupon, eligibility" $black $gray $line $soft
        Draw-Box $g 625 235 210 100 "Payment Order" "Razorpay order, amount, currency, status" $black $gray $line $soft
        Draw-Box $g 900 235 210 100 "Webhook" "Signature verify, idempotency, status update" $black $gray $line $soft
        Draw-Box $g 1175 235 210 100 "Approval" "Approve, reject, waitlist, refund" $black $gray $line $soft
        Draw-Box $g 360 520 230 95 "Documents" "Upload, private URL, verification status" $black $gray $line $soft
        Draw-Box $g 815 520 230 95 "Post Actions" "Receipt, invoice, notification, audit" $black $gray $line $soft
        Draw-Arrow $g 285 285 350 285 $line
        Draw-Arrow $g 560 285 625 285 $line
        Draw-Arrow $g 835 285 900 285 $line
        Draw-Arrow $g 1110 285 1175 285 $line
        Draw-Arrow $g 455 335 475 520 $line
        Draw-Arrow $g 1280 335 930 520 $line
    }

New-Canvas (Join-Path $outDir "backend_live_score_event_flow.png") `
    "Live Score Event Processing Workflow" `
    "Authorized scoring events update immutable history, Redis live state, Socket.IO rooms, statistics, and results" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 70 235 205 100 "Score Command" "Start, score, foul, card, timeout, correction" $black $gray $line $soft
        Draw-Box $g 335 235 205 100 "Sport Adapter" "Validate match state and sport rules" $black $gray $line $soft
        Draw-Box $g 600 235 205 100 "Event Store" "MatchEvent, correction reason, audit trail" $black $gray $line $soft
        Draw-Box $g 865 235 205 100 "State Builder" "Score snapshot, stats, standings update" $black $gray $line $soft
        Draw-Box $g 1130 235 205 100 "Broadcast" "Socket rooms, public live UI, notifications" $black $gray $line $soft
        Draw-Box $g 455 520 230 95 "Redis Cache" "Current score, timer, active match state" $black $gray $line $soft
        Draw-Box $g 830 520 230 95 "Reports" "Results, leaderboards, match analytics" $black $gray $line $soft
        Draw-Arrow $g 275 285 335 285 $line
        Draw-Arrow $g 540 285 600 285 $line
        Draw-Arrow $g 805 285 865 285 $line
        Draw-Arrow $g 1070 285 1130 285 $line
        Draw-Arrow $g 950 335 570 520 $line
        Draw-Arrow $g 970 335 945 520 $line
    }

New-Canvas (Join-Path $outDir "backend_jobs_observability_flow.png") `
    "Jobs, Notifications, Logging, and Operations Flow" `
    "Background workers, queues, structured logs, alerts, backups, and health checks support production behavior" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 230 220 100 "Domain Events" "Payment paid, match ended, registration approved" $black $gray $line $soft
        Draw-Box $g 380 230 220 100 "Queues & Jobs" "Email, SMS, reports, exports, cleanup" $black $gray $line $soft
        Draw-Box $g 670 230 220 100 "Notifications" "Templates, channels, retries, delivery log" $black $gray $line $soft
        Draw-Box $g 960 230 220 100 "Observability" "Structured logs, metrics, correlation IDs" $black $gray $line $soft
        Draw-Box $g 1250 230 220 100 "Alerts" "Errors, webhooks, DB, Redis, backups" $black $gray $line $soft
        Draw-Box $g 390 515 240 95 "Maintenance" "Queue drain, cache warm, read-only mode" $black $gray $line $soft
        Draw-Box $g 850 515 240 95 "Recovery" "Backups, restore drills, rollback plans" $black $gray $line $soft
        Draw-Arrow $g 310 280 380 280 $line
        Draw-Arrow $g 600 280 670 280 $line
        Draw-Arrow $g 890 280 960 280 $line
        Draw-Arrow $g 1180 280 1250 280 $line
        Draw-Arrow $g 490 330 510 515 $line
        Draw-Arrow $g 1070 330 970 515 $line
    }
