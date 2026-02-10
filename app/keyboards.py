from telegram import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
from app.i18n import t


def main_keyboard(lang: str):
        keyboard = [
            [KeyboardButton(t("btn_new", lang))],
            [KeyboardButton(t("btn_list", lang))],
            [KeyboardButton(t("btn_language", lang))],
        ]

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
        )

def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_ua"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ])