"""Main entry point for weather brief generation and delivery."""
import sys
from pathlib import Path

# Add current directory to path for imports
# sys.path.insert(0, str(Path(__file__).parent))

from src.day_classifier import get_day_type
from src.prompt_builder import build_weather_context, build_llm_prompt
from src.llm_client import generate_weather_brief, generate_subject_line
from src.email_sender import send_weather_brief_email

import os

print("DEBUG GROQ:", "SET" if os.getenv("GROQ_API_KEY") else "MISSING")

def main():
    """Generate and send daily weather brief."""
    
    # Determine day type and build context
    day_type = get_day_type()
    weather_header_html, weather_summaries, locations = build_weather_context(day_type)
    
    # Generate LLM prompt with location awareness
    prompt = build_llm_prompt(day_type, weather_summaries, locations)
    
    # Generate weather brief from LLM
    brief = generate_weather_brief(prompt)
    
    # Generate dynamic subject line based on weather
    subject = generate_subject_line(weather_summaries.get("midday", {}))
    
    # Send email
    success = send_weather_brief_email(subject, brief, weather_header_html)
    
    # Print confirmation
    if success:
        print(f"\n✅ Weather brief sent successfully!")
        print(f"📧 To: {__import__('os').getenv('RECIPIENT_EMAIL')}")
        print(f"📝 Subject: {subject}")
    else:
        print(f"\n⚠️ Failed to send weather brief email.")


if __name__ == "__main__":
    main()