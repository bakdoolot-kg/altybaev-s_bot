import asyncio
import aioschedule
from aiogram import types, Dispatcher
from config import bot


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text="Id получен, ожидайте...")


async def do_homework():
    photo = open("media/images/justdoit.jpg", "rb")
    await bot.send_photo(chat_id=chat_id, photo=photo, caption="Домашку сделал? Нет? Тогда JUST DO IT!!!")


async def scheduler():
    aioschedule.every().monday.at("11:00").do(do_homework)
    aioschedule.every().thursday.at("11:00").do(do_homework)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_handler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id, lambda word: 'дз' in word.text)