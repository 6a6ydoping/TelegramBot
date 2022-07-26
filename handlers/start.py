from aiogram import Router
from aiogram import Bot
from other_functions.time import get_datetime_now
from config import manager_id
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.start_kb import get_is_user_already_exists, check_users_data, main_panel, get_user_classification
from aiogram.dispatcher.fsm.context import FSMContext
from db.user_db import add_user, is_user_in_db, get_status
from aiogram.dispatcher.fsm.state import State, StatesGroup

router = Router()


class Form(StatesGroup):
    user_info = State()
    user_name = State()
    user_phone = State()
    user_email = State()
    user_classification = State()
    login = State()
    signed_in = State()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    print(message.chat.id)
    await state.set_state(None)
    await message.answer(
        'Авторизуйтесь или создайте новую учетную запись',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Зарегистрироваться', ignore_case=True))
async def new_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_name)
    await message.answer(
        'Выберите вариант',
        reply_markup= get_user_classification(),
    )


@router.message(Form.user_name)
async def get_user_name(message: Message, state: FSMContext) -> None:
    await state.update_data(user_name=message.text)
    await message.answer('Введите ваш номер телефона')
    await state.set_state(Form.user_phone)


@router.message(Form.user_phone)
async def get_user_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(user_phone=message.text)
    await message.answer('Введите вашу электронную почту')
    await state.set_state(Form.user_email)


@router.message(Form.user_email)
async def get_user_email(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.update_data(user_email=message.text)
    data = await state.get_data()
    await message.answer(
        f"Нажмите <b><i>да</i></b> если данные верны\n ФИО: <b>{data['user_name']}</b> \n Номер: <b>{data['user_phone']}</b> \n Почта: <b>{data['user_email']}</b>",
        reply_markup=check_users_data()
    )
    await state.set_state(None)


@router.message(Text(text="Да"))
async def user_created_successfully(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    if data:
        await message.answer(
            'Ваши данные были занесены в базу данных и отправлены менеджеру!',
        )
        await bot.send_message(chat_id=manager_id, text=message.text)
        add_user([data['user_name'], data['user_phone'], data['user_email']])
        await state.set_state(Form.signed_in)
        await message.answer(
            f'Добро пожаловать {data["user_name"]}!',
            reply_markup=main_panel()
        )



@router.message(Text(text='Вернуться назад'))
async def go_back(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await message.answer(
        'Выберите вариант',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Авторизоваться', ignore_case=True))
async def existing_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.login)
    await message.answer(
        'Введите имя для авторизации информации',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Form.login)
async def get_login(message: Message, state: FSMContext) -> None:
    if is_user_in_db(message.text):
        data = await state.update_data(user_name=message.text)
        await state.set_state(Form.signed_in)
        await message.answer(f'Добро пожаловать, {data["user_name"]}!', reply_markup=main_panel())
    else:
        await message.answer(
            'Такого пользователя нет в базе данных.',
            reply_markup=get_is_user_already_exists()
        )


@router.message(Text(text="Связаться с тех поддержкой"), Form.signed_in)
async def signed_in(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    user_name = data["user_name"]
    await message.answer(
        f"{user_name}, ваша заявка была передана тех поддержке, чтобы вам ответили не меняйте ник до того как "
        f"с вами свяжется менеджер.")
    await bot.send_message(manager_id,
                           f"В {get_datetime_now()} пришла заявка для тех поддержки от пользователя @{message.from_user.username}")


@router.message(Text(text="Статус отчета"), Form.signed_in)
async def status_of_report(message: Message, state: FSMContext, bot: Bot) -> None:
    status = get_status()
    await message.answer()
