import smtplib
from email.message import EmailMessage

from flask import current_app


def send_password_reset_email(user, reset_url):
    """Sends a password reset link to the user via SMTP if configured, or logs it."""
    mail_server = current_app.config.get("MAIL_SERVER")
    mail_port = current_app.config.get("MAIL_PORT", 587)
    mail_username = current_app.config.get("MAIL_USERNAME")
    mail_password = current_app.config.get("MAIL_PASSWORD")
    mail_sender = current_app.config.get("MAIL_DEFAULT_SENDER", "noreply@resumebuilder.com")
    mail_use_tls = current_app.config.get("MAIL_USE_TLS", True)

    current_app.logger.info("Password reset link for %s: %s", user.email, reset_url)

    if not mail_server:
        # SMTP not configured; logged above for dev/testing
        return False

    msg = EmailMessage()
    msg["Subject"] = "Reset Your ResumeBuilder Password"
    msg["From"] = mail_sender
    msg["To"] = user.email
    msg.set_content(
        f"""Hello,

To reset your password for your ResumeBuilder account, please visit the following link:

{reset_url}

This link is valid for 30 minutes. If you did not make this request, you can safely ignore this email and your password will remain unchanged.

Best regards,
The ResumeBuilder Team
"""
    )

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
        return True
    except Exception as exc:
        current_app.logger.error("Failed to send password reset email to %s: %s", user.email, exc)
        return False

