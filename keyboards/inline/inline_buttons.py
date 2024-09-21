
# aiogram
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Buttons for profile to change profile
profile_buttons = [
    [
        InlineKeyboardButton(
            text="👫Изменить пол",
            callback_data='change_gender'
        ),
        InlineKeyboardButton(
            text="🔞Изменить возраст",
            callback_data='change_age'
        )
    ],
    [
        # InlineKeyboardButton(
        #     text="👫Изменить пол",
        #     callback_data='change_gender'
        # ),
        # InlineKeyboardButton(
        #     text="🔞Изменить возраст",
        #     callback_data='change_age'
        # )
    ],
]
profile_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=profile_buttons,
                                               resize_keyboard=True,
                                               one_time_keyboard=True,
                                               input_field_placeholder="Choice a button",
                                               selective=True)

# Buttons for profile to change profile
gender_buttons = [
    [
        InlineKeyboardButton(
            text="Парень🧑🏻",
            callback_data='change_gender_male'
        ),
        InlineKeyboardButton(
            text="Девушка👱🏻‍♀️",
            callback_data='change_gender_female'
        )
    ],
    [
        InlineKeyboardButton(
            text="⬅️Назад",
            callback_data='back_to_profile'
        ),
    ],
]
gender_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=gender_buttons,
                                               resize_keyboard=True,
                                               one_time_keyboard=True,
                                               input_field_placeholder="Choice a button",
                                               selective=True)

# Buttons for profile to change profile
age_buttons = [
    [
        InlineKeyboardButton(
            text="❌Удалить возраст",
            callback_data='delete_age'
        ),
    ],
    [
        InlineKeyboardButton(
            text="⬅️Назад",
            callback_data='back_to_profile'
        ),
    ],
]
age_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=age_buttons,
                                               resize_keyboard=True,
                                               one_time_keyboard=True,
                                               input_field_placeholder="Choice a button",
                                               selective=True)

