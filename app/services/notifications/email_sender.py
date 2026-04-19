import smtplib
from email.mime.text import MIMEText

from app.config.settings import settings


def send_results_email(body: str) -> None:
    """
    Sends final ranked posts via Gmail SMTP using TLS and app-password auth.
    """
    if not settings.EMAIL_USER or not settings.EMAIL_PASS or not settings.EMAIL_RECEIVER:
        raise ValueError("Email settings are incomplete. Check EMAIL_USER, EMAIL_PASS, and EMAIL_RECEIVER.")

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = "Top 3 Reddit Finance Insights"
    message["From"] = settings.EMAIL_USER
    message["To"] = settings.EMAIL_RECEIVER

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
        server.sendmail(settings.EMAIL_USER, [settings.EMAIL_RECEIVER], message.as_string())