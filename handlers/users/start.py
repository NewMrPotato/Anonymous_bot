# aiogram
import datetime

from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command

from handlers.users.search_chat import change_user_status_to_default_message
# local imports
from keyboards.default import menu_keyboard
from loader import router, dp, bot

# database
import sqlite3

# Getting admin ids from config
admin_ids = [int(i) for i in
             open('data/text/config.txt', 'r').readlines()[1].split('\\')[0].replace(' ', '').split(',')]


# Handler command /start
@dp.message(Command("start"))
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
        await message.answer("🌐 <b>Главное меню</b>\n\n"
                             "✏️Для использования бота пользуйся <i>кнопками снизу</i> или <i>меню команд</i>\n\n"
                             "📑Весь список команд вы можете увидеть, написав команду /help", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE tg_id = ?", (message.from_user.id,))
        count = cursor.fetchone()[0]

        # Closing database connecting
        cursor.close()
        conn.close()

        if not (count > 0):  # checking already exist user in database
            # Connecting to database
            conn = sqlite3.connect('data/database/database.sqlite')
            cursor = conn.cursor()

            # Getting current time using datetime
            today = datetime.datetime.now()

            # New user data
            user_id = message.from_user.id
            date_regist = today.date()
            gender = 'unknown'
            age = 0
            good_rep = 0
            bad_rep = 0
            dialogs = 0
            messages = 0
            username = message.from_user.username
            status = 'default'
            reports = 0

            # If username is hidden, set UNKNOWN
            if username is None:
                username = 'UNKNOWN'

            # Requesting to adding new user
            cursor.execute(
                "INSERT INTO users (tg_id, username, date_regist, gender, gender, good_rep, bad_rep, dialogs, messages, status, reports) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, username, date_regist, gender, age, good_rep, bad_rep, dialogs, messages, status, reports))
            print(f"ID: {user_id}, Username: {username}, Date registered: {date_regist}")

            # Accepting changes
            conn.commit()

            # Closing database connecting
            conn.close()

        await change_user_status_to_default_message(message)
