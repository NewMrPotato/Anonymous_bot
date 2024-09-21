# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

# local imports
from keyboards.inline import profile_inline_keyboard, gender_inline_keyboard
from loader import router, dp, bot

# database
import sqlite3

# Getting admin ids from config
admin_ids = [int(i) for i in
             open('data/text/config.txt', 'r').readlines()[1].split('\\')[0].replace(' ', '').split(',')]


# Show profile to user, if request from text message
async def show_profile_text_request(message: types.Message, edit=False):
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
        global gender, age

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE tg_id = ?", (message.from_user.id,))
        result = cursor.fetchone()

        # Changing user status in database
        cursor.execute("""
                                UPDATE users
                                SET status = ?
                                WHERE tg_id = ?;
                            """, ('default', message.from_user.id))

        # Closing database connecting
        cursor.close()
        conn.close()

        # Getting gender of user
        if result[3] == 'female':
            gender = 'Девушка 👱🏻‍♀️'
        elif result[3] == 'male':
            gender = 'Парень 🧑🏻'
        elif result[3] == 'unknown':
            gender = 'Неизвестен'

        # Getting age of user
        if result[4] == 0:
            age = 'Неизвестен'
        else:
            age = result[4]

        profile_text = f'🔎 ID: <b>{result[0]}</b>\n' \
                       f'📅 Вы были зарегистрированы: <b>{result[2]}</b>\n\n' \
                       f'👫 Пол: <b>{gender}</b>\n' \
                       f'🔞 Возраст: <b>{age}</b>\n' \
                       f'➖➖➖➖➖➖➖➖➖➖\n' \
                       f"📊 Статистика:\n\n" \
                       f"💬 Всего диалогов: <b>{result[7]}</b>\n" \
                       f"📩 Ты отправил(а) сообщений: <b>{result[8]}</b>\n\n" \
                       f"👥 Репутация: 👍<b>({result[5]})</b>👎<b>({result[6]})</b>"
        # f'Интересы:'

        if edit:
            await message.edit_text(profile_text, parse_mode=ParseMode.HTML,
                                    reply_markup=profile_inline_keyboard)
        else:
            await message.answer(profile_text, parse_mode=ParseMode.HTML,
                                 reply_markup=profile_inline_keyboard)


# Show profile to user, if request from callback message
async def show_profile_callback_request(callback: types.CallbackQuery, edit=False):
    # Connecting to database
    conn = sqlite3.connect('data/database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM users WHERE tg_id = ?", (callback.from_user.id,))

    result = cursor.fetchone()
    user_status = ''

    if result is not None:
        user_status = result[0]

    # Closing database connecting
    cursor.close()
    conn.close()

    # Проверка на вывод с баланса
    if user_status == 'blacklist' and callback.from_user.id not in admin_ids:
        await callback.answer('Вы были добавлены в черный список⚫️ \n\n'
                              'Для вас доступ к боту запрещен!')
    else:
        global gender, age

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE tg_id = ?", (callback.from_user.id,))
        result = cursor.fetchone()

        # Changing user status in database
        cursor.execute("""
                                UPDATE users
                                SET status = ?
                                WHERE tg_id = ?;
                            """, ('default', callback.from_user.id))

        # Closing database connecting
        cursor.close()
        conn.close()

        # Getting gender of user
        if result[3] == 'female':
            gender = 'Девушка 👱🏻‍♀️'
        elif result[3] == 'male':
            gender = 'Парень 🧑🏻'
        elif result[3] == 'unknown':
            gender = 'Неизвестен'

        # Getting age of user
        if result[4] == 0:
            age = 'Неизвестен'
        else:
            age = result[4]

        profile_text = f'🔎 ID: <b>{result[0]}</b>\n' \
                       f'📅 Вы были зарегистрированы: <b>{result[2]}</b>\n\n' \
                       f'👫 Пол: <b>{gender}</b>\n' \
                       f'🔞 Возраст: <b>{age}</b>\n' \
                       f'➖➖➖➖➖➖➖➖➖➖\n' \
                       f"📊 Статистика:\n\n" \
                       f"💬 Всего диалогов: <b>{result[7]}</b>\n" \
                       f"📩 Ты отправил(а) сообщений: <b>{result[8]}</b>\n\n" \
                       f"👥 Репутация: 👍<b>({result[5]})</b>👎<b>({result[6]})</b>"
        # f'Интересы:'

        if edit:
            await callback.message.edit_text(profile_text, reply_markup=profile_inline_keyboard)
        else:
            await callback.message.answer(profile_text, reply_markup=profile_inline_keyboard)


# Text version of handler /profile
@dp.message(F.text == "👤Профиль")
async def profile(message: types.Message):
    await show_profile_text_request(message)


# Command handler /profile, searching new chat
@dp.message(Command("profile"))
async def profile(message: types.Message):
    await show_profile_text_request(message)


# Come backing to profile
@router.callback_query(lambda query: query.data == "back_to_profile")
async def back_to_profile_handler(callback: types.CallbackQuery):
    # Connecting to database
    conn = sqlite3.connect('data/database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM users WHERE tg_id = ?", (callback.from_user.id,))

    result = cursor.fetchone()
    user_status = ''

    if result is not None:
        user_status = result[0]

    # Closing database connecting
    cursor.close()
    conn.close()

    # Проверка на вывод с баланса
    if user_status == 'blacklist' and callback.from_user.id not in admin_ids:
        await callback.answer('Вы были добавлены в черный список⚫️ \n\n'
                              'Для вас доступ к боту запрещен!')
    else:
        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        # Changing user status in database
        cursor.execute("""
                            UPDATE users
                            SET status = ?
                            WHERE tg_id = ?;
                        """, ('default', callback.from_user.id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await show_profile_callback_request(callback, edit=True)
