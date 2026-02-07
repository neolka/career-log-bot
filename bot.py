from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import BOT_TOKEN
import json
from datetime import datetime
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton


QUESTIONS = [
    "Над чим ти сьогодні працювала?",
    "Що саме ти зробила?",
    "Який результат або користь це дало?"
]

user_states = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def main_keyboard():
    keyboard = [
        [KeyboardButton("➕ Новий запис")],
        [KeyboardButton("📋 Мої досягнення")]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Обери дію"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.message.from_user.id} started bot")
    await update.message.reply_text(
        "Привіт! Я CareerLogBot 🤖\n"
        "Я допоможу тобі фіксувати твої професійні досягнення.\n\n"
        "Напиши /new щоб додати новий запис.\n"
        "Напиши /list щоб побачити 5 останніх записів\n"
        "Або обери дію ⬇️",
        reply_markup=main_keyboard()
    )

async def new_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    logger.info(f"User {user_id} started a new achievement entry")

    user_states[user_id] = {
        "step": 0,
        "answers": []
    }
    await update.message.reply_text(
        QUESTIONS[0],
        reply_markup=main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_id = update.message.from_user.id

    text = update.message.text

    if text == "➕ Новий запис":
        await new_entry(update, context)
        return

    if text == "📋 Мої досягнення":
        await list_achievements(update, context)
        return

    if user_id not in user_states:
        await update.message.reply_text("Напиши /new щоб почати новий запис 🙂")
        return

    state = user_states[user_id]
    state["answers"].append(update.message.text)
    
    logger.info(f"User {user_id} answered step {state['step']}: {update.message.text}")
    
    state["step"] += 1

    if state["step"] < len(QUESTIONS):
        await update.message.reply_text(QUESTIONS[state["step"]])
    else:
        save_achievement(state["answers"])
        del user_states[user_id]
        await update.message.reply_text("Готово ✅ Твої досягнення збережено.")

def save_achievement(answers):
    achievement = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "context": answers[0],
        "action": answers[1],
        "result": answers[2]
    }

    try:
        with open("achievements.json", "r", encoding="utf-8") as f:
            content = f.read().strip()
            data = json.loads(content) if content else []
    except FileNotFoundError:
        data = []

    data.append(achievement)

    with open("achievements.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info("Achievement successfully saved")


async def list_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("User requested achievements list")
    
    try:
        with open("achievements.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        await update.message.reply_text("Поки що немає жодного запису 🙂")
        return

    if not data:
        await update.message.reply_text("Список досягнень порожній 🫶")
        return

    message = "📌 Твої досягнення:\n\n"

    for entry in data[-5:]:  # останні 5
        message += (
            f"📌 {entry['date']}\n"
            f"Контекст: {entry['context']}\n"
            f"Дія: {entry['action']}\n"
            f"Результат: {entry['result']}\n\n"
        )

    await update.message.reply_text(message)


def main():
    logger.info("BOT STARTED")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_entry))
    app.add_handler(CommandHandler("list", list_achievements))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.run_polling()

if __name__ == "__main__":
    main()
