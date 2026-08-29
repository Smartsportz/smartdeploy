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

New-Canvas (Join-Path $outDir "phase5_admin_shell_layout.png") `
    "Super Admin Shell Layout" `
    "Cloud console structure for navigation, search, alerts, and module workspaces" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 185 1410 85 "Top Navigation" "Global search, quick actions, notifications, live match indicator, theme toggle, profile, settings, organization switcher" $soft $line
        Draw-Box $g 95 320 280 390 "Left Sidebar" "Dashboard, tournaments, registration, finance, users, master data, website, reports, settings" $soft $line
        Draw-Box $g 430 320 455 165 "Dashboard Workspace" "KPI cards, charts, activity feed, pending approvals, quick actions" $soft $line
        Draw-Box $g 940 320 565 165 "Data Management Workspace" "Searchable tables, filters, drawers, forms, modals, export, bulk actions" $soft $line
        Draw-Box $g 430 545 455 165 "Control Workflows" "Publish, approve, refund, suspend, archive, duplicate, notify" $soft $line
        Draw-Box $g 940 545 565 165 "Observability" "Audit logs, security history, reports, scheduled exports, versioned settings" $soft $line
        Draw-Arrow $g 235 270 235 320 $line
        Draw-Arrow $g 375 515 430 405 $line
        Draw-Arrow $g 375 515 430 625 $line
    }

New-Canvas (Join-Path $outDir "phase5_super_admin_module_map.png") `
    "Super Admin Module Map" `
    "Core ownership areas controlled from the Super Admin portal" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 650 325 300 135 "Super Admin" "Highest authority across platform, organizations, tournaments, users, finance, CMS, reports, and settings" $soft $line
        Draw-Box $g 110 205 230 110 "Tournaments" "Create, publish, fixtures, matches, live results" $soft $line
        Draw-Box $g 420 205 230 110 "Users & RBAC" "Management users, roles, permissions, audit logs" $soft $line
        Draw-Box $g 950 205 230 110 "Finance" "Payments, refunds, coupons, revenue" $soft $line
        Draw-Box $g 1260 205 230 110 "Master Data" "Sports, venues, categories, organizations" $soft $line
        Draw-Box $g 110 555 230 110 "Website CMS" "Hero, gallery, sponsors, blogs, FAQs, contact" $soft $line
        Draw-Box $g 420 555 230 110 "Notifications" "Email, SMS, WhatsApp, push, templates" $soft $line
        Draw-Box $g 950 555 230 110 "Reports" "Tournament, financial, participation, custom" $soft $line
        Draw-Box $g 1260 555 230 110 "System" "Security, integrations, backup, maintenance" $soft $line
        Draw-Arrow $g 650 350 340 260 $line
        Draw-Arrow $g 690 325 650 260 $line
        Draw-Arrow $g 950 350 1065 315 $line
        Draw-Arrow $g 950 390 1260 260 $line
        Draw-Arrow $g 650 435 340 610 $line
        Draw-Arrow $g 690 460 650 610 $line
        Draw-Arrow $g 950 435 1065 555 $line
        Draw-Arrow $g 950 390 1260 610 $line
    }

New-Canvas (Join-Path $outDir "phase5_rbac_permission_model.png") `
    "Azure-Style RBAC Permission Model" `
    "Granular permissions with reusable templates and scoped assignments" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 115 230 235 120 "User" "Management user profile, department, employee ID, status" $soft $line
        Draw-Box $g 430 230 235 120 "Role" "Tournament manager, finance officer, live score manager, read only, custom" $soft $line
        Draw-Box $g 745 230 235 120 "Permission Group" "Reusable bundles with inheritance support" $soft $line
        Draw-Box $g 1060 230 235 120 "Permission" "Create, view, edit, delete, publish, approve, refund, export" $soft $line
        Draw-Box $g 615 520 335 125 "Scope" "Tournament, sport, venue, organization, module, or global system access" $soft $line
        Draw-Box $g 1060 520 335 125 "Enforcement" "Route guards, API middleware, query filters, audit logging" $soft $line
        Draw-Arrow $g 350 290 430 290 $line
        Draw-Arrow $g 665 290 745 290 $line
        Draw-Arrow $g 980 290 1060 290 $line
        Draw-Arrow $g 860 350 785 520 $line
        Draw-Arrow $g 950 585 1060 585 $line
    }

New-Canvas (Join-Path $outDir "phase5_admin_action_audit_flow.png") `
    "Admin Action, Audit, and Settings Flow" `
    "Every sensitive action is authorized, confirmed, executed, logged, and reported" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 230 225 115 "Admin Action" "Create, update, delete, publish, approve, refund, permission change" $soft $line
        Draw-Box $g 365 230 225 115 "RBAC Check" "Verify role, permission, scope, and active status" $soft $line
        Draw-Box $g 650 230 225 115 "Confirmation" "Required for destructive and financial actions" $soft $line
        Draw-Box $g 935 230 225 115 "Service Layer" "Validate, execute transaction, update domain records" $soft $line
        Draw-Box $g 1220 230 225 115 "Audit Log" "Timestamp, user, action, module, old/new values, IP, device" $soft $line
        Draw-Box $g 365 520 285 120 "Versioned Settings" "Payment, email, SMS, WhatsApp, integrations, security, maintenance" $soft $line
        Draw-Box $g 775 520 285 120 "Notifications" "Send targeted messages, templates, scheduling, delivery status" $soft $line
        Draw-Box $g 1185 520 285 120 "Reports & Exports" "PDF, Excel, CSV, scheduled email delivery" $soft $line
        Draw-Arrow $g 305 290 365 290 $line
        Draw-Arrow $g 590 290 650 290 $line
        Draw-Arrow $g 875 290 935 290 $line
        Draw-Arrow $g 1160 290 1220 290 $line
        Draw-Arrow $g 1047 345 510 520 $line
        Draw-Arrow $g 1047 345 918 520 $line
        Draw-Arrow $g 1330 345 1330 520 $line
    }
