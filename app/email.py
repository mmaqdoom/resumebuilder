import json
import smtplib
from email.message import EmailMessage
import urllib.error
import urllib.request

from flask import current_app


def _send_via_resend(api_key, from_email, to_email, subject, text_content, html_content):
    """Sends an email using Resend's REST API over HTTPS (TLS 1.3)."""
    url = "https://api.resend.com/emails"
    payload = {
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "text": text_content,
        "html": html_content,
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "ResumeBuilder-Flask/1.0",
    }

    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_body = response.read().decode("utf-8")
            current_app.logger.info("Email successfully sent via Resend API to %s: %s", to_email, res_body)
            return True
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        current_app.logger.error("Resend API HTTP error (%s): %s", exc.code, err_body)
        return False
    except urllib.error.URLError as exc:
        current_app.logger.error("Resend API connection error: %s", exc.reason)
        return False
    except Exception as exc:
        current_app.logger.error("Unexpected error sending email via Resend API: %s", exc)
        return False


def _send_via_smtp(mail_server, mail_port, mail_use_tls, mail_username, mail_password, from_email, to_email, subject, text_content, html_content):
    """Fallback email sender using standard SMTP."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(text_content)
    if html_content:
        msg.add_alternative(html_content, subtype="html")

    try:
        if mail_port == 465:
            with smtplib.SMTP_SSL(mail_server, mail_port, timeout=10) as server:
                if mail_username and mail_password:
                    server.login(mail_username, mail_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(mail_server, mail_port, timeout=10) as server:
                if mail_use_tls:
                    server.starttls()
                if mail_username and mail_password:
                    server.login(mail_username, mail_password)
                server.send_message(msg)
        current_app.logger.info("Email sent via SMTP to %s", to_email)
        return True
    except Exception as exc:
        current_app.logger.error("Failed to send email via SMTP to %s: %s", to_email, exc)
        return False


def send_password_reset_email(user, reset_url):
    """
    Sends a secure password reset link to the user.
    Priority 1: Resend REST API (HTTPS / TLS 1.3 token auth)
    Priority 2: Standard SMTP (if configured)
    Priority 3: Development logger & local fallback
    """
    resend_api_key = current_app.config.get("RESEND_API_KEY")
    resend_from_email = current_app.config.get(
        "RESEND_FROM_EMAIL", "ResumeBuilder <onboarding@resend.dev>"
    )

    mail_server = current_app.config.get("MAIL_SERVER")
    mail_port = current_app.config.get("MAIL_PORT", 587)
    mail_use_tls = current_app.config.get("MAIL_USE_TLS", True)
    mail_username = current_app.config.get("MAIL_USERNAME")
    mail_password = current_app.config.get("MAIL_PASSWORD")
    mail_sender = current_app.config.get(
        "MAIL_DEFAULT_SENDER", "ResumeBuilder <noreply@resumebuilder.com>"
    )

    subject = "Reset Your ResumeBuilder Password"

    text_content = f"""Hello,

To reset your password for your ResumeBuilder account, please click on the following link or copy it into your browser:

{reset_url}

This link is valid for 30 minutes. If you did not make this request, you can safely ignore this email and your password will remain unchanged.

Best regards,
The ResumeBuilder Team
"""

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #F8FAFC; color: #131B2E;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed; background-color: #F8FAFC; padding: 40px 16px;">
        <tr>
            <td align="center">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 540px; background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 12px rgba(19, 27, 46, 0.05);">
                    <!-- Brand Header -->
                    <tr>
                        <td style="padding: 32px 32px 24px 32px; border-bottom: 1px solid #F1F5F9;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td>
                                        <span style="font-size: 20px; font-weight: 700; color: #3525CD; letter-spacing: -0.5px;">ResumeBuilder</span>
                                        <span style="display: inline-block; margin-left: 8px; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 9999px; background-color: #EAEDFF; color: #3525CD; text-transform: uppercase;">Security</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Main Body -->
                    <tr>
                        <td style="padding: 32px;">
                            <h1 style="font-size: 22px; font-weight: 700; color: #131B2E; margin: 0 0 12px 0; letter-spacing: -0.3px;">Reset Your Password</h1>
                            <p style="font-size: 15px; line-height: 24px; color: #464555; margin: 0 0 24px 0;">
                                We received a request to reset the password for your ResumeBuilder account (<strong>{user.email}</strong>). Click the button below to choose a new password:
                            </p>
                            <!-- CTA Button -->
                            <table border="0" cellpadding="0" cellspacing="0" style="margin: 0 0 28px 0;">
                                <tr>
                                    <td align="center" style="border-radius: 10px; background-color: #4F46E5;">
                                        <a href="{reset_url}" target="_blank" style="font-size: 14px; font-weight: 600; color: #FFFFFF; text-decoration: none; padding: 12px 28px; display: inline-block; border-radius: 10px; background-color: #4F46E5;">
                                            Reset Password &rarr;
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            <p style="font-size: 13px; line-height: 20px; color: #777587; margin: 0 0 16px 0;">
                                ⏱ <strong>Security notice:</strong> This link will automatically expire in <strong>30 minutes</strong> and can only be used once.
                            </p>
                            <p style="font-size: 13px; line-height: 20px; color: #777587; margin: 0;">
                                If you did not request a password reset, you can safely ignore this email. Your account remains completely secure.
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 24px 32px; background-color: #F8FAFC; border-top: 1px solid #F1F5F9; font-size: 12px; color: #94A3B8; text-align: center; line-height: 18px;">
                            ResumeBuilder &bull; Tailored profile resumes for students and professionals
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    current_app.logger.info("Password reset link generated for %s: %s", user.email, reset_url)

    # 1. Try Resend REST API if key is present
    if resend_api_key:
        return _send_via_resend(
            resend_api_key,
            resend_from_email,
            user.email,
            subject,
            text_content,
            html_content,
        )

    # 2. Try SMTP if configured
    if mail_server:
        return _send_via_smtp(
            mail_server,
            mail_port,
            mail_use_tls,
            mail_username,
            mail_password,
            mail_sender,
            user.email,
            subject,
            text_content,
            html_content,
        )

    # 3. Neither configured (Local development / testing mode)
    return False
