import os
from aiogram import Bot, types, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


bot = Bot(token=open('data/text/config.txt', 'r').readlines()[0].split('\\')[0].replace(' ', ''), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
router = Router()
dp.include_router(router)
