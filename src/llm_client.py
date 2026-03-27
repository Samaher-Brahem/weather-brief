import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Groq client will automatically use GROQ_API_KEY from .env
client = Groq()


def generate_weather_brief(prompt: str) -> tuple:
    """
    Sends the weather prompt to Groq and gets back both subject line and brief.
    Uses streaming and returns both as a tuple (subject, brief).
    """
    
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_completion_tokens=512,
        top_p=0.95,
        stream=True,
        stop=None
    )
    
    # Collect all chunks into a single string
    full_response = ""
    for chunk in completion:
        content = chunk.choices[0].delta.content
        if content:
            full_response += content
            print(content, end="", flush=True)  # Print in real-time
    
    print()  # New line after streaming completes
    
    # Parse the response to extract subject and brief
    subject = ""
    brief = ""
    
    # Try to find SUBJECT: and BRIEF: tags
    if "SUBJECT:" in full_response and "BRIEF:" in full_response:
        subject_start = full_response.find("SUBJECT:") + len("SUBJECT:")
        brief_start = full_response.find("BRIEF:") + len("BRIEF:")
        
        subject = full_response[subject_start:full_response.find("BRIEF:")].strip()
        brief = full_response[brief_start:].strip()
    else:
        # Fallback: split by double newline or assume first line is subject
        lines = full_response.split("\n")
        if len(lines) >= 2:
            subject = lines[0].strip()
            brief = "\n".join(lines[1:]).strip()
        else:
            # Last resort: use entire response as brief
            subject = "☀️ Weather Brief"
            brief = full_response.strip()
    
    return (subject, brief)