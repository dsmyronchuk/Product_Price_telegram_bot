from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()

# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token='6116629666:AAH_6YpUOtVa8nljSAzI_LC81WJnX1wT9aA')
dp = Dispatcher(bot, storage=storage)

