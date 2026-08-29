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

New-Canvas (Join-Path $outDir "database_triple_db_topology.png") `
    "Smart Sportz Triple Database Topology" `
    "DB-1 editable primary, DB-2 immutable mirror backup, DB-3 event/login/software logs, Redis sessions/cache" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 90 230 230 105 "Application API" "Node.js services, Prisma, Socket.IO, jobs" $black $gray $line $soft
        Draw-Box $g 410 210 250 120 "DB-1 Primary" "Editable PostgreSQL: create, update, delete, soft delete" $black $gray $line $soft
        Draw-Box $g 760 210 250 120 "DB-2 Mirror" "Immutable backup: insert-only, no app edit/delete" $black $gray $line $soft
        Draw-Box $g 1110 210 250 120 "DB-3 Logs" "Software events, login logs, audit, security trails" $black $gray $line $soft
        Draw-Box $g 350 515 230 100 "Redis" "Sessions, cache, live score active state, queues" $black $gray $line $soft
        Draw-Box $g 685 515 230 100 "JSON Backups" "Encrypted table exports, manifests, checksums" $black $gray $line $soft
        Draw-Box $g 1020 515 230 100 "Secure Storage" "Object storage, WORM retention, restore archive" $black $gray $line $soft
        Draw-Arrow $g 320 282 410 270 $line
        Draw-Arrow $g 660 270 760 270 $line
        Draw-Arrow $g 320 300 350 545 $line
        Draw-Arrow $g 320 260 1110 260 $line
        Draw-Arrow $g 535 330 750 515 $line
        Draw-Arrow $g 885 330 800 515 $line
        Draw-Arrow $g 915 565 1020 565 $line
    }

New-Canvas (Join-Path $outDir "database_er_domain_diagram.png") `
    "Smart Sportz Core ER Domain Diagram" `
    "Primary relational model grouped by identity, tournaments, teams, players, matches, payments, CMS, and reports" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 120 190 220 95 "Organization" "Settings, branding, venues, users" $black $gray $line $soft
        Draw-Box $g 410 190 220 95 "Identity" "User, Role, Permission, Session" $black $gray $line $soft
        Draw-Box $g 700 190 220 95 "Tournament" "Categories, stages, rules, announcements" $black $gray $line $soft
        Draw-Box $g 990 190 220 95 "Sports & Venues" "Sport, rule, venue, court, equipment" $black $gray $line $soft
        Draw-Box $g 265 450 220 95 "Registration" "Team/player entry, documents, waitlist" $black $gray $line $soft
        Draw-Box $g 555 450 220 95 "Teams & Players" "Roster, coaches, statistics, profile" $black $gray $line $soft
        Draw-Box $g 845 450 220 95 "Matches & Scores" "Fixture, match, event, live score, result" $black $gray $line $soft
        Draw-Box $g 1135 450 220 95 "Finance & CMS" "Payment, refund, invoice, page, gallery" $black $gray $line $soft
        Draw-Arrow $g 340 238 410 238 $line
        Draw-Arrow $g 630 238 700 238 $line
        Draw-Arrow $g 920 238 990 238 $line
        Draw-Arrow $g 810 285 375 450 $line
        Draw-Arrow $g 810 285 665 450 $line
        Draw-Arrow $g 810 285 955 450 $line
        Draw-Arrow $g 810 285 1245 450 $line
    }

New-Canvas (Join-Path $outDir "database_table_relationships.png") `
    "High-Level Table Relationship Map" `
    "Foreign keys and junction tables connect users, tournaments, registration, teams, players, matches, and payments" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 75 210 210 95 "User" "id, profile, auth, status" $black $gray $line $soft
        Draw-Box $g 350 210 210 95 "UserRole" "userId, roleId, scope" $black $gray $line $soft
        Draw-Box $g 625 210 210 95 "RolePermission" "roleId, permissionId" $black $gray $line $soft
        Draw-Box $g 900 210 210 95 "Tournament" "sport, venue, status, dates" $black $gray $line $soft
        Draw-Box $g 1175 210 210 95 "Payment" "order, transaction, status" $black $gray $line $soft
        Draw-Box $g 230 500 210 95 "Registration" "mode, status, category" $black $gray $line $soft
        Draw-Box $g 505 500 210 95 "Team / Player" "roster, documents, stats" $black $gray $line $soft
        Draw-Box $g 780 500 210 95 "Match" "fixture, teams, status" $black $gray $line $soft
        Draw-Box $g 1055 500 210 95 "MatchEvent" "type, value, metadata" $black $gray $line $soft
        Draw-Arrow $g 285 257 350 257 $line
        Draw-Arrow $g 560 257 625 257 $line
        Draw-Arrow $g 835 257 900 257 $line
        Draw-Arrow $g 1110 257 1175 257 $line
        Draw-Arrow $g 1005 305 335 500 $line
        Draw-Arrow $g 440 548 505 548 $line
        Draw-Arrow $g 715 548 780 548 $line
        Draw-Arrow $g 990 548 1055 548 $line
    }

