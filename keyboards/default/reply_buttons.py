# aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Кнопки для главного меню
menu_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text="🚀Искать собеседника"
        )
    ],
    [
        KeyboardButton(
            text="👤Профиль"
        )
    ],
    # [
    #     KeyboardButton(
    #         text="⚙️Настройки"
    #     )
    # ]
    # [
    #     KeyboardButton(
    #         text="📖Интересы поиска"
    #     )
    # ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Choice a button", selective=True)
