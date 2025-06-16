# TDS Virtual TA 🤖

This is a FastAPI-powered Teaching Assistant bot that can answer student questions using:

- TDS course content (Jan 2025 – Apr 2025)
- Discourse forum posts (Jan 1 – Apr 14, 2025)

## Features

- Accepts student question and image (optional)
- Searches knowledge base for answers
- Returns relevant links with summaries

## Usage

### 1. Local

```bash
uvicorn main:app --reload
