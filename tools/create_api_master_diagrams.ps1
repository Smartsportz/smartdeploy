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
    $fontTitle = New-Object System.Drawing.Font("Times New Roman", 31, [System.Drawing.FontStyle]::Bold)
    $fontSub = New-Object System.Drawing.Font("Times New Roman", 16, [System.Drawing.FontStyle]::Regular)
    $g.DrawString($title, $fontTitle, (New-Object System.Drawing.SolidBrush($black)), 70, 42)
    $g.DrawString($subtitle, $fontSub, (New-Object System.Drawing.SolidBrush($gray)), 72, 96)
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
    $fontHead = New-Object System.Drawing.Font("Times New Roman", 15, [System.Drawing.FontStyle]::Bold)
    $fontBody = New-Object System.Drawing.Font("Times New Roman", 11.5, [System.Drawing.FontStyle]::Regular)
    $sf = New-Object System.Drawing.StringFormat
    $sf.Alignment = [System.Drawing.StringAlignment]::Center
    $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
    $titleRect = New-Object System.Drawing.RectangleF(($x + 10), ($y + 8), ($w - 20), 31)
    $bodyRect = New-Object System.Drawing.RectangleF(($x + 12), ($y + 42), ($w - 24), ($h - 48))
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
    $pen.EndCap = [System.Drawing.Drawing2D.LineCap]::ArrowAnchor
    $g.DrawLine($pen, $x1, $y1, $x2, $y2)
}

New-Canvas (Join-Path $outDir "api_ecosystem_overview.png") `
    "Smart Sportz API Ecosystem Overview" `
    "Frontend pages call internal APIs; backend modules connect databases, Redis, sockets, jobs, and external providers" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 240 230 105 "Frontend Apps" "Public website, auth, super admin, management portal" $black $gray $line $soft
        Draw-Box $g 385 240 240 105 "API Gateway" "REST /api/v1, auth guard, RBAC, validation, rate limit" $black $gray $line $soft
        Draw-Box $g 710 185 230 100 "Service Layer" "Tournament, user, match, payment, CMS, notification" $black $gray $line $soft
        Draw-Box $g 710 410 230 100 "Socket.IO" "Live score, match events, dashboards, public broadcast" $black $gray $line $soft
        Draw-Box $g 1015 185 230 100 "Data Layer" "DB-1 primary, DB-2 mirror, DB-3 logs, Redis" $black $gray $line $soft
        Draw-Box $g 1015 410 230 100 "External APIs" "Payments, SMS, email, WhatsApp, push, files, maps, AI" $black $gray $line $soft
        Draw-Box $g 1300 300 190 95 "Webhooks" "Razorpay, WhatsApp, email, storage callbacks" $black $gray $line $soft
        Draw-Arrow $g 315 292 385 292 $line
        Draw-Arrow $g 625 292 710 235 $line
        Draw-Arrow $g 625 292 710 460 $line
        Draw-Arrow $g 940 235 1015 235 $line
        Draw-Arrow $g 940 460 1015 460 $line
        Draw-Arrow $g 1245 460 1300 348 $line
        Draw-Arrow $g 1300 325 625 325 $line
    }

New-Canvas (Join-Path $outDir "api_external_provider_flow.png") `
    "External API Provider Flow" `
    "Provider credentials stay on the server; webhooks are verified before DB writes and user notifications" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 245 210 100 "User Action" "Register, pay, OTP, upload, subscribe, contact" $black $gray $line $soft
        Draw-Box $g 350 245 220 100 "Internal API" "Validate request, RBAC, idempotency, audit context" $black $gray $line $soft
        Draw-Box $g 635 175 230 96 "Payment API" "Razorpay order, payment, refund, invoice" $black $gray $line $soft
        Draw-Box $g 635 325 230 96 "Messaging APIs" "SMS, WhatsApp, email, push notification" $black $gray $line $soft
        Draw-Box $g 935 175 230 96 "Media / Maps / AI" "Cloudinary/S3, Google Maps, OpenAI" $black $gray $line $soft
        Draw-Box $g 935 325 230 96 "Provider Webhook" "Signed callback, status update, retry-safe event" $black $gray $line $soft
        Draw-Box $g 1235 250 230 105 "DB + Logs" "DB-1 state, DB-2 mirror, DB-3 audit/log event" $black $gray $line $soft
        Draw-Arrow $g 290 295 350 295 $line
        Draw-Arrow $g 570 292 635 222 $line
        Draw-Arrow $g 570 292 635 372 $line
        Draw-Arrow $g 865 222 935 222 $line
        Draw-Arrow $g 865 372 935 372 $line
        Draw-Arrow $g 1165 372 1235 302 $line
        Draw-Arrow $g 1165 222 1235 302 $line
    }

New-Canvas (Join-Path $outDir "api_internal_module_map.png") `
    "Internal API Module Map" `
    "REST modules are grouped by domain, use service/repository layers, and share security middleware" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 200 210 95 "Auth" "login, OTP, refresh, logout, password reset" $black $gray $line $soft
        Draw-Box $g 365 200 210 95 "Admin" "users, roles, permissions, settings, audit" $black $gray $line $soft
        Draw-Box $g 645 200 210 95 "Tournament" "sports, venues, categories, fixtures, brackets" $black $gray $line $soft
        Draw-Box $g 925 200 210 95 "Registration" "teams, players, documents, approval, waitlist" $black $gray $line $soft
        Draw-Box $g 1205 200 210 95 "Payment" "orders, webhooks, refunds, invoices, receipts" $black $gray $line $soft
        Draw-Box $g 225 500 210 95 "Live Score" "matches, events, stats, timeline, sockets" $black $gray $line $soft
        Draw-Box $g 505 500 210 95 "CMS" "pages, sections, sponsors, gallery, FAQs, blogs" $black $gray $line $soft
        Draw-Box $g 785 500 210 95 "Notification" "email, SMS, WhatsApp, push, templates" $black $gray $line $soft
        Draw-Box $g 1065 500 210 95 "Reports" "dashboards, exports, analytics, logs" $black $gray $line $soft
        Draw-Arrow $g 295 248 365 248 $line
        Draw-Arrow $g 575 248 645 248 $line
        Draw-Arrow $g 855 248 925 248 $line
        Draw-Arrow $g 1135 248 1205 248 $line
        Draw-Arrow $g 750 295 330 500 $line
        Draw-Arrow $g 750 295 610 500 $line
        Draw-Arrow $g 1030 295 890 500 $line
        Draw-Arrow $g 1310 295 1170 500 $line
    }

New-Canvas (Join-Path $outDir "api_auth_payment_workflow.png") `
    "Auth, Registration, Payment, and Notification Workflow" `
    "The critical user journey moves from secure login to registration approval, payment, webhooks, and confirmation" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 70 260 190 96 "Login / OTP" "JWT, refresh token, session in Redis" $black $gray $line $soft
        Draw-Box $g 320 260 190 96 "Registration" "team/player form, files, validation" $black $gray $line $soft
        Draw-Box $g 570 260 190 96 "Approval" "manager/admin review, status change" $black $gray $line $soft
        Draw-Box $g 820 260 190 96 "Payment" "Razorpay order, checkout, receipt" $black $gray $line $soft
        Draw-Box $g 1070 260 190 96 "Webhook" "verify signature, update payment status" $black $gray $line $soft
        Draw-Box $g 1320 260 190 96 "Notify" "email, SMS, WhatsApp, push" $black $gray $line $soft
        Draw-Box $g 420 500 250 95 "Database Writes" "DB-1 transaction, DB-2 mirror, DB-3 audit event" $black $gray $line $soft
        Draw-Box $g 890 500 250 95 "Live Dashboards" "admin counters, management approvals, public status" $black $gray $line $soft
        Draw-Arrow $g 260 308 320 308 $line
        Draw-Arrow $g 510 308 570 308 $line
        Draw-Arrow $g 760 308 820 308 $line
        Draw-Arrow $g 1010 308 1070 308 $line
        Draw-Arrow $g 1260 308 1320 308 $line
        Draw-Arrow $g 665 356 545 500 $line
        Draw-Arrow $g 1165 356 1015 500 $line
    }

New-Canvas (Join-Path $outDir "api_page_to_endpoint_map.png") `
    "Frontend Page to Internal Endpoint Map" `
    "Each visible page owns a focused API surface, with common auth, RBAC, pagination, filtering, and audit behavior" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 190 225 95 "Public Pages" "home, tournaments, gallery, blog, contact" $black $gray $line $soft
        Draw-Box $g 385 190 225 95 "Auth Pages" "login, forgot, OTP, reset, remember me" $black $gray $line $soft
        Draw-Box $g 685 190 225 95 "Registration Pages" "team/player entry, upload, payment, status" $black $gray $line $soft
        Draw-Box $g 985 190 225 95 "Admin Pages" "dashboard, users, tournaments, CMS, reports" $black $gray $line $soft
        Draw-Box $g 1285 190 225 95 "Management Pages" "live score, match control, approvals, reports" $black $gray $line $soft
        Draw-Box $g 205 500 250 95 "/api/v1/public/*" "published content, public tournament data" $black $gray $line $soft
        Draw-Box $g 515 500 250 95 "/api/v1/auth/*" "credentials, OTP, tokens, sessions" $black $gray $line $soft
        Draw-Box $g 825 500 250 95 "/api/v1/registrations/*" "forms, documents, checkout, approvals" $black $gray $line $soft
        Draw-Box $g 1135 500 250 95 "/api/v1/admin/*" "RBAC-protected operations and exports" $black $gray $line $soft
        Draw-Arrow $g 198 285 330 500 $line
        Draw-Arrow $g 498 285 640 500 $line
        Draw-Arrow $g 798 285 950 500 $line
        Draw-Arrow $g 1098 285 1260 500 $line
        Draw-Arrow $g 1398 285 1260 500 $line
    }