New-Canvas (Join-Path $outDir "database_write_mirror_json_flow.png") `
    "Write, Mirror, and JSON Backup Data Flow" `
    "DB-1 accepts mutations, DB-2 mirrors immutable changes, and encrypted JSON exports preserve table-level backups" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 75 235 210 100 "App Write" "Create, update, soft delete, transaction" $black $gray $line $soft
        Draw-Box $g 350 235 210 100 "DB-1 Commit" "Primary mutable record with audit fields" $black $gray $line $soft
        Draw-Box $g 625 235 210 100 "Change Capture" "WAL/logical stream, outbox, checksum" $black $gray $line $soft
        Draw-Box $g 900 235 210 100 "DB-2 Insert" "Immutable mirror version, no edit/delete" $black $gray $line $soft
        Draw-Box $g 1175 235 210 100 "Backup Verify" "Row count, checksum, lag, restore test" $black $gray $line $soft
        Draw-Box $g 350 520 230 95 "DB-1 JSON" "Encrypted table JSON or NDJSON export" $black $gray $line $soft
        Draw-Box $g 760 520 230 95 "DB-2 JSON" "Encrypted mirror export with manifest" $black $gray $line $soft
        Draw-Arrow $g 285 285 350 285 $line
        Draw-Arrow $g 560 285 625 285 $line
        Draw-Arrow $g 835 285 900 285 $line
        Draw-Arrow $g 1110 285 1175 285 $line
        Draw-Arrow $g 455 335 465 520 $line
        Draw-Arrow $g 1005 335 875 520 $line
    }

New-Canvas (Join-Path $outDir "database_security_encryption_model.png") `
    "Database Security and Encryption Model" `
    "Passwords are hashed, sensitive fields are encrypted, JSON exports are encrypted and signed, and keys are rotated" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 85 230 220 100 "Passwords" "Argon2id/bcrypt hash, salt, optional pepper" $black $gray $line $soft
        Draw-Box $g 370 230 220 100 "Sensitive Fields" "PII, tokens, documents, payment metadata" $black $gray $line $soft
        Draw-Box $g 655 230 220 100 "Encryption" "AES-256-GCM, KMS keys, field-level policy" $black $gray $line $soft
        Draw-Box $g 940 230 220 100 "JSON Backups" "Encrypt, compress, sign, checksum, manifest" $black $gray $line $soft
        Draw-Box $g 1225 230 220 100 "Storage" "WORM, lifecycle, access logs, restore policy" $black $gray $line $soft
        Draw-Box $g 430 520 230 95 "Access Control" "DB roles, least privilege, separate credentials" $black $gray $line $soft
        Draw-Box $g 835 520 230 95 "Key Rotation" "Versioned keys, re-encrypt plan, audit trail" $black $gray $line $soft
        Draw-Arrow $g 305 280 370 280 $line
        Draw-Arrow $g 590 280 655 280 $line
        Draw-Arrow $g 875 280 940 280 $line
        Draw-Arrow $g 1160 280 1225 280 $line
        Draw-Arrow $g 765 330 545 520 $line
        Draw-Arrow $g 1050 330 950 520 $line
    }

New-Canvas (Join-Path $outDir "database_redis_session_cache_flow.png") `
    "Redis Session, Cache, Queue, and Live State Flow" `
    "Redis supports sessions, cache, live match state, rate limits, and background queues without becoming source of truth" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 225 220 100 "API Request" "Auth, route, cache key, rate check" $black $gray $line $soft
        Draw-Box $g 380 170 220 100 "Session Cache" "Session/token state, revocation, TTL" $black $gray $line $soft
        Draw-Box $g 380 390 220 100 "Query Cache" "Public lists, dashboard counts, lookup data" $black $gray $line $soft
        Draw-Box $g 720 170 220 100 "Live State" "Current score, timer, active match snapshot" $black $gray $line $soft
        Draw-Box $g 720 390 220 100 "Queues" "Notifications, exports, reports, cleanup" $black $gray $line $soft
        Draw-Box $g 1080 280 260 100 "DB-1 Source" "Persistent source of truth and recovery base" $black $gray $line $soft
        Draw-Arrow $g 315 260 380 220 $line
        Draw-Arrow $g 315 305 380 440 $line
        Draw-Arrow $g 600 220 720 220 $line
        Draw-Arrow $g 600 440 720 440 $line
        Draw-Arrow $g 940 220 1080 310 $line
        Draw-Arrow $g 940 440 1080 350 $line
    }
