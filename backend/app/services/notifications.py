from __future__ import annotations

import base64
import json
import random
import smtplib
import urllib.parse
import urllib.request
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Any

from app.core.config import settings

try:
    import resend
except Exception:  # pragma: no cover - local env may install requirements later
    resend = None


@dataclass
class DeliveryResult:
    ok: bool
    provider: str
    message: str


def generate_otp(length: int = 4) -> str:
    start = 10 ** (length - 1)
    end = (10 ** length) - 1
    return str(random.randint(start, end))


def _twilio_auth_header() -> str | None:
    if settings.twilio_account_sid and settings.twilio_auth_token:
        username = settings.twilio_account_sid
        password = settings.twilio_auth_token
    else:
        username = settings.twilio_api_key_sid
        password = settings.twilio_api_key_secret
    if not username or not password:
        return None
    token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def send_sms_otp(phone: str, code: str | None = None) -> DeliveryResult:
    return DeliveryResult(False, "whatsapp", "SMS is disabled. WhatsApp verification is configured but inactive.")


def check_sms_otp(phone: str, code: str) -> DeliveryResult:
    return DeliveryResult(False, "whatsapp", "SMS verification checks are disabled.")


def send_sms_message(phone: str, message: str) -> DeliveryResult:
    return DeliveryResult(False, "whatsapp", "SMS sending is disabled. Use WhatsApp delivery when an API is configured.")


def send_whatsapp_message(phone: str, message: str) -> DeliveryResult:
    if not settings.whatsapp_delivery_enabled:
        return DeliveryResult(False, "whatsapp", "WhatsApp delivery is configured but inactive.")
    if settings.whatsapp_provider != "twilio":
        return DeliveryResult(False, "whatsapp", "No active WhatsApp API provider is configured.")
    auth = _twilio_auth_header()
    if not auth:
        return DeliveryResult(False, "twilio", "Twilio credentials are not configured")
    if not settings.twilio_from_number and not settings.twilio_messaging_service_sid:
        return DeliveryResult(False, "twilio", "WhatsApp requires TWILIO_FROM_NUMBER or TWILIO_MESSAGING_SERVICE_SID")
    to_number = settings.whatsapp_default_to or phone
    payload = {"To": f"whatsapp:{to_number}", "Body": message}
    if settings.twilio_messaging_service_sid:
        payload["MessagingServiceSid"] = settings.twilio_messaging_service_sid
    else:
        payload["From"] = settings.twilio_from_number if settings.twilio_from_number.startswith("whatsapp:") else f"whatsapp:{settings.twilio_from_number}"
    form = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json",
        data=form,
        method="POST",
        headers={"Authorization": auth, "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return DeliveryResult(True, "twilio", f"WhatsApp queued {payload.get('sid', '')}".strip())
    except Exception as exc:
        return DeliveryResult(False, "twilio", str(exc))


def send_email(
    to_email: str,
    subject: str,
    html: str,
    text: str | None = None,
    attachments: list[dict[str, Any]] | None = None,
) -> DeliveryResult:
    if not settings.smtp_host or not settings.smtp_username or not settings.smtp_password:
        if settings.notification_delivery_mode == "whatsapp":
            return DeliveryResult(False, "smtp", "SMTP credentials are not configured")
        if settings.email_provider == "brevo":
            return send_brevo_email(to_email, subject, html, text, attachments=attachments)
        if not settings.resend_api_key:
            return DeliveryResult(False, "resend", "RESEND_API_KEY is not configured")
        delivery_to = settings.resend_test_to_email if settings.resend_force_test_recipient else to_email
        redirect_note = f" redirected to test inbox {delivery_to}" if delivery_to != to_email else ""
        if resend is not None:
            resend.api_key = settings.resend_api_key
            params: resend.Emails.SendParams = {
                "from": settings.resend_from_email,
                "to": [delivery_to],
                "subject": subject,
                "html": html,
            }
            if text:
                params["text"] = text
            if attachments:
                params["attachments"] = [
                    {
                        "filename": att.get("filename") or att.get("name") or "attachment.pdf",
                        "content": base64.b64encode(att["content"]).decode("utf-8") if isinstance(att["content"], bytes) else str(att["content"]),
                    }
                    for att in attachments
                ]
            try:
                email = resend.Emails.send(params)
                message = f"Email queued{redirect_note}"
                if isinstance(email, dict) and email.get("id"):
                    message = f"{message} {email['id']}"
                return DeliveryResult(True, "resend", message.strip())
            except Exception as exc:
                return DeliveryResult(False, "resend", str(exc))
        body: dict[str, Any] = {
            "from": settings.resend_from_email,
            "to": [delivery_to],
            "subject": subject,
            "html": html,
        }
        if text:
            body["text"] = text
        if attachments:
            body["attachments"] = [
                {
                    "filename": att.get("filename") or att.get("name") or "attachment.pdf",
                    "content": base64.b64encode(att["content"]).decode("utf-8") if isinstance(att["content"], bytes) else str(att["content"]),
                }
                for att in attachments
            ]
        request = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps(body).encode("utf-8"),
            method="POST",
            headers={"Authorization": f"Bearer {settings.resend_api_key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=12) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return DeliveryResult(True, "resend", f"Email queued {payload.get('id', '')}".strip())
        except Exception as exc:
            return DeliveryResult(False, "resend", str(exc))

    delivery_to = to_email
    sender_email = settings.smtp_sender_email or settings.smtp_username or "info@liyansvastra.com"
    domain = sender_email.split("@")[1] if "@" in sender_email else "smartsportz.in"

    from email.utils import formatdate, make_msgid

    message = EmailMessage()
    message["From"] = f"{settings.smtp_sender_name} <{sender_email}>"
    message["To"] = delivery_to
    message["Reply-To"] = f"{settings.smtp_sender_name} <{sender_email}>"
    message["Subject"] = subject
    message["Date"] = formatdate(localtime=True)
    message["Message-ID"] = make_msgid(domain=domain)
    message["X-Mailer"] = "SmartSportz Platform v1.0"
    message["List-Unsubscribe"] = f"<mailto:{sender_email}?subject=unsubscribe>"
    message.set_content(text or "Please view this message in an HTML-capable mail client.")
    message.add_alternative(html, subtype="html")

    if attachments:
        for att in attachments:
            content = att.get("content")
            if isinstance(content, str):
                try:
                    content_bytes = base64.b64decode(content)
                except Exception:
                    content_bytes = content.encode("utf-8")
            else:
                content_bytes = bytes(content or b"")
            filename = att.get("filename") or att.get("name") or "document.pdf"
            content_type = att.get("content_type", "application/pdf")
            maintype, subtype = content_type.split("/", 1) if "/" in content_type else ("application", "pdf")
            message.add_attachment(content_bytes, maintype=maintype, subtype=subtype, filename=filename)
    try:
        if settings.smtp_use_ssl:
            with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port, timeout=15) as client:
                client.login(settings.smtp_username, settings.smtp_password)
                client.send_message(message)
        else:
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as client:
                if settings.smtp_use_tls:
                    client.starttls()
                client.login(settings.smtp_username, settings.smtp_password)
                client.send_message(message)
        return DeliveryResult(True, "smtp", f"Email sent to {delivery_to}")
    except Exception as exc:
        return DeliveryResult(False, "smtp", str(exc))


def send_brevo_email(
    to_email: str,
    subject: str,
    html: str,
    text: str | None = None,
    attachments: list[dict[str, Any]] | None = None,
) -> DeliveryResult:
    if not settings.brevo_api_key:
        return DeliveryResult(False, "brevo", "BREVO_API_KEY is not configured")
    delivery_to = settings.brevo_test_to_email if settings.brevo_force_test_recipient else to_email
    redirect_note = f" redirected to test inbox {delivery_to}" if delivery_to != to_email else ""
    payload: dict[str, Any] = {
        "sender": {"name": settings.brevo_sender_name, "email": settings.brevo_sender_email},
        "to": [{"email": delivery_to}],
        "subject": subject,
        "htmlContent": html,
    }
    if text:
        payload["textContent"] = text
    if attachments:
        payload["attachment"] = []
        for att in attachments:
            content = att.get("content")
            if isinstance(content, bytes):
                b64_content = base64.b64encode(content).decode("utf-8")
            else:
                b64_content = str(content)
            filename = att.get("filename") or att.get("name") or "document.pdf"
            payload["attachment"].append({"name": filename, "content": b64_content})
    request = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email",
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "api-key": settings.brevo_api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read().decode("utf-8") or "{}"
            response_payload = json.loads(body)
        message_id = response_payload.get("messageId", "")
        return DeliveryResult(True, "brevo", f"Email queued{redirect_note} {message_id}".strip())
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        return DeliveryResult(False, "brevo", f"HTTP {exc.code}: {error_body}")
    except Exception as exc:
        return DeliveryResult(False, "brevo", str(exc))


def send_resend_sdk_test_email() -> dict[str, Any]:
    if resend is None:
        return {"ok": False, "provider": "resend", "message": "resend package is not installed"}
    if not settings.resend_api_key:
        return {"ok": False, "provider": "resend", "message": "RESEND_API_KEY is not configured"}
    resend.api_key = settings.resend_api_key
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["delivered@resend.dev"],
        "subject": "hello world",
        "html": "<p>it works!</p>",
    }
    try:
        email = resend.Emails.send(params)
        return {"ok": True, "provider": "resend", "response": email}
    except Exception as exc:
        return {"ok": False, "provider": "resend", "message": str(exc)}


def send_email_otp(to_email: str, code: str) -> DeliveryResult:
    if settings.otp_delivery_mode == "local":
        print(f"[OTP LOCAL] Verification code for {to_email}: {code}", flush=True)
        return DeliveryResult(True, "local", f"Local development code: {code}")
    html = f"""
    <div style="font-family:Arial,sans-serif;line-height:1.5;color:#0b1b33">
      <h2>Verify your Smart Sportz account</h2>
      <p>Your verification code is:</p>
      <p style="font-size:28px;font-weight:800;color:#007a4d;letter-spacing:4px">{code}</p>
      <p>This code expires soon. Do not share it with anyone.</p>
    </div>
    """
    delivery = send_email(to_email, "Smart Sportz verification code", html, f"Your Smart Sportz verification code is {code}.")
    if not delivery.ok and (settings.app_env in {"development", "docker"} or settings.otp_delivery_mode == "local"):
        print(f"[OTP LOCAL FALLBACK] Code for {to_email}: {code} (Email delivery failed: {delivery.message})", flush=True)
        return DeliveryResult(True, "local", f"Local development code: {code}")
    return delivery


def registration_completion_message(details: dict[str, Any]) -> str:
    payment_line = details.get("paymentDetails") or details.get("receiptNumber") or "Payment received"
    return (
        "Smart Sportz registration complete.\n"
        f"Tournament: {details.get('tournamentName')}\n"
        f"Team: {details.get('teamName')} ({details.get('teamCode')})\n"
        f"Unique ID: {details.get('confirmationCode')}\n"
        f"Payment: {payment_line}\n"
        f"QR: {details.get('qrPayload')}"
    )


def match_selection_message(details: dict[str, Any]) -> str:
    return (
        "Smart Sportz team selected for match.\n"
        f"Tournament: {details.get('tournamentName')}\n"
        f"Round: {details.get('round') or 'TBA'}\n"
        f"Teams: {details.get('teams') or 'TBA'}\n"
        f"Date: {details.get('startsAt') or 'TBA'}\n"
        f"Bracket details: {details.get('bracketDetails') or 'Published bracket'}"
    )


def match_reminder_message(details: dict[str, Any]) -> str:
    return (
        "Smart Sportz match reminder.\n"
        f"Tournament: {details.get('tournamentName')}\n"
        f"Round: {details.get('round') or 'TBA'}\n"
        f"Teams: {details.get('teams') or 'TBA'}\n"
        f"Match time: {details.get('startsAt') or 'TBA'} to {details.get('endsAt') or 'TBA'}\n"
        "Reminder: your match is scheduled in 2 days."
    )


def send_registration_payment_success(
    to_email: str,
    phone: str,
    details: dict[str, Any],
    pdf_bytes: bytes | None = None,
) -> list[DeliveryResult]:
    results: list[DeliveryResult] = []

    # 1. Send Email with PDF pass attachment
    if to_email:
        team_name = details.get("teamName", "Your Team")
        tournament_name = details.get("tournamentName", "Tournament")
        team_code = details.get("teamCode", "PASS")
        receipt_number = details.get("receiptNumber", "-")
        confirmation_code = details.get("confirmationCode", "-")
        captain_name = details.get("captainName", "-")

        subject = f"Registration Confirmed: {tournament_name} - {team_name}"
        html = f"""
        <div style="font-family: Arial, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #0b1c30; max-width: 620px; margin: 0 auto; padding: 28px; border: 1px solid #e2e8f0; border-radius: 16px; background: #ffffff;">
          <div style="text-align: center; margin-bottom: 24px; border-bottom: 2px solid #08723f; padding-bottom: 16px;">
            <h1 style="color: #08723f; margin: 0; font-size: 26px; font-weight: 900; letter-spacing: -0.5px;">SMART SPORTZ</h1>
            <p style="color: #64748b; font-size: 14px; margin: 4px 0 0; font-weight: 600;">Official Tournament Registration & Verification Pass</p>
          </div>
          
          <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 16px 20px; margin-bottom: 22px;">
            <h3 style="color: #166534; margin: 0 0 6px; font-size: 17px; font-weight: 800;">&#10004; Payment Verified & Registration Confirmed</h3>
            <p style="color: #15803d; margin: 0; font-size: 14px; line-height: 1.5;">
              Congratulations! Your team registration for <strong>{tournament_name}</strong> has been verified by the tournament management team.
            </p>
          </div>

          <table style="width: 100%; border-collapse: collapse; margin-bottom: 22px; font-size: 14px;">
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Tournament:</td>
              <td style="padding: 10px 0; color: #0f172a; font-weight: 700; text-align: right;">{tournament_name}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Team Name:</td>
              <td style="padding: 10px 0; color: #0f172a; font-weight: 700; text-align: right;">{team_name}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Captain:</td>
              <td style="padding: 10px 0; color: #0f172a; font-weight: 700; text-align: right;">{captain_name}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Team Code:</td>
              <td style="padding: 10px 0; color: #08723f; font-weight: 800; font-family: monospace; font-size: 15px; text-align: right;">{team_code}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Confirmation Code:</td>
              <td style="padding: 10px 0; color: #08723f; font-weight: 800; font-family: monospace; font-size: 15px; text-align: right;">{confirmation_code}</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Receipt Number:</td>
              <td style="padding: 10px 0; color: #0f172a; font-weight: 700; text-align: right;">{receipt_number}</td>
            </tr>
            <tr>
              <td style="padding: 10px 0; color: #64748b; font-weight: 600;">Payment Status:</td>
              <td style="padding: 10px 0; color: #16a34a; font-weight: 900; text-align: right;">&#10004; PAID &amp; VERIFIED</td>
            </tr>
          </table>

          <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px; padding: 16px; margin-bottom: 24px; text-align: center;">
            <p style="margin: 0; color: #1e293b; font-size: 14px; font-weight: 700;">
              &#128206; Official Registration Pass PDF Attached
            </p>
            <p style="margin: 6px 0 0; color: #64748b; font-size: 13px; line-height: 1.4;">
              Your official registration pass with verified QR code is attached to this email. Please download and keep a copy for venue check-in on match days.
            </p>
          </div>

          <div style="font-size: 12px; color: #94a3b8; text-align: center; border-top: 1px solid #f1f5f9; padding-top: 16px;">
            <p style="margin: 0;">Smart Sportz Enterprise SaaS &bull; Tournament Management Platform</p>
          </div>
        </div>
        """
        text = (
            f"Smart Sportz Registration Confirmed!\n\n"
            f"Tournament: {tournament_name}\n"
            f"Team: {team_name} ({team_code})\n"
            f"Captain: {captain_name}\n"
            f"Confirmation Code: {confirmation_code}\n"
            f"Receipt: {receipt_number}\n"
            f"Payment Status: PAID & VERIFIED\n\n"
            f"Your official registration pass PDF is attached to this email. Please carry it to the venue."
        )

        attachments = None
        if pdf_bytes:
            filename = f"smart-sportz-pass-{team_code}.pdf"
            attachments = [{"filename": filename, "content": pdf_bytes, "content_type": "application/pdf"}]

        email_result = send_email(to_email, subject, html, text=text, attachments=attachments)
        results.append(email_result)

    # 2. WhatsApp Notification
    whatsapp_message = registration_completion_message(details)
    wa_result = send_whatsapp_message(phone or settings.twilio_default_to, whatsapp_message)
    if not wa_result.ok:
        wa_result.message = f"{wa_result.message}; WhatsApp text fallback: {whatsapp_message}"
    results.append(wa_result)

    return results


def send_match_selection_whatsapp(phone: str, details: dict[str, Any]) -> DeliveryResult:
    message = match_selection_message(details)
    result = send_whatsapp_message(phone or settings.whatsapp_default_to, message)
    if not result.ok:
        result.message = f"{result.message}; WhatsApp text fallback: {message}"
    return result


def send_match_reminder_whatsapp(phone: str, details: dict[str, Any]) -> DeliveryResult:
    message = match_reminder_message(details)
    result = send_whatsapp_message(phone or settings.whatsapp_default_to, message)
    if not result.ok:
        result.message = f"{result.message}; WhatsApp text fallback: {message}"
    return result
