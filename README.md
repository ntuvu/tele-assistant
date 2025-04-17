# Telegram Bot

A Python-based Telegram bot built with aiogram.

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your bot token:
   ```bash
   cp .env.example .env
   ```
5. Edit `.env` and add your bot token from @BotFather

## Running the Bot

```bash
python src/main.py
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── handlers/
│       ├── __init__.py
│       └── commands.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
``` 