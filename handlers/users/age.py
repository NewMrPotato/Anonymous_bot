# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

# local imports
from handlers.users.profile import show_profile_callback_request
from keyboards.inline import profile_inline_keyboard, gender_inline_keyboard, age_inline_keyboard
from loader import router, dp, bot
from handlers.users.profile import admin_ids

# database
import sqlite3

# other
from time import sleep


# Show a panel to user for changing gender
@router.callback_query(lambda query: query.data == "change_age")
async def age_handler(callback: types.CallbackQuery):
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

        # Changing user gender in database
        cursor.execute("""
                            UPDATE users
                            SET status = ?
                            WHERE tg_id = ?;
                        """, ('age', callback.from_user.id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await callback.message.edit_text('<b>Введите ваш возраст цифрами (от 9 до 99)</b>\n\n'
                                         'Например, если вам 18 год, напишите 18 <i>(Без пробелов)</i>⬇️',
                                         parse_mode=ParseMode.HTML, reply_markup=age_inline_keyboard)


# Deleting user age
@router.callback_query(lambda query: query.data == "delete_age")
async def deleting_age_handler(callback: types.CallbackQuery):
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

        # Changing user gender in database
        cursor.execute("""
                        UPDATE users
                        SET age = ?
                        WHERE tg_id = ?;
                    """, (0, callback.from_user.id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await callback.message.edit_text('Ваш возраст был успешно удален✅')

        sleep(1)

        await show_profile_callback_request(callback, edit=True)

