"""llm api interactions."""
import os
import json
from groq import Groq

def generate_weather_brief(prompt: str) -> tuple[str, str]:
    """call groq with json mode for guaranteed parsing."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError("GROQ_API_KEY missing")
        
    client = Groq(api_key=api_key)
    
    # enforcing json mode guarantees the llm returns a parsable object
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_completion_tokens=400,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(completion.choices[0].message.content)
    return result.get("subject", "☀️ Daily Weather Brief"), result.get("body", "Failed to generate brief.")