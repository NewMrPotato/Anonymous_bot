# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.default import menu_keyboard
# local imports
from loader import router, dp, bot
from handlers.users.profile import admin_ids
from handlers.users.profile import show_profile_callback_request, show_profile_text_request
from keyboards.inline import age_inline_keyboard

# database
import sqlite3

# other
from time import sleep

# List waiting connect users
waiting_list = []
# Dir for current chats
active_chats = {}


async def search_chat(message: types.Message, next_chat=True):
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

        user_id = message.from_user.id
        # If user is in active chat, annoy him or find new chat
        if user_id in active_chats and next_chat:
            # await message.answer("Вы уже находитесь в чате с другим пользователем.")
            # return
            user_id = message.from_user.id
            partner_id = active_chats.pop(user_id)
            active_chats.pop(partner_id, None)

            # Buttons for evaluate user
            evaluate_buttons = [
                [
                    InlineKeyboardButton(
                        text="👍",
                        callback_data=f'rep/{user_id}/g'
                    ),
                    InlineKeyboardButton(
                        text="👎",
                        callback_data=f'rep/{user_id}/b'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⛔️Пожаловаться",
                        callback_data=f'report/{user_id}'
                    ),
                ],
            ]
            evaluate_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=evaluate_buttons,
                                                            resize_keyboard=True,
                                                            one_time_keyboard=True,
                                                            input_field_placeholder="Choice a button",
                                                            selective=True)

            await bot.send_message(partner_id, "💬 <b>Ваш собеседник покинул(а) чат</b>\n\n"
                                               "✒️ Оставьте отзыв о вашем собеседнике", parse_mode=ParseMode.HTML,
                                   reply_markup=evaluate_inline_keyboard)

            # Buttons for evaluate user
            evaluate_buttons = [
                [
                    InlineKeyboardButton(
                        text="👍",
                        callback_data=f'rep/{partner_id}/g'
                    ),
                    InlineKeyboardButton(
                        text="👎",
                        callback_data=f'rep/{partner_id}/b'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⛔️️Пожаловаться",
                        callback_data=f'report/{partner_id}'
                    ),
                ],
            ]
            evaluate_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=evaluate_buttons,
                                                            resize_keyboard=True,
                                                            one_time_keyboard=True,
                                                            input_field_placeholder="Choice a button",
                                                            selective=True)

            await message.answer("💬 <b>Вы покинули чат</b>\n\n"
                                 "✒️ Оставьте отзыв о вашем собеседнике", parse_mode=ParseMode.HTML,
                                 reply_markup=evaluate_inline_keyboard)

        # If user is in active chat, annoy him or find new chat
        elif user_id in active_chats and not next_chat:
            await message.answer("👥 <b>Вы уже находитесь в чате</b>", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)
            return

        # If user is in waiting list, annoy him
        if user_id in waiting_list:
            await message.answer("👀 <b>Вы уже находитесь в поиске</b>", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)
            return

        # If someone in queue, connect them
        if waiting_list:
            partner_id = waiting_list.pop(0)
            active_chats[user_id] = partner_id
            active_chats[partner_id] = user_id

            # Connecting to database
            conn = sqlite3.connect('data/database/database.sqlite')
            cursor = conn.cursor()

            # Changing count dialogs for first user in database
            cursor.execute("""SELECT dialogs FROM users WHERE tg_id = ?;""", (user_id,))
            dialogs = cursor.fetchone()[0]
            cursor.execute("""UPDATE users SET dialogs = ? WHERE tg_id = ?;""", (dialogs + 1, user_id))

            # Changing count dialogs for second user in database
            cursor.execute("""SELECT dialogs FROM users WHERE tg_id = ?;""", (partner_id,))
            dialogs = cursor.fetchone()[0]
            cursor.execute("""UPDATE users SET dialogs = ? WHERE tg_id = ?;""", (dialogs + 1, partner_id))

            # Getting info about user1
            cursor.execute("SELECT * FROM users WHERE tg_id = ?", (user_id,))
            user_info = cursor.fetchone()

            # Getting info about user2
            cursor.execute("SELECT * FROM users WHERE tg_id = ?", (partner_id,))
            partner_info = cursor.fetchone()

            # Accepting changes
            conn.commit()

            # Closing database connecting
            cursor.close()
            conn.close()

            user_gender = ''
            user_age = 0

            pather_gender = ''
            pather_age = 0

            # Getting gender of user
            if user_info[3] == 'female':
                user_gender = 'Девушка 👱🏻‍♀️'
            elif user_info[3] == 'male':
                user_gender = 'Парень 🧑🏻'
            elif user_info[3] == 'unknown':
                user_gender = 'Неизвестен'

            # Getting age of user
            if user_info[4] == 0:
                user_age = 'Неизвестен'
            else:
                user_age = user_info[4]

            # Getting gender of pather
            if partner_info[3] == 'female':
                pather_gender = 'Девушка 👱🏻‍♀️'
            elif partner_info[3] == 'male':
                pather_gender = 'Парень 🧑🏻'
            elif partner_info[3] == 'unknown':
                pather_gender = 'Неизвестен'

            # Getting age of user
            if partner_info[4] == 0:
                pather_age = 'Неизвестен'
            else:
                pather_age = partner_info[4]

            await bot.send_message(partner_id, "🎭<b>Собеседник найден!</b>\n\n"
                                               f"👫 Пол: <b>{user_gender}</b>\n"
                                               f"🔞 Возраст: <b>{user_age}</b>\n"
                                               f"👥 Репутация: 👍<b>({user_info[5]})</b>👎<b>({user_info[6]})</b>\n\n"
                                               "/next - искать следующего\n"
                                               "/stop - завершить диалог", parse_mode=ParseMode.HTML)
            await message.answer("🎭<b>Собеседник найден!</b>\n\n"
                                 f"👫 Пол: <b>{pather_gender}</b>\n"
                                 f"🔞 Возраст: <b>{pather_age}</b>\n"
                                 f"👥 Репутация: 👍<b>({partner_info[5]})</b>👎<b>({partner_info[6]})</b>\n\n"
                                 "/next - искать следующего\n"
                                 "/stop - завершить диалог", parse_mode=ParseMode.HTML)
        else:
            # else add user in waiting list
            waiting_list.append(user_id)
            await message.answer("🔍 <b>Идет поиск собеседника...</b>", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


# Ending inputting data
async def change_user_status_to_default_message(message: types.Message):
    # Connecting to database
    conn = sqlite3.connect('data/database/database.sqlite')
    cursor = conn.cursor()

    # Changing user gender in database
    cursor.execute("""
                            SELECT status FROM users
                            WHERE tg_id = ?;
                        """, (message.from_user.id,))
    status = cursor.fetchone()[0]

    if status != 'default':
        # Changing user status in database
        cursor.execute("""
                                    UPDATE users
                                    SET status = ?
                                    WHERE tg_id = ?;
                                """, ('default', message.from_user.id))

    # Accepting changes
    conn.commit()

    # Closing database connecting
    conn.close()


# Command handler /search, searching new chat
@dp.message(Command("search"))
async def search(message: types.Message):
    await search_chat(message, next_chat=False)


# Text version of handler /next
@dp.message(F.text == "🚀Искать собеседника")
async def search(message: types.Message):
    await search_chat(message)


# Command handler /next, searching new chat
@dp.message(Command("next"))
async def next_chat(message: types.Message):
    await search_chat(message)


@dp.message(Command("stop"))
async def stop(message: types.Message):
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

        user_id = message.from_user.id
        if user_id in active_chats:
            partner_id = active_chats.pop(user_id)
            active_chats.pop(partner_id, None)

            # Buttons for evaluate user
            evaluate_buttons = [
                [
                    InlineKeyboardButton(
                        text="👍",
                        callback_data=f'rep/{user_id}/g'
                    ),
                    InlineKeyboardButton(
                        text="👎",
                        callback_data=f'rep/{user_id}/b'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⛔️️Пожаловаться",
                        callback_data=f'report/{user_id}'
                    ),
                ],
            ]
            evaluate_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=evaluate_buttons,
                                                            resize_keyboard=True,
                                                            one_time_keyboard=True,
                                                            input_field_placeholder="Choice a button",
                                                            selective=True)

            await bot.send_message(partner_id, "💬 <b>Ваш собеседник покинул(а) чат</b>\n\n"
                                               "✒️ Оставьте отзыв о вашем собеседнике", parse_mode=ParseMode.HTML,
                                   reply_markup=evaluate_inline_keyboard)

            # Buttons for evaluate user
            evaluate_buttons = [
                [
                    InlineKeyboardButton(
                        text="👍",
                        callback_data=f'rep/{partner_id}/g'
                    ),
                    InlineKeyboardButton(
                        text="👎",
                        callback_data=f'rep/{partner_id}/b'
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⛔️️Пожаловаться",
                        callback_data=f'report/{partner_id}'
                    ),
                ],
            ]
            evaluate_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=evaluate_buttons,
                                                            resize_keyboard=True,
                                                            one_time_keyboard=True,
                                                            input_field_placeholder="Choice a button",
                                                            selective=True)

            await message.answer("💬 <b>Вы покинули чат</b>\n\n"
                                 "✒️ Оставьте отзыв о вашем собеседнике", parse_mode=ParseMode.HTML,
                                 reply_markup=evaluate_inline_keyboard)
        elif user_id in waiting_list:
            waiting_list.remove(user_id)
            await message.answer("💤 <b>Поиск прекращен</b>", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)
        else:
            await message.answer("🤷 <b>Вы не находитесь ни в чате, ни в поиске собеседника</b>", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)


# message handler
@router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    # Connecting to database
    conn = sqlite3.connect('data/database/database.sqlite')
    cursor = conn.cursor()

    # Changing user gender in database
    cursor.execute("""
                        SELECT status FROM users
                        WHERE tg_id = ?;
                    """, (message.from_user.id,))
    status = cursor.fetchone()[0]

    # Accepting changes
    conn.commit()

    # Closing database connecting
    conn.close()

    # Проверка на вывод с баланса
    if status == 'blacklist' and message.from_user.id not in admin_ids:
        await message.answer('Вы были добавлены в черный список⚫️ \n\n'
                             'Для вас доступ к боту запрещен!')

    elif user_id in active_chats:
        partner_id = active_chats[user_id]

        # Connecting to database
        conn = sqlite3.connect('data/database/database.sqlite')
        cursor = conn.cursor()

        # Changing count messages for user in database
        cursor.execute("""SELECT messages FROM users WHERE tg_id = ?;""", (user_id,))
        messages = cursor.fetchone()[0]
        cursor.execute("""UPDATE users SET messages = ? WHERE tg_id = ?;""", (messages + 1, user_id))

        # Accepting changes
        conn.commit()

        # Closing database connecting
        conn.close()

        # Handler for different types of message
        try:
            # Text
            if message.text:
                # Replace label "Переслано из..."
                new_message = message.text
                if message.forward_from:
                    new_message = new_message.replace(
                        f"Переслано из {message.forward_from.first_name} {message.forward_from.last_name} ", "")
                await bot.send_message(partner_id, new_message)
                return

            # Voice
            elif message.voice:
                await bot.send_voice(partner_id, message.voice.file_id)
                return

            # Video
            elif message.video:
                await bot.send_video(partner_id, message.video.file_id)
                return

            # Stickers
            elif message.sticker:
                await bot.send_sticker(partner_id, message.sticker.file_id)
                return

            # Animations
            elif message.animation:
                await bot.send_animation(partner_id, message.animation.file_id)
                return

            # Photo
            elif message.photo:
                await bot.send_photo(partner_id, message.photo[-1].file_id)
                return

            # Audio
            elif message.audio:
                await bot.send_audio(partner_id, message.audio.file_id)
                return

            # Document
            elif message.document:
                await bot.send_document(partner_id, message.document.file_id)
                return

            # Location
            elif message.location:
                await bot.send_location(partner_id, message.location.latitude, message.location.longitude)
                return

            # Contact
            elif message.contact:
                await bot.send_contact(partner_id, message.contact.phone_number, message.contact.first_name,
                                       message.contact.last_name)
                return

            # Venue
            elif message.venue:
                await bot.send_venue(partner_id, message.venue.latitude, message.venue.longitude, message.venue.title,
                                     message.venue.address)
                return

            # Poll
            elif message.poll:
                # Пересылка опроса не поддерживается API aiogram
                await message.answer("Извините, но переслать опрос я не могу 🤷", reply_markup=menu_keyboard)
                return

            # Expected type
            else:
                await message.answer("Извините, но я не могу переслать этот тип сообщения 🤷", reply_markup=menu_keyboard)
                return
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    #     await bot.send_message(partner_id, message.text)
    #
    #     try:
    #         # Убираем приписку "Переслано из..."
    #         new_message = message.text
    #         if message.forward_from:
    #             new_message = new_message.replace(
    #                 f"Переслано из {message.forward_from.first_name} {message.forward_from.last_name} ", "")
    #
    #         # Пересылаем сообщение
    #         await bot.send_message(partner_id, new_message)
    #
    #         # Отправляем подтверждение
    #         await message.answer("Сообщение переслано!")
    #     except Exception as e:
    #         await message.answer(f"Произошла ошибка: {e}")
    elif status == 'age':
        age = message.text

        # Checking valid of input age
        if age.isdigit():
            if 9 <= int(age) <= 99:

                # Connecting to database
                conn = sqlite3.connect('data/database/database.sqlite')
                cursor = conn.cursor()

                # Changing user gender in database
                cursor.execute("""
                                UPDATE users
                                SET age = ?
                                WHERE tg_id = ?;
                            """, (age, message.from_user.id))

                # Accepting changes
                conn.commit()

                # Closing database connecting
                conn.close()

                await message.answer('Ваш возраст был успешно изменен✅')

                sleep(1)

                await show_profile_text_request(message)

            # if age input is incorrect
            else:
                await message.answer('Некоректное ввод возраста❌\n'
                                     'Проверьте, что число правильно записано')

                sleep(1)

                await message.answer('<b>Введите ваш возраст цифрами (от 9 до 99)</b>\n\n'
                                     'Например, если вам 18 год, напишите 18 <i>(Без пробелов)</i>⬇️',
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=age_inline_keyboard)
        else:
            await message.answer('Некоректное ввод возраста❌\n'
                                 'Проверьте, что число правильно записано')

            sleep(1)

            await message.answer('<b>Введите ваш возраст цифрами (от 9 до 99)</b>\n\n'
                                 'Например, если вам 18 год, напишите 18 <i>(Без пробелов)</i>⬇️',
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=age_inline_keyboard)
    else:
        await message.answer("Используйте /search для поиска собеседника", reply_markup=menu_keyboard)
