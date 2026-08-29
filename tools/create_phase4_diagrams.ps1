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

New-Canvas (Join-Path $outDir "phase4_registration_lifecycle.png") `
    "Registration Lifecycle" `
    "From tournament configuration to participant confirmation" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 80 225 220 120 "Configure" "Rules, capacity, category, documents, fees" $soft $line
        Draw-Box $g 350 225 220 120 "Register" "Individual, team, or hybrid form" $soft $line
        Draw-Box $g 620 225 220 120 "Documents" "Upload, preview, replace, validation" $soft $line
        Draw-Box $g 890 225 220 120 "Review" "Confirm details, coupon, final amount" $soft $line
        Draw-Box $g 1160 225 220 120 "Submit" "Payment or approval workflow begins" $soft $line
        Draw-Arrow $g 300 285 350 285 $line
        Draw-Arrow $g 570 285 620 285 $line
        Draw-Arrow $g 840 285 890 285 $line
        Draw-Arrow $g 1110 285 1160 285 $line
        Draw-Box $g 365 520 260 120 "Capacity Rules" "Approved, pending, waitlist, late registration" $soft $line
        Draw-Box $g 760 520 300 120 "Confirmation" "Email, SMS, WhatsApp, receipt, invoice" $soft $line
        Draw-Arrow $g 1270 345 495 520 $line
        Draw-Arrow $g 625 580 760 580 $line
    }

New-Canvas (Join-Path $outDir "phase4_payment_webhook_flow.png") `
    "Razorpay Payment and Webhook Flow" `
    "Secure payment state changes with backend verification" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 95 220 230 120 "Registration" "Create draft registration and amount" $soft $line
        Draw-Box $g 385 220 230 120 "Backend" "Create Razorpay order, store pending payment" $soft $line
        Draw-Box $g 675 220 230 120 "Razorpay" "UPI, card, net banking, wallet" $soft $line
        Draw-Box $g 965 220 230 120 "Webhook" "Signature verification and event validation" $soft $line
        Draw-Box $g 1255 220 230 120 "Database" "Paid, failed, expired, refunded status" $soft $line
        Draw-Arrow $g 325 280 385 280 $line
        Draw-Arrow $g 615 280 675 280 $line
        Draw-Arrow $g 905 280 965 280 $line
        Draw-Arrow $g 1195 280 1255 280 $line
        Draw-Box $g 410 520 300 120 "Audit Trail" "Payment initiated, verified, failed, refunded" $soft $line
        Draw-Box $g 820 520 320 120 "Receipts" "Invoice, payment receipt, QR code, PDF download" $soft $line
        Draw-Arrow $g 1370 340 560 520 $line
        Draw-Arrow $g 1370 340 980 520 $line
    }

New-Canvas (Join-Path $outDir "phase4_approval_waitlist_refund.png") `
    "Approval, Waitlist, and Refund Workflow" `
    "Admin decisions after registration submission" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 650 180 300 100 "Submitted" "Registration received after form/payment step" $soft $line
        Draw-Box $g 160 370 260 125 "Approve" "Participant confirmed and notified" $soft $line
        Draw-Box $g 500 370 260 125 "Reject" "Reason captured, notification sent" $soft $line
        Draw-Box $g 840 370 260 125 "Request Docs" "Additional files required before approval" $soft $line
        Draw-Box $g 1180 370 260 125 "Waitlist" "Position shown, auto-promote when slot opens" $soft $line
        Draw-Box $g 500 610 260 100 "Refund" "Full, partial, manual, future automated" $soft $line
        Draw-Box $g 840 610 260 100 "Notifications" "Email, SMS, WhatsApp templates" $soft $line
        Draw-Arrow $g 650 245 290 370 $line
        Draw-Arrow $g 730 280 630 370 $line
        Draw-Arrow $g 870 280 970 370 $line
        Draw-Arrow $g 950 245 1310 370 $line
        Draw-Arrow $g 630 495 630 610 $line
        Draw-Arrow $g 970 495 970 610 $line
        Draw-Arrow $g 1310 495 970 610 $line
    }

New-Canvas (Join-Path $outDir "phase4_registration_data_model.png") `
    "Registration and Payment Data Model" `
    "Core records needed for reliable participant and payment management" `
    {
        param($g, $black, $gray, $line, $soft)
        Draw-Box $g 120 205 250 110 "Tournament" "Rules, capacity, categories, fee settings" $soft $line
        Draw-Box $g 480 205 250 110 "Registration" "Type, status, approval, waitlist position" $soft $line
        Draw-Box $g 840 205 250 110 "Participant" "Team, player, individual profile" $soft $line
        Draw-Box $g 1200 205 250 110 "Documents" "Logo, ID proof, certificates, consent" $soft $line
        Draw-Box $g 480 480 250 120 "Payment" "Order, transaction, status, amount, taxes" $soft $line
        Draw-Box $g 840 480 250 120 "Invoice" "Receipt, QR code, PDF, organizer info" $soft $line
        Draw-Box $g 1200 480 250 120 "Audit Log" "User, timestamp, IP, previous/new values" $soft $line
        Draw-Arrow $g 370 260 480 260 $line
        Draw-Arrow $g 730 260 840 260 $line
        Draw-Arrow $g 1090 260 1200 260 $line
        Draw-Arrow $g 605 315 605 480 $line
        Draw-Arrow $g 730 540 840 540 $line
        Draw-Arrow $g 1090 540 1200 540 $line
    }
