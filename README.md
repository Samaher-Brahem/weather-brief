# WhetherAI 🌦️ - Daily Weather Brief

WhetherAI is a lightweight automation project that generates and delivers a personalized daily weather brief via email. It combines real-time weather data, simple decision logic, and an LLM to produce concise, human-like summaries tailored to my routine.

## Overview

Each morning, the system:
- Collects weather data for Antwerp and Brussels
- Determines the type of day (commute, work from home, weekend, or holiday)
- Generates a structured weather brief using an LLM
- Formats the output into a clean HTML email
- Sends it automatically

The goal was to build something practical, reliable, and slightly opinionated in tone. so, basically, it's a daily tool I actually use.

## Architecture

The project is intentionally simple and modular:

- **Data layer**: Open-Meteo API for forecasts, ICS feed for Belgian public holidays  
- **Logic layer**: Day classification and time-based weather segmentation  
- **Generation layer**: Prompt construction + LLM (Groq) with enforced JSON output  
- **Delivery layer**: HTML email formatting and SMTP sending  
- **Automation**: GitHub Actions (scheduled daily run with timezone handling)

## Key Features

- **Day-aware logic**  
  Adapts behavior based on commute days, weekends, and holidays.

- **Time segmentation**  
  Splits the day into five periods (overnight → night) for clearer insights.

- **LLM-structured output**  
  Uses JSON mode to guarantee consistent parsing and formatting.

- **Clean email rendering**  
  Styled HTML with a header, structured sections, and dynamic content.

- **Resilient integrations**  
  Caching, fallbacks (e.g. GIF), and defensive API handling.

- **Fully automated**  
  Runs daily via GitHub Actions with environment-based configuration.

## Project Structure

.
├── main.py
├── config.py
├── .github/workflows/weather_brief.yml
└── src/
├──── day_classifier.py
├──── prompt_builder.py
├──── llm_client.py
├──── email_sender.py
├──── weather.py
└──── holidays.py

## Environment Variables

The project relies on the following secrets:

- `GROQ_API_KEY`
- `GMAIL_USER`
- `GMAIL_PASSWORD`
- `RECIPIENT_EMAIL`
- `GIPHY_API_KEY`

## Design Choices

- **Simplicity over abstraction**  
    The code is kept straightforward and readable, avoiding unnecessary complexity.

- **Deterministic outputs from LLMs**  
    JSON mode is enforced to eliminate parsing issues and ensure reliability.

- **Timezone correctness**  
    All logic is aligned with Europe/Brussels to avoid scheduling inconsistencies.

- **User-first tone**  
    The generated content is intentionally concise and slightly informal, designed for daily consumption.

## Motivation

This project started as a way to automate a small daily habit: Checking the weather before the day starts. It evolved into a compact system that blends APIs, automation, and LLMs into something genuinely useful.

---

Built by <a href="https://www.linkedin.com/in/samaherbrahem/" target="_blank" rel="noopener noreferrer">Samaher Brahem</a>