"""email formatting and delivery."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_weather_email(subject: str, body: str, header_html: str, gif_url: str = None) -> bool:
    """send html email via gmail."""
    user = os.getenv("GMAIL_USER")
    pwd = os.getenv("GMAIL_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")
    
    # 1. Split body to handle signature and GIF placement
    lines = body.split('\n')
    
    processed_lines = []
    gif_inserted = False
    
    for line in lines:
        processed_lines.append(line)
        # Robust check: looks for TL;DR regardless of case or formatting (like **TL;DR:**)
        if "TL;DR" in line.upper() and gif_url and not gif_inserted:
            # Centered GIF with explicit styles for email clients
            gif_html = (
                f'<div style="text-align: center; margin: 20px 0;">'
                f'<img src="{gif_url}" alt="Weather Vibe" width="400" '
                f'style="max-width: 100%; height: auto; border-radius: 10px; border: 1px solid #eee; display: block; margin: 0 auto;">'
                f'</div>'
            )
            processed_lines.append(gif_html)
            gif_inserted = True

    # Identify signature (last two lines) for right-alignment
    main_text_lines = processed_lines[:-2]
    signature_lines = processed_lines[-2:]
    
    main_html = "<br/>".join(main_text_lines).replace("\n", "<br/>")
    sig_html = "<br/>".join(signature_lines).replace("\n", "<br/>")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: sans-serif; background: #f5f5f5; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {header_html}
            <div style="color: #444; line-height: 1.6; font-size: 15px;">
                {main_html}
                <br/><br/>
                <div style="text-align: right; color: #666; font-style: italic;">
                    {sig_html}
                </div>
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