# Weather Brief Automator 🌤️

A lightweight, automated script that sends you a smart daily weather briefing every morning. 

Instead of opening a weather app and figuring out what to wear, this script pulls data from Open-Meteo, figures out if you're commuting or working from home, and uses an AI (Groq + Llama 3) to write you a quick, human-friendly email summary.

## What it does
* **Tracks your whole day:** Summarizes the weather in 5 blocks: Overnight (0-6h), Morning (6-11h), Midday (11-16h), Evening (16-20h), and Night (20-24h).
* **Location aware:** If it's a commute day, it automatically checks the destination city's weather for your work hours.
* **Smart Subjects:** The AI generates a unique subject line every day based on the actual forecast (e.g., "🌧️ Bring an umbrella!").

## Setup
1. Clone the repo and `pip install -r requirements.txt`.
2. Create a `.env` file with:
   ```env
   GROQ_API_KEY=your_key
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASSWORD=your_app_password
   RECIPIENT_EMAIL=where_to_send@email.com