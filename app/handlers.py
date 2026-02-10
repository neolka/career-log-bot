from telegram import Update
from telegram.ext import ContextTypes
from app.i18n import t, get_lang, set_lang
import logging
from app.keyboards import main_keyboard, language_keyboard
from app.storage import (
    save_achievement,
    load_achievements,
)

logger = logging.getLogger(__name__)

# single-user in-memory state
STATE = {
    "step": None,
    "answers": [],
}

async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang()

    await update.message.reply_text(
        t("choose_language", lang),
        reply_markup=language_keyboard(),
    )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = query.data.replace("lang_", "").lower()
    set_lang(lang)

    await query.edit_message_text(
        t("language_changed", lang)
    )

    # показуємо меню вже НОВОЮ мовою
    await query.message.reply_text(
        t("choose_action", lang),
        reply_markup=main_keyboard(lang),
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User started bot")
    lang = get_lang()

    STATE["step"] = None
    STATE["answers"] = []

    await update.message.reply_text(
        t("start_message", lang),
        reply_markup=main_keyboard(lang),
    )

async def new_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User started new entry")
    lang = get_lang()

    STATE["step"] = 0
    STATE["answers"] = []

    await update.message.reply_text(
        t("question_1", lang),
        reply_markup=main_keyboard(lang),
    )

async def list_achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User requested achievements list")

    lang = get_lang()
    achievements = load_achievements()

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

    text = update.message.text
    lang = get_lang()

    # кнопки
    if text == t("btn_new", lang):
        await new_entry(update, context)
        return

    if text == t("btn_list", lang):
        await list_achievements(update, context)
        return
    
    if text == t("btn_language", lang):
        await language(update, context)
        return

    # немає активного сценарію
    if STATE["step"] is None:
        await update.message.reply_text(
            t("choose_action", lang),
            reply_markup=main_keyboard(lang),
        )
        return


    STATE["answers"].append(text)

    logger.info(
        f"User answered step {STATE['step']}: {text}"
    )

    STATE["step"] += 1

    next_step = STATE["step"] + 1
    key = f"question_{next_step}"

    if next_step <= 3:
        await update.message.reply_text(t(key, lang))
    else:
        save_achievement(STATE["answers"])
        STATE["step"] = None
        STATE["answers"] = []

        await update.message.reply_text(
            t("saved", lang),
            reply_markup=main_keyboard(lang),
        )
