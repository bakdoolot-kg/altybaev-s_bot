from aiogram import Bot, Dispatcher
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
ADMIN = [608718247]
URL = "https://altybaev.herokuapp.com/"
URI = "postgres://epequgptpkadpk:4d84f2513f0adef38e5c1f62953796691d96737b15c9ea2a6954eb80ed7f3bf4@ec2-23-23-182-238.compute-1.amazonaws.com:5432/dbrdguj35auqmn"