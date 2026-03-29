"""entry point for weather brief."""
import sys
from dotenv import load_dotenv
from src.day_classifier import get_day_type
from src.prompt_builder import build_weather_context, build_llm_prompt
from src.llm_client import generate_weather_brief
from src.email_sender import send_weather_email

def main():
    load_dotenv()
    print("🚀 starting weather brief generation...")
    
    try:
        day_type = get_day_type()
        print(f"📅 detected day: {day_type}")
        
        # 1. get weather data & header
        header, summaries = build_weather_context(day_type)
        
        # 2. build prompt and get json response from llm
        prompt = build_llm_prompt(day_type, summaries)
        subject, body = generate_weather_brief(prompt)
        print(f"✉️  subject generated: {subject}")
        
        # 3. send email
        if send_weather_email(subject, body, header):
            print("✅ success!")
            return 0
            
        return 1
    except Exception as e:
        print(f"❌ fatal error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())