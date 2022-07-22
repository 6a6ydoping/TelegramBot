from aiogram import Router
from aiogram import Bot
import db.user_db
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.start_kb import get_is_user_already_exists
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import State, StatesGroup

router = Router()


class Form(StatesGroup):
    user_info = State()
    login = State()


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
    await state.set_state(Form.user_info)
    await message.answer(
        'Введите свои данные:',
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Form.user_info)
async def reply_to_user_info(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        'Ваши данные были отправлены менеджеру!',
        reply_markup=ReplyKeyboardRemove()
    )
    # 1684396970
    await bot.send_message(chat_id=1684396970, text=message.text)


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
        'Ваших данных нет в базе данных',
        reply_markup=get_is_user_already_exists()
    )
    await bot.send_message(chat_id=955253586, text=message.text)
    # 955253586
