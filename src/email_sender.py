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
    
    # 1. Split body into lines to find the insertion point
    lines = body.split('\n')
    processed_lines = []
    gif_inserted = False
    
    for line in lines:
        processed_lines.append(line)
        
        # Robust check for TL;DR (handles **TL;DR:**, tl;dr, etc.)
        if "TL;DR" in line.upper() and gif_url and not gif_inserted:
            # Constrained GIF container
            gif_html = (
                f'<div style="text-align: center; margin: 15px 0;">'
                f'<img src="{gif_url}" alt="Weather Vibe" width="300" '
                f'style="width: 200px; max-width: 100%; height: auto; border-radius: 8px; '
                f'border: 1px solid #eee; display: inline-block;">'
                f'</div>'
            )
            processed_lines.append(gif_html)
            gif_inserted = True

    # Identify the main body vs the last two lines (sign-off and signature)
    # This ensures the 'With love, WhetherAI' stays right-aligned
    main_text_lines = processed_lines[:-2]
    signature_lines = processed_lines[-2:]
    
    # Join with breaks, ensuring LLM double-newlines (\n\n) translate to HTML
    main_html = "<br/>".join(main_text_lines).replace("\n", "<br/>")
    sig_html = "<br/>".join(signature_lines).replace("\n", "<br/>")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: sans-serif; background: #f5f5f5; padding: 20px; margin: 0;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {header_html}
            <div style="color: #444; line-height: 1.6; font-size: 15px;">
                {main_html}
                <br/><br/>
                <div style="text-align: right; color: #666; font-style: italic; border-top: 1px solid #fafafa; padding-top: 10px;">
                    {sig_html}
                </div>
            </div>
            <div style="margin-top: 30px; font-size: 11px; color: #bbb; text-align: center;">
                Generated at {datetime.now().strftime("%H:%M")} • WhetherAI v3.0
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