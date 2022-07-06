from aiogram import types, Dispatcher
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from config import bot


async def quiz_2(call: types.CallbackQuery):
    answer_next_button = KeyboardButton('Следующий вопрос >')
    answer_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    answer_markup.add(answer_next_button)

    question = "Какой синтаксис вы бы использовали при создании переменной для ввода имени?"
    answers = [
        "input=name",
        "name=input{}",
        "name=INPUT",
        "name=input()",
    ]

    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        explanation="Сам думай",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=answer_markup
    )


def register_handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_next")
