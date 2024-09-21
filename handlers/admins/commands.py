# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

from handlers.users.profile import show_profile_callback_request
# local imports
from keyboards.inline import profile_inline_keyboard, gender_inline_keyboard, age_inline_keyboard
from loader import router, dp, bot

# database
import sqlite3

# other
from time import sleep

# Getting admin ids from config
admin_ids = [int(i) for i in
             open('data/text/config.txt', 'r').readlines()[1].split('\\')[0].replace(' ', '').split(',')]


# Handler command /admin
@dp.message(Command("admin"))
async def admin(message: types.Message):
    # Checking is user in admins or not
    if message.from_user.id in admin_ids:
        await message.answer(f'Возможности админов:\n\n'
                             f'1) Чтобы получить данные о определенном пользователе введите команду:\n'
                             f'/user id\n\n'
                             f'2) Чтобы получить данные о определенном количестве пользователей введите команду:\n'
                             f'/users количество\n\n'
                             f'3) Чтобы добавить пользователя в черный список введите команду:\n'
                             f'/blacklist id\n'
                             f'(Чтобы добавить в белый список, нужно ввести эту команду повторно)\n\n')


# Handler command /gettable
@dp.message(Command("gettable"))
async def gettable(message: types.Message):
    # Checking is user in admins or not
    if message.from_user.id in admin_ids:

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {message.text.split(' ')[1]}")
        rows = cursor.fetchall()

        table_str = "id | username | data | gender | age | good_rep | bad_rep | dialogs | messages | status | reports\n"

        for row in rows:
            table_str += " | ".join(str(cell) for cell in row) + "\n"

        conn.close()

        MAX_MESSAGE_LENGTH = 4000

        if len(table_str) > MAX_MESSAGE_LENGTH:
            parts = [table_str[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(table_str), MAX_MESSAGE_LENGTH)]
        else:
            parts = [table_str]

        for part in parts:
            await message.answer(part)


# Handler command /user
@dp.message(Command("user"))
async def users(message: types.Message):
    # Checking is user in admins or not
    if message.from_user.id in admin_ids:
        user_id = int(message.text.split(' ')[1])

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        # Select user data
        cursor.execute(f"SELECT * FROM users WHERE tg_id = ?", (user_id,))
        user_info = cursor.fetchall()[0]

        conn.close()

        await message.answer(f'👤 Профиль: #{user_info[0]}\n'
                             f'✈️ Username: @{user_info[1]}\n'
                             f'📅 Дата регистрации: {user_info[2]}\n'
                             f'⛔️ Жалоб: {user_info[10]}\n'
                             f'👥 Репутация: 👍({user_info[5]}) 👎({user_info[6]})\n'
                             f'👫 Пол: {user_info[3]}\n'
                             f'🔞 Возраст: {user_info[4]}\n'
                             f'💬 Диалогов: {user_info[7]}\n'
                             f'📩 Сообщений: {user_info[8]}\n'
                             f'⭐️ Статус: {user_info[9]}\n\n')


# Handler command /users
@dp.message(Command("users"))
async def users(message: types.Message):
    # Checking is user in admins or not
    if message.from_user.id in admin_ids:
        count = int(message.text.split(' ')[1])

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM users")
        rows = cursor.fetchall()

        table_str = ''

        try:
            for i in range(count):
                row = rows[i]

                table_str += f'👤 Профиль: #{row[0]}\n' \
                             f'✈️ Username: @{row[1]}\n' \
                             f'📅 Дата регистрации: {row[2]}\n' \
                             f'⛔️ Жалоб: {row[10]}\n' \
                             f'👥 Репутация: 👍({row[5]}) 👎({row[6]})\n' \
                             f'👫 Пол: {row[3]}\n' \
                             f'🔞 Возраст: {row[4]}\n' \
                             f'💬 Диалогов: {row[7]}\n' \
                             f'📩 Сообщений: {row[8]}\n' \
                             f'⭐️ Статус: {row[9]}\n\n'
        except Exception as e:
            await message.answer('Столько пользователей нет! Введите меньшее количество')

        conn.close()

        MAX_MESSAGE_LENGTH = 4000

        if len(table_str) > MAX_MESSAGE_LENGTH:
            parts = [table_str[i:i + MAX_MESSAGE_LENGTH] for i in range(0, len(table_str), MAX_MESSAGE_LENGTH)]
        else:
            parts = [table_str]

        for part in parts:
            await message.answer(part)


# Handler command /users
@dp.message(Command("blacklist"))
async def blacklist(message: types.Message):
    # Checking is user in admins or not
    if message.from_user.id in admin_ids:
        user_id = int(message.text.split(' ')[1])

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        # Updating user status
        cursor.execute("SELECT status FROM users WHERE tg_id = ?", (user_id,))

        result = cursor.fetchone()
        bl_user_status = result[0]

        # Adding user to blacklist, if he is not already here
        if bl_user_status != 'blacklist':
            # Выполните запрос
            cursor.execute("""UPDATE users SET status = ? WHERE tg_id = ?""",
                           ('blacklist', user_id))
            conn.commit()

            await message.answer('Пользователь был успешно занесен в черный список⚫️')
        # Если же он уже в черном списке, то заносим его в белый
        else:
            # Выполните запрос
            cursor.execute("""UPDATE users SET status = ? WHERE tg_id = ?""",
                           ('default', user_id))
            conn.commit()

            await message.answer('Пользователь был успешно занесен в белый список⚪️')

        # Закрываем соединение с базой данных
        cursor.close()
        conn.close()
