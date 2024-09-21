# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

# local imports
from handlers.users.profile import show_profile_callback_request
from handlers.users.profile import admin_ids
from keyboards.inline import gender_inline_keyboard
from loader import router, dp, bot

# database
import sqlite3

# other
from time import sleep


# Show a panel to user for changing gender
@router.callback_query(lambda query: query.data == "change_gender")
async def gender_handler(callback: types.CallbackQuery):
    await callback.message.edit_text('<b>Выберите ваш пол:</b>', parse_mode=ParseMode.HTML, reply_markup=gender_inline_keyboard)


# Change user gender to male
@router.callback_query(lambda query: query.data == "change_gender_male")
async def gender_male_handler(callback: types.CallbackQuery):
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
                    SET gender = ?
                    WHERE tg_id = ?;
                """, ('male', callback.from_user.id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await callback.message.edit_text('<b>Ваш пол был успешно изменен</b>✅',  parse_mode=ParseMode.HTML)

        sleep(1)

        await show_profile_callback_request(callback, edit=True)


# Change user gender to female
@router.callback_query(lambda query: query.data == "change_gender_female")
async def gender_female_handler(callback: types.CallbackQuery):
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
                    SET gender = ?
                    WHERE tg_id = ?;
                """, ('female', callback.from_user.id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        await callback.message.edit_text('Ваш пол был успешно изменен✅')

        sleep(1)

        await show_profile_callback_request(callback, edit=True)
