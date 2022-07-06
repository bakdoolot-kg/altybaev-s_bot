from random import choice

from aiogram import types, Dispatcher
from aiogram.types import ParseMode

from config import bot, ADMIN


async def handle_message(message: types.Message):
    try:
        if message.text == "Следующий вопрос >":
            print(message)
            question = "В чем, по распространенному мнению, должно повезти, если не везет в картах?"
            answers = [
                "В дружбе",
                "В Работе",
                "В спорте",
                "В любви",
            ]

            await bot.send_poll(
                chat_id=message.chat.id,
                question=question,
                options=answers,
                is_anonymous=False,
                type='quiz',
                correct_option_id=3,
                explanation="Сам думай",
                explanation_parse_mode=ParseMode.MARKDOWN_V2,
            )

        if message.text.startswith('game'):
            if message.from_user.id not in ADMIN:
                await message.answer('Играть дозволено только Админам ;) ')
            else:
                dices = ["⚽", "🏀", "🎲", "🎯", "🎳", "🎰"]
                await bot.send_dice(message.chat.id, emoji=choice(dices))

        num = int(message.text) ** 2
        await bot.send_message(message.chat.id, num)
    except:
        pass


def register_handlers_extra(dp: Dispatcher):
    dp.register_message_handler(handle_message)
