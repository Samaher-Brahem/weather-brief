"""email formatting and delivery."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_weather_email(subject: str, body: str, header_html: str) -> bool:
    """send html email via gmail."""
    user = os.getenv("GMAIL_USER")
    pwd = os.getenv("GMAIL_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")
    
    # format body text to html breaks
    body_html = body.replace("\n", "<br/>")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: sans-serif; background: #f5f5f5; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {header_html}
            <div style="color: #444; line-height: 1.6; font-size: 15px;">
                {body_html}
            </div>
            <div style="margin-top: 30px; font-size: 12px; color: #999; text-align: center;">
                Generated at {datetime.now().strftime("%H:%M")}
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = user
        msg["To"] = recipient
        msg.attach(MIMEText(html, "html"))
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(user, pwd)
            server.sendmail(user, recipient, msg.as_string())
        return True
    except Exception as e:
        print(f"❌ email failed: {e}")
        return False