# CareerLogBot

Telegram bot for tracking professional achievements.

## Features

- Add daily achievements
- View recent achievements (by default - last 5)
- Reply keyboard navigation

## Tech stack

- Python 3.9+
- python-telegram-bot 20.x

## Setup

1. Clone repository
2. Create virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

General flow:

1. Create you owm bot in Telegtam using instructions from @botFather to get your own bot token
2. Clone repo
3. Create .env file in the root folder
4. Add your_telegram_bot_token to the .env file e.g. BOT_TOKEN=your_telegram_bot_token
5. Create data file in the data folder
   cp data/achievements.example.json data/achievements.json
6. Run bot using the command:
   python3 main.py
