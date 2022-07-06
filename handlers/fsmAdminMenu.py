from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import bot, ADMIN
from keyboards.client_kb import cancel_markup
from database import psql_db


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id not in ADMIN:
            await message.answer('Добавлять блюда может только админ!')
        else:
            await FSMAdmin.photo.set()
            await message.answer(f"Приветсвую {message.from_user.full_name}, "
                                 f"отправьте фото блюда",
                                 reply_markup=cancel_markup
                                 )
    else:
        await message.answer("Пишите в личку")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = message.message_id
        data["photo"] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Название блюда?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await FSMAdmin.next()
    await message.answer("Описание блюда?")


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
    await FSMAdmin.next()
    await message.answer("Цена блюда?")


async def load_price(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["price"] = int(message.text, base=3)
            await bot.send_photo(message.from_user.id,
                                 data['photo'],
                                 caption=f"Название: {data['name']}\n"
                                         f"Описание: {data['description']}\n"
                                         f"Цена: {data['price']} сом")

        print(data)
        await psql_db.psql_command_insert(state)
        await state.finish()
        await message.answer('Блюдо успешно добавлено в меню!')
    except:
        await message.answer('Цена только в числах!')


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Операция отменена!")


async def delete_data(message: types.Message):
    if message.from_user.id in ADMIN and message.chat.type == "private":
        result = await psql_db.psql_command_all()
        for menu in result:
            await bot.send_photo(
                message.from_user.id,
                photo=menu[1],
                caption=f"Название: {menu[2]}\n"
                        f"Описание: {menu[3]}\n"
                        f"Цена: {menu[4]}\n",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton(
                        f"delete {menu[2]}",
                        callback_data=f"delete {menu[0]}"
                    )
                )
            )
    else:
        await message.answer('Ты не админ!')


async def complete_delete(call: types.CallbackQuery):
    await psql_db.psql_command_delete(call.data.replace("delete ", ""))
    await call.answer(text="Блюдо удалено!", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands=["cancel"])
    dp.register_message_handler(cancel_registration, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(fsm_start, commands=["menu"])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(complete_delete,
                                       lambda call: call.data and
                                                    call.data.startswith('delete '))
