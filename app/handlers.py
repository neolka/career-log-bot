from telegram import Update
from telegram.ext import ContextTypes
from app.i18n import t, get_lang, set_lang
import logging
from app.keyboards import main_keyboard, language_keyboard
from app.storage import (
    save_achievement,
    load_achievements,
)
from app.database import Database
db = Database()

logger = logging.getLogger(__name__)

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    await update.message.reply_text(
        t("choose_language", lang),
        reply_markup=language_keyboard(),
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    lang = query.data.replace("lang_", "").lower()
    set_lang(user_id, lang)

    await query.edit_message_text(
        t("language_changed", lang)
    )

    # Показуємо меню вже НОВОЮ мовою
    await query.message.reply_text(
        t("choose_action", lang),
        reply_markup=main_keyboard(lang),
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User started bot")
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    # Очищуємо дані користувача при старті
    context.user_data["step"] = None
    context.user_data["answers"] = []

    await update.message.reply_text(
        t("start_message", lang),
        reply_markup=main_keyboard(lang),
    )

async def new_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User started new entry")
    user_id = update.effective_user.id
    lang = get_lang(user_id)

    # Встановлюємо стан ТІЛЬКИ для цього користувача
    context.user_data["step"] = 0
    context.user_data["answers"] = []

    await update.message.reply_text(
        t("question_1", lang),
        reply_markup=main_keyboard(lang),
    )

async def list_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User requested achievements list")
    user_id = update.effective_user.id
    lang = get_lang(user_id)
    achievements = db.get_achievements(user_id)

    if not achievements:
        await update.message.reply_text(t("no_achievements", lang))
        return

    message = "📌 My achievents \n\n"
    for entry in achievements[-5:]:
        message += (
            f"📌 {entry['date']}\n"
            f"{entry['context']}\n"
            f"{entry['action']}\n"
            f"{entry['result']}\n\n"
        )

    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.effective_user.id
    text = update.message.text
    lang = get_lang(user_id)

    # Ініціалізація стану, якщо порожньо
    if "step" not in context.user_data:
        context.user_data["step"] = None
    if "answers" not in context.user_data:
        context.user_data["answers"] = []

    # кнопки меню
    if text == t("btn_new", lang):
        await new_entry(update, context)
        return

    if text == t("btn_list", lang):
        await list_achievements(update, context)
        return
    
    if text == t("btn_language", lang):
        await language(update, context)
        return
    
    # Якщо запис не розпочато
    if context.user_data["step"] is None:
        await update.message.reply_text(
            t("choose_action", lang),
            reply_markup=main_keyboard(lang),
        )
        return

    # Зберігаємо відповідь у список користувача
    context.user_data["answers"].append(text)
    
    current_step = context.user_data["step"]
    logger.info(f"User answered step {current_step}")

    context.user_data["step"] += 1
    next_step_num = context.user_data["step"] + 1

    if next_step_num <= 3:
        key = f"question_{next_step_num}"
        await update.message.reply_text(t(key, lang))
    else:
        # Зберігаємо результат
        db.add_achievement(user_id, context.user_data["answers"])
        
        # Скидаємо стан саме для цього користувача
        context.user_data["step"] = None
        context.user_data["answers"] = []

        await update.message.reply_text(
            t("saved", lang),
            reply_markup=main_keyboard(lang),
        )