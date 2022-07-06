from aiogram import types, Dispatcher

from config import bot, ADMIN
from database.bot_db import sql_commands_get_all_id
from database import psql_db


async def dice(message: types.Message):
    user = await bot.send_dice(message.chat.id, emoji="🎲")
    pc = await bot.send_dice(message.chat.id, emoji="🎲")

    if user.dice.value > pc.dice.value:
        await message.answer(f'Победил {message.from_user.full_name}')
    elif user.dice.value == pc.dice.value:
        await message.answer('Ничья!')
    else:
        await message.answer(f'Победил Бот (Точнее Я)')


async def mailing(message: types.Message):
    if message.from_user.id in ADMIN:
        result = await sql_commands_get_all_id()
        print(result)
        for id in result:
            await bot.send_message(id[0], message.text[3:])
    else:
        await message.answer("Ты не мой БОСС!!!")


async def get_all_users(message: types.Message):
    if message.from_user.id in ADMIN:
        all_users = psql_db.cursor.execute("SELECT * FROM users")
        result = psql_db.cursor.fetchall()
        answer = ""
        for row in result:
            answer += f"ID {row[0]}\nUsername: {row[1]}\nFullname: {row[2]}\n\n"
        answer += f"{len(result)} users"
        await message.answer(answer)
    else:
        await message.answer("Ты не мой БОСС!!!")


async def mailing_for_users(message: types.Message):
    if message.from_user.id in ADMIN:
        all_users = psql_db.cursor.execute("SELECT id FROM users")
        result = psql_db.cursor.fetchall()
        print(result)
        for id in result:
            await bot.send_message(id[0], message.text[4:])
    else:
        await message.answer("Ты не мой БОСС!!!")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(dice, commands=["dice"])
    dp.register_message_handler(mailing, commands=["R"])
    dp.register_message_handler(mailing_for_users, commands=["R2"])
    dp.register_message_handler(get_all_users, commands=["users"])
