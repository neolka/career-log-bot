# CareerLogBot

CareerLogBot is a Telegram bot for tracking professional achievements in a simple, structured way.  
It helps you regularly record what you did, why it mattered, and what results you achieved. This can help track the progress at work and use this info during interviews.

This project is designed as a clean single-user pet project and can be extended to multi-user mode later.

## Features

- Add daily professional achievements
- Guided flow: **context → action → result**
- View recent achievements (last 5 by default)
- Language switch (English / Ukrainian)
- Reply keyboard navigation
- Local JSON storage

## Tech stack

- Python 3.9+
- python-telegram-bot 20.x
- Async handlers
- JSON-based storage

## Setup

```bash

###1. Clone repository
git clone https://github.com/your-username/careerlogbot.git
cd careerlogbot

##2. Install dependencies
pip install -r requirements.txt

###3. Create Telegram bot
Create your own Telegram bot using @BotFather and get a bot token.

###4. Create .env file in the project root folder
Add
BOT_TOKEN=your_telegram_bot_token

###4. Prepare data storage
cp data/achievements.example.json data/achievements.json

###5. Run the bot using the command:
   python3 main.py

```

Project status

1. Single-user mode (by design)
2. Stable core functionality
3. Ready for extension (multi-user, database, analytics)
