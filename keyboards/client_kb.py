from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_button = KeyboardButton("/start")
quiz_button = KeyboardButton("/quiz")
dice_button = KeyboardButton("/dice")
menu_button = KeyboardButton("/menu")

film_button = KeyboardButton("/film")
anime_button = KeyboardButton("/anime")
cartoon_button = KeyboardButton("/cartoons")

start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

start_markup.row(start_button, quiz_button, dice_button, menu_button, film_button, anime_button, cartoon_button)

cancel_button = KeyboardButton("CANCEL")
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(cancel_button)