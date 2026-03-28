"""Email sending utilities with HTML formatting."""
import os
import smtplib
import sys
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")


def create_email_html(subject: str, brief: str, weather_header: str) -> str:
    """
    Create a professional HTML email template.
    
    Args:
        subject: Email subject
        brief: Weather brief content
        weather_header: HTML header with date and temps
        
    Returns:
        Complete HTML string
    """
    timestamp = datetime.now().strftime("%H:%M")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 30px 20px;
                color: #333;
                line-height: 1.6;
            }}
            .content p {{
                margin: 15px 0;
                font-size: 15px;
            }}
            .period {{
                background-color: #f9f9f9;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .period strong {{
                display: block;
                color: #667eea;
                margin-bottom: 8px;
                font-size: 16px;
            }}
            .tip {{
                background-color: #e8f4f8;
                border: 1px solid #b3dfe8;
                padding: 15px;
                border-radius: 6px;
                margin: 20px 0;
                font-style: italic;
                color: #555;
            }}
            .footer {{
                background-color: #f5f5f5;
                padding: 15px 20px;
                text-align: center;
                font-size: 12px;
                color: #999;
                border-top: 1px solid #e0e0e0;
            }}
            strong {{
                color: #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>☀️ Weather Brief</h1>
            </div>
            <div class="content">
                {weather_header}
                <div style="margin-top: 20px; color: #555;">
                    {brief.replace(chr(10), '<br/>')}
                </div>
            </div>
            <div class="footer">
                Generated at {timestamp}
            </div>
        </div>
    </body>
    </html>
    """
    return html


def send_weather_brief_email(subject: str, brief: str, weather_header: str) -> bool:
    """
    Send the weather brief email via Gmail SMTP.
    
    Args:
        subject: Email subject line
        brief: Weather brief content
        weather_header: HTML header with metadata
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = GMAIL_USER
        message["To"] = RECIPIENT_EMAIL
        
        # Create HTML version
        html_content = create_email_html(subject, brief, weather_header)
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Send via Gmail SMTP
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, RECIPIENT_EMAIL, message.as_string())
        server.quit()
        
        return True
    
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False