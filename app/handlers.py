from telegram import Update
from telegram.ext import ContextTypes
import logging

from app.storage import save_achievement, load_achievements
from app.keyboards import main_keyboard
from app.constants import QUESTIONS

logger = logging.getLogger(__name__)

# локальний in-memory state
user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} started bot")

    await update.message.reply_text(
        "Привіт! Я CareerLogBot 🤖\n"
        "Я допоможу тобі фіксувати твої професійні досягнення.\n\n"
        "Обери дію ⬇️",
        reply_markup=main_keyboard(),
    )


async def new_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} started new entry")

    user_states[user_id] = {
        "step": 0,
        "answers": [],
    }

    await update.message.reply_text(
        QUESTIONS[0],
        reply_markup=main_keyboard(),
    )


async def list_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} requested achievements list")

    data = load_achievements()

    if not data:
        await update.message.reply_text("Список досягнень порожній 🫶")
        return

    message = "📌 Твої досягнення:\n\n"
    for entry in data[-5:]:
        message += (
            f"📅 {entry['date']}\n"
            f"Контекст: {entry['context']}\n"
            f"Дія: {entry['action']}\n"
            f"Результат: {entry['result']}\n\n"
        )

    await update.message.reply_text(message)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text

    # кнопки
    if text == "➕ Новий запис":
        await new_entry(update, context)
        return

    if text == "📋 Мої досягнення":
        await list_achievements(update, context)
        return

    # немає активного сценарію
    if user_id not in user_states:
        await update.message.reply_text(
            "Обери дію з меню ⬇️",
            reply_markup=main_keyboard(),
        )
        return

    state = user_states[user_id]
    state["answers"].append(text)

    logger.info(
        f"User {user_id} answered step {state['step']}: {text}"
    )

    state["step"] += 1

    if state["step"] < len(QUESTIONS):
        await update.message.reply_text(QUESTIONS[state["step"]])
    else:
        save_achievement(state["answers"])
        del user_states[user_id]
        await update.message.reply_text(
            "Готово ✅ Твої досягнення збережено.",
            reply_markup=main_keyboard(),
        )
