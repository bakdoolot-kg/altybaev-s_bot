from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup

from config import bot
from keyboards.client_kb import start_markup
from parser import movies, animes, cartoons
from database import psql_db


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, f"Бот 18-1 к вашим услугам {message.from_user.full_name}",
                           reply_markup=start_markup)


async def command_mem(message: types.Message):
    photo = open("media/images/putin.jpg", 'rb')
    await bot.send_photo(message.chat.id, photo=photo)


async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_next = InlineKeyboardButton(
        "Следующий вопрос",
        callback_data='button_next'
    )
    markup.add(button_next)

    question = "Какая функция используется для вывода сообщений в Python?"
    answers = [
        "print("")",
        "print",
        "input=name",
        "name=input"
    ]

    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        explanation="К сожалению не могу подсказать",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )


async def pin_message(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Команда должна быть ответом на сообщение!")
    else:
        await bot.pin_chat_message(message.chat.id, message.message_id)


async def parser_movies(message: types.Message):
    data = movies.parser()
    for movie in data:
        desc = movie['desc'].split(", ")
        await bot.send_message(
            message.from_user.id,
            f"Название: {movie['title']}\n"
            f"Год: #{desc[0]}\n"
            f"Страна: {'' if len(desc) == 2 else f'#{desc[1]}'}\n"
            f"Жанр: #{desc[1] if len(desc) == 2 else desc[2]}\n\n"
            f"{movie['link']}"
        )


async def parser_anime(message: types.Message):
    data = animes.parser()
    for anime in data:
        desc = anime['desc'].split(", ")
        await bot.send_message(
            message.from_user.id,
            f"Название: {anime['title']}\n"
            f"Год: #{desc[0]}\n"
            f"Страна: {'' if len(desc) == 2 else f'#{desc[1]}'}\n"
            f"Жанр: #{desc[1] if len(desc) == 2 else desc[2]}\n\n"
            f"{anime['link']}"
        )


async def parser_cartoons(message: types.Message):
    data = cartoons.parser()
    for cartoon in data:
        desc = cartoon['desc'].split(", ")
        await bot.send_message(
            message.from_user.id,
            f"Название: {cartoon['title']}\n"
            f"Год: #{desc[0]}\n"
            f"Страна: {'' if len(desc) == 2 else f'#{desc[1]}'}\n"
            f"Жанр: #{desc[1] if len(desc) == 2 else desc[2]}\n\n"
            f"{cartoon['link']}"
        )


async def hi(message: types.Message):
    user_id = message.from_user.id
    username = f"@{message.from_user.username}"
    fullname = message.from_user.full_name
    try:
        psql_db.cursor.execute(
            "INSERT INTO users (id, username, fullname) VALUES (%s, %s, %s)",
            (user_id, username, fullname)
        )
        psql_db.cursor.commit()

    except:
        psql_db.cursor.execute("rollback")
        psql_db.cursor.execute(
            "INSERT INTO users (id, username, fullname) VALUES (%s, %s, %s)",
            (user_id, username, fullname)
        )
        psql_db.cursor.commit()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(command_mem, commands=['mem'])
    dp.register_message_handler(pin_message, commands=['pin'], commands_prefix="!/")
    dp.register_message_handler(parser_movies, commands=['film'])
    dp.register_message_handler(parser_anime, commands=['anime'])
    dp.register_message_handler(parser_cartoons, commands=['cartoons'])
    dp.register_message_handler(hi, commands=['hi'])
