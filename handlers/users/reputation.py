# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import CallbackQuery

# local imports
from handlers.users.profile import show_profile_callback_request
from keyboards.inline import profile_inline_keyboard, gender_inline_keyboard, age_inline_keyboard
from loader import router, dp, bot
from handlers.users.profile import admin_ids

# database
import sqlite3


# Show a panel to user for setting reputation
@router.callback_query(lambda query: query.data.split('/')[0] == "rep")
async def rep_handler(callback: types.CallbackQuery):
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
        # Получаем данные из обратного вызова
        callback_data = callback.data
        callback_data = callback_data.split('/')

        user_id = callback_data[1]

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        if callback_data[2] == 'g':
            # Changing count good_rep for second user in database
            cursor.execute("""SELECT good_rep FROM users WHERE tg_id = ?;""", (user_id,))
            good_rep = cursor.fetchone()[0]
            cursor.execute("""UPDATE users SET good_rep = ? WHERE tg_id = ?;""", (good_rep + 1, user_id))

        elif callback_data[2] == 'b':
            # Changing count bad_rep for second user in database
            cursor.execute("""SELECT bad_rep FROM users WHERE tg_id = ?;""", (user_id,))
            bad_rep = cursor.fetchone()[0]
            cursor.execute("""UPDATE users SET bad_rep = ? WHERE tg_id = ?;""", (bad_rep + 1, user_id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await callback.message.edit_text('<b>Отзыв успешно оставлен. Спасибо за обратную связь!</b>', parse_mode=ParseMode.HTML)


# Show a panel to user for setting report
@router.callback_query(lambda query: query.data.split('/')[0] == "report")
async def report_handler(callback: types.CallbackQuery):
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
        # Получаем данные из обратного вызова
        callback_data = callback.data
        callback_data = callback_data.split('/')

        user_id = callback_data[1]

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        # Changing count dialogs for second user in database
        cursor.execute("""SELECT reports FROM users WHERE tg_id = ?;""", (user_id,))
        reports = cursor.fetchone()[0] + 1
        cursor.execute("""UPDATE users SET reports = ? WHERE tg_id = ?;""", (reports, user_id))

        # Annoying administration about spam
        if reports > 10:
            # Getting username of reported user
            cursor.execute("""SELECT username FROM users WHERE tg_id = ?;""", (user_id,))
            username = cursor.fetchone()[0]

            for ida in admin_ids:
                await bot.send_message(ida, f'Пользователь с ID: {user_id} (@{username}) получил больше 10 репортов за спам, {reports} репортов')

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await callback.message.edit_text('<b>Отзыв успешно оставлен. Спасибо за обратную связь!</b>', parse_mode=ParseMode.HTML)

