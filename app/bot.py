from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
import os
from config.config import BOT_TOKEN
from app.handlers import (
    start,
    new_entry,
    list_achievements,
    handle_message,
    language,
    language_callback,
)

def run_bot():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_entry))
    app.add_handler(CommandHandler("list", list_achievements))
    app.add_handler(CommandHandler("language", language))

    app.add_handler(CallbackQueryHandler(language_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()