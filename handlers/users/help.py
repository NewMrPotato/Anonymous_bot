# aiogram
from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command

from keyboards.default import menu_keyboard
# local imports
from loader import router, dp, bot
from handlers.users.search_chat import change_user_status_to_default_message
from handlers.users.profile import admin_ids
# database
import sqlite3


# Command handler /help, send all commands
@dp.message(Command("help"))
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

        await message.answer(
            "🤖 Этот бот предназначен для <i>анонимного общения</i>. Бот может пересылать <b>сообщения, фото, видео, гифки, стикеры, аудиосообщения и тд</b>\n\n"
            "<b>Все комманды для управлением ботом:</b>\n\n"
            "🔍 /search — <i>поиск собеседника</i>\n"
            "💬 /next — <i>закончить текущий диалог и сразу же искать нового собеседника</i>\n"
            "⛔️ /stop — <i>закончить разговор с собеседником</i>\n"
            "👤 /profile - <i>посмотреть ваш профиль</i>\n"
            # "⚙️ /settings — изменить настройки профиля и бота\n"
            "📜 /rules — <i>ознакомиться с правилами</i>\n\n"
            "По любым вопросам обращаться к @anonchatRu_80", parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)
