from aiogram import Router
from aiogram import Bot
from aiogram import types
import db.user_db
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.start_kb import get_is_user_already_exists, inline_yes_or_no
from aiogram.dispatcher.fsm.context import FSMContext
from db.user_db import add_user
from aiogram.dispatcher.fsm.state import State, StatesGroup

router = Router()


class Form(StatesGroup):
    user_info = State()
    user_name = State()
    user_phone = State()
    user_email = State()
    login = State()


user_array = []


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    print(message.chat.id)
    await state.set_state(None)
    await message.answer(
        'Выберите вариант:',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Новый пользователь', ignore_case=True))
async def new_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_name)
    await message.answer(
        'Введите ваше ФИО:',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Form.user_name)
async def get_user_name(message: Message, state: FSMContext) -> None:
    await state.update_data(user_name=message.text)
    user_array.append(message.text)
    await message.answer('Введите ваш номер телефона')
    await state.set_state(Form.user_phone)
    print(user_array)


@router.message(Form.user_phone)
async def get_user_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(user_phone=message.text)
    user_array.append(message.text)
    await message.answer('Введите вашу электронную почту')
    await state.set_state(Form.user_email)


@router.message(Form.user_email)
async def reply_to_user_info(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        'Ваши данные были занесены в базу данных и отправлены менеджеру!',
        reply_markup=ReplyKeyboardRemove()
    )
    user_array.append(message.text)
    # 1684396970
    await bot.send_message(chat_id=1684396970, text=message.text)
    await state.clear()
    add_user(user_array)


# @router.message(Form.user_email)
# async def get_user_email(message: Message, state: FSMContext, bot: Bot) -> None:
#     await state.update_data(user_email=message.text)
#     user_array.append(message.text)
#     await message.answer(
#         f"Нажмите <b><i>да</i></b> если данные верны\n ФИО: <b>{user_array[0]}</b> \n Номер: <b>{user_array[1]}</b> \n Почта: <b>{user_array[2]}</b>",
#         reply_markup=inline_yes_or_no()
#     )
#     await state.set_state(None)


@router.message(Text(text='Существующий пользователь', ignore_case=True))
async def existing_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.login)
    await message.answer(
        'Введите логин для получения информации',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Form.login)
async def get_login(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(
        f'Привет, ',
        # reply_markup=get_is_user_already_exists()
    )
    await bot.send_message(chat_id=955253586, text=message.text)
    # 955253586
