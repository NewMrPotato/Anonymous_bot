# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

# local imports
from handlers.users.search_chat import change_user_status_to_default_message
from keyboards.default import menu_keyboard
from loader import router, dp, bot
from handlers.users.profile import admin_ids

# database
import sqlite3

# Getting link on rules from config
rules_link = open('data/text/config.txt', 'r').readlines()[2].split('\\')[0].replace(' ', '')


# Command handler /rule, send all rules
@dp.message(Command("rules"))
async def start(message: types.Message):
    # Connecting to database
    conn = sqlite3.connect('data/database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM users WHERE tg_id = ?", (message.from_user.id,))

    result = cursor.fetchone()
    user_status = ''

    if result is not None:
        user_status = result[0]

    # Closing database connecting
    cursor.close()
    conn.close()

    # Проверка на вывод с баланса
    if user_status == 'blacklist' and message.from_user.id not in admin_ids:
        await message.answer('Вы были добавлены в черный список⚫️ \n\n'
                             'Для вас доступ к боту запрещен!')
    else:

        await change_user_status_to_default_message(message)

        await message.answer(f'📜<b>Правила поведения в чате можете посмотреть <a href="{rules_link}">здесь</a></b>', parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)
