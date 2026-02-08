from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    keyboard = [
        [KeyboardButton("➕ Новий запис")],
        [KeyboardButton("📋 Мої досягнення")],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Обери дію"
    )
