from aiogram import Router
from aiogram import Bot
from other_functions.time import get_datetime_now
from config import manager_id
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.start_kb import get_is_user_already_exists, check_users_data, main_panel
from aiogram.dispatcher.fsm.context import FSMContext
from db.user_db import add_user, is_user_in_db, get_status
from aiogram.dispatcher.fsm.state import State, StatesGroup

router = Router()


class Form(StatesGroup):
    user_info = State()
    user_name = State()
    user_phone = State()
    user_email = State()
    login = State()
    signed_in = State()


user_array = []
old_user_info = []


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    print(message.chat.id)
    old_user_info, user_array = [], []
    await state.set_state(None)
    await message.answer(
        'Выберите вариант',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Новый пользователь', ignore_case=True))
async def new_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_name)
    await message.answer(
        'Введите ваше ФИО',
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
async def get_user_email(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(user_email=message.text)
    user_array.append(message.text)
    await message.answer(
        f"Нажмите <b><i>да</i></b> если данные верны\n ФИО: <b>{user_array[0]}</b> \n Номер: <b>{user_array[1]}</b> \n Почта: <b>{user_array[2]}</b>",
        reply_markup=check_users_data()
    )
    await state.set_state(None)


@router.message(Text(text="Да"))
async def user_created_successfully(message: Message, state: FSMContext, bot: Bot) -> None:
    if user_array:
        await message.answer(
            'Ваши данные были занесены в базу данных и отправлены менеджеру!',
        )
        user_array.append(message.text)
        await bot.send_message(chat_id=manager_id, text=message.text)
        add_user(user_array)
        await state.set_state(Form.signed_in)
        await message.answer(
            f'Добро пожаловать {user_array[0]}!',
            reply_markup=main_panel()
        )
        user_array.clear()


@router.message(Text(text='Вернуться назад'))
async def go_back(message: Message, state: FSMContext, bot: Bot) -> None:
    user_array.clear()
    await state.clear()
    await message.answer(
        'Выберите вариант',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Существующий пользователь', ignore_case=True))
async def existing_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.login)
    await message.answer(
        'Введите имя для авторизации информации',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Form.login)
async def get_login(message: Message, state: FSMContext) -> None:
    old_user_info.append(message.text)
    if is_user_in_db(message.text):
        await state.set_state(Form.signed_in)
        await message.answer(f'Добро пожаловать, {message.text}!', reply_markup=main_panel())
    else:
        await message.answer(
            'Такого пользователя нет в базе данных.',
            reply_markup=get_is_user_already_exists()
        )
        old_user_info.clear()


@router.message(Text(text="Связаться с тех поддержкой"), Form.signed_in)
async def signed_in(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(
        f"{old_user_info[0]}, ваша заявка была передана тех поддержке, чтобы вам ответили не меняйте ник до того как "
        f"с вами свяжется менеджер.")
    await bot.send_message(manager_id,
                           f"В {get_datetime_now()} пришла заявка для тех поддержки от пользователя @{message.from_user.username}")


@router.message(Text(text="Статус отчета"), Form.signed_in)
async def status_of_report(message: Message, state: FSMContext, bot: Bot) -> None:
    status = get_status()
    await message.answer()
