import requests
from datetime import datetime, timedelta

ICS_URL = "https://www.officeholidays.com/ics-all/belgium"


def test_next_30_days():
    print("🔍 Checking next 30 days holidays...\n")

    today = datetime.now()
    end_date = today + timedelta(days=30)

    try:
        response = requests.get(ICS_URL, timeout=10)
        response.raise_for_status()

        print("✅ ICS downloaded\n")

        lines = response.text.splitlines()

        holidays = []

        current_date = None
        current_name = None

        for line in lines:
            # Capture event date
            if "DTSTART" in line:
                try:
                    date_str = line.split(":")[1].strip()
                    current_date = datetime.strptime(date_str, "%Y%m%d")
                except Exception:
                    current_date = None

            # Capture event name
            elif line.startswith("SUMMARY"):
                current_name = line.split(":", 1)[1]

                # Only store if both date + name exist
                if current_date and today <= current_date <= end_date:
                    holidays.append((current_date, current_name))

                # Reset for next event
                current_date = None
                current_name = None

        # Sort by date
        holidays.sort()

        if holidays:
            print("🎉 Upcoming holidays:\n")
            for date, name in holidays:
                print(f"{date.strftime('%Y-%m-%d')} → {name}")
        else:
            print("ℹ️ No holidays in next 30 days")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_next_30_days()




    """HEEEEEHI PROMPTS.PY"""

    # These are the base LLM prompts.
# ⚡ Instructions are highly detailed to structure output as bullets + summary.

COMMUTE_DAY_PROMPT = """
You are a sarcastic, witty weather brief writer. Generate a weather brief for someone commuting between Antwerp and Brussels.

📌 Only include:
- Bullet points for Morning, Midday, Evening
- Summary at the end

RULES:
- Start with Hi Sam/Hi Samaher only once at the intro
- Each bullet: 1-2 sentences max, include:
  * Temperature range
  * Wind speed
  * Rain probability
- End summary: overall impression + any tips
- Friendly and witty, short humor allowed, not over the top

FORMAT:
- **Morning**: ...
- **Midday**: ...
- **Evening**: ...
- **Summary**: ...
"""

WFH_DAY_PROMPT = """
You are a witty weather brief writer. Generate a weather brief for someone working from home.

📌 Only include:
- Bullet points for Morning, Midday, Evening
- Summary at the end

RULES:
- Use simple language
- Only mention Antwerp weather
- Start with Hi Sam/Hi Samaher at the intro
- Each bullet: temperature range, wind, rain
- Summary: overall day impression, any indoor/outdoor tips

FORMAT:
- **Morning**: ...
- **Midday**: ...
- **Evening**: ...
- **Summary**: ...
"""

HOLIDAY_WEEKEND_PROMPT = """
You are a witty weather brief writer. Generate a weather brief for a Belgian public holiday or weekend day.

📌 Only include:
- Bullet points for Morning, Midday, Evening
- Summary at the end

RULES:
- Use friendly, witty language
- Start with Hi Sam/Hi Samaher at the intro
- Include temperature range, wind, rain probability for each bullet
- Summary: overall day impression + tips for the holiday or weekend

FORMAT:
- **Morning**: ...
- **Midday**: ...
- **Evening**: ...
- **Summary**: ...
"""