from aiogram import Router
from aiogram import Bot
from other_functions.time import get_datetime_now
from config import manager_id, admin_shortnames, manager_shortnames, analyst_shortnames, accountant_id
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.start_kb import get_is_user_already_exists, check_users_data, main_panel, get_user_classification, \
    get_request_keyboard
from aiogram.dispatcher.fsm.context import FSMContext
from db.all_requests_db import add_request, is_user_in_db, get_status, export_to_excel
from db.new_clients_db import add_new_user
from aiogram.dispatcher.fsm.state import State, StatesGroup
from filters.filter import ChatTypeFilter
from aiogram.types import FSInputFile

router = Router()
router.message.filter(
    ChatTypeFilter(chat_type=["group", "supergroup"])
)


class Form(StatesGroup):
    user_info = State()
    user_name = State()
    user_phone = State()
    user_email = State()
    user_classification = State()
    user_company = State()
    get_phone = State()
    get_login = State()
    new_user = State()
    creating_new_user = State()
    signed_in = State()
    user_accountant_req = State()


@router.message(Command(commands=['start']))
async def cmd_start(message: Message, state: FSMContext):
    print(message.chat.id)
    await state.set_state(None)
    await message.answer(
        'Добрый день! Вы уже являетесь нашим клиентом?',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Я новый клиент', ignore_case=True))
async def new_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.user_classification)
    await message.answer(
        'Выберите вариант',
        reply_markup=get_user_classification(),
    )


# Юридическое или Физическое лицо
@router.message(Form.user_classification)
async def set_user_classification(message: Message, state: FSMContext) -> None:
    if message.text == 'Физическое лицо':
        await state.update_data(user_classification='Физическое лицо')
        await state.set_state(Form.user_name)
        await message.answer(
            'Напишите свое ФИО',
            reply_markup=ReplyKeyboardRemove()
        )
    elif message.text == 'Юридическое лицо':
        await state.update_data(user_classification='Юридическое лицо')
        await state.set_state(Form.user_company)
        await message.answer(
            'Напишите название вашей компании',
            reply_markup=ReplyKeyboardRemove()
        )


# Узнать компанию Юридического лица
@router.message(Form.user_company)
async def get_user_company(message: Message, state: FSMContext) -> None:
    await state.update_data(user_company=message.text)
    await state.set_state(Form.user_name)
    await message.answer(
        'Напишите свое ФИО',
    )


@router.message(Form.user_name)
async def get_user_name(message: Message, state: FSMContext) -> None:
    await state.update_data(user_name=message.text)
    await message.answer('Введите номер телефона, привязанный к вашему телеграму', reply_markup=ReplyKeyboardRemove)
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
    if data['user_classification'] == 'Физическое лицо':
        await message.answer(
            f"Нажмите <b><i>да</i></b> если данные верны"
            f"\n ФИО: <b>{data['user_name']}</b> "
            f"\n Номер: <b>{data['user_phone']}</b> "
            f"\n Почта: <b>{data['user_email']}</b>",
            reply_markup=check_users_data()
        )
        await state.set_state(Form.new_user)
    elif data['user_classification'] == 'Юридическое лицо':
        await message.answer(
            f"Нажмите <b><i>да</i></b> если данные верны"
            f"\n Название компании: <b>{data['user_company']}</b>"
            f"\n ФИО: <b>{data['user_name']}</b> "
            f"\n Номер: <b>{data['user_phone']}</b> "
            f"\n Почта: <b>{data['user_email']}</b>",
            reply_markup=check_users_data()
        )
        await state.set_state(Form.new_user)


@router.message(Text(text='Да'), Form.new_user)
async def new_user(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    await message.answer(
        'Ваши данные отправлены менеджеру, с вами свяжутся в течении двух часов!',
        reply_markup=ReplyKeyboardRemove()
    )
    if data['user_classification'] == 'Юридическое лицо':
        await bot.send_message(chat_id=manager_id, text=(f"Запрос на создание нового пользователя:"
                                                         f"\n Классификация: <b>Юридическое лицо</b>"
                                                         f"\n Название компании: <b>{data['user_company']}</b>"
                                                         f"\n ФИО: <b>{data['user_name']}</b> "
                                                         f"\n Номер: <b>{data['user_phone']}</b> "
                                                         f"\n Почта: <b>{data['user_email']}</b>"
                                                         f"\n Время: <b>{get_datetime_now()[0]}  {get_datetime_now()[1]}</b>"
                                                         ))
        add_new_user(
            [get_datetime_now()[0], data['user_name'], data['user_phone'], data['user_email'], data['user_company']]
        )
    elif data['user_classification'] == 'Физическое лицо':
        await bot.send_message(chat_id=manager_id, text=(f"Запрос на создание нового пользователя:"
                                                         f"\n Классификация: <b>Физическое лицо</b>"
                                                         f"\n ФИО: <b>{data['user_name']}</b> "
                                                         f"\n Номер: <b>{data['user_phone']}</b> "
                                                         f"\n Почта: <b>{data['user_email']}</b>"
                                                         f"\n Время: <b>{get_datetime_now()[0]}  {get_datetime_now()[1]}</b>"
                                                         ))
        add_new_user([get_datetime_now()[0], data['user_name'], data['user_phone'], data['user_email'], 'None'])
    await state.set_state(Form.creating_new_user)


# Пользователь проверяет введенные данные, если все верно, после сообщения "Да" данные сохраняются
# @router.message(Form.creating_new_user)
# async def user_created_successfully(message: Message, state: FSMContext, bot: Bot) -> None:
#     print('OK')
#     data = await state.get_data()
#     if data:
#         if data['user_classification'] == 'Физическое лицо':
#             add_new_user([get_datetime_now(), data['user_name'], data['user_phone'], data['user_email'], 'None'])
#         elif data['user_classification'] == 'Юридическое лицо':
#             print(get_datetime_now(), data['user_name'], data['user_phone'], data['user_email'], data['user_company'])
#             add_new_user(
#                 [get_datetime_now(), data['user_name'], data['user_phone'], data['user_email'], data['user_company']]
#             )
#         await message.answer(
#             'Ваши данные были занесены в базу данных и отправлены менеджеру!',
#         )
#         await bot.send_message(chat_id=manager_id, text=message.text)
#         # add_user([data['user_name'], data['user_phone'], data['user_email']])
#         await state.clear()
#         # await state.set_state(Form.signed_in)
#         # await message.answer(
#         #     f'Добро пожаловать {data["user_name"]}!',
#         #     reply_markup=main_panel()
#         # )


@router.message(Text(text='Вернуться назад'))
async def go_back(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await message.answer(
        'Выберите вариант',
        reply_markup=get_is_user_already_exists()
    )


@router.message(Text(text='Я существующий клиент', ignore_case=True))
async def existing_user(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.get_login)
    await message.answer(
        'Введите ваш логин',
        #'Введите номер телефона привязанный к вашему <b>телеграму</b> для создания запроса',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Form.get_login)
async def get_login(message: Message, state: FSMContext) -> None:
    data = await state.update_data(user_login=message.text)
    await message.answer(f'Введите номер телефона привязанный к вашему телеграму')
    await state.set_state(Form.get_phone)


@router.message(Form.get_phone)
async def get_login(message: Message, state: FSMContext) -> None:
    data = await state.update_data(user_phone=message.text)
    await state.set_state(Form.signed_in)
    await message.answer('Добро пожаловать!', reply_markup=main_panel())


@router.message(Text(text="Связаться с тех поддержкой"), Form.signed_in)
async def signed_in(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    user_phone = data["user_phone"]
    user_login = data["user_login"]
    await message.answer(
        f"Ваша заявка была передана тех поддержке, чтобы вам ответили не меняйте ник до того как "
        f"с вами свяжется менеджер.")
    await bot.send_message(manager_id,
                           f"В {get_datetime_now()[0]}  {get_datetime_now()[1]} пришла заявка для тех поддержки\nЛогин:{user_login}\nНомер телефона:{user_phone} ")
    add_request([data['user_login'], data['user_phone'], 'tech_support', 'Ali', get_datetime_now()[0], get_datetime_now()[1]])


@router.message(Text(text="Новый запрос"), Form.signed_in)
async def status_of_report(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.answer(
        'Вы можете сделать запрос на <b>новый отчет</b> и запрос в <b>бухгалтерию</b>',
        reply_markup=get_request_keyboard()
    )


@router.message(Text(text="Связаться с бухгалтерией"), Form.signed_in)
async def get_accountant_request(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    user_phone = data['user_phone']
    await message.answer(
        'Ваша заявка была передана в бухгалтерию, с вами свяжутся в течении двух часов!',
        reply_markup=main_panel()
    )
    await bot.send_message(accountant_id,
                           f"В {get_datetime_now()[0]}  {get_datetime_now()[1]} пришла заявка в бухгалтерию по номеру телефона {user_phone}")
    add_request(
        [data['user_login'], data['user_phone'], 'accountant', 'Buhgalter Name', get_datetime_now()[0], get_datetime_now()[1]])


@router.message(Text(text="Новый отчет"), Form.signed_in)
async def new_report(message: Message, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    user_phone = data['user_phone']
    await message.answer(
        f"Ваш запрос был передан менеджеру, с вами свяжутся в течении двух часов!",
        reply_markup=main_panel()
    )
    await bot.send_message(manager_id,
                           f"В {get_datetime_now()[0]}  {get_datetime_now()[1]} \nЗапрос на новый отчет по номеру телефона {user_phone}")
    add_request(
        [data['user_login'], data['user_phone'], 'new request', 'Manager_Name', get_datetime_now()[0],
         get_datetime_now()[1]])


# @router.message(Form.user_accountant_req)
# async def accountant_request(message: Message, state: FSMContext, bot: Bot) -> None:
#     await state.update_data(user_accountant_req=message.text)
#     request_text = message.text + '\n\n Запрос в бухгалтерию от @' + message.from_user.id + ' в ' + str(
#         get_datetime_now())
#     await bot.send_message(manager_id, request_text)
#     await message.answer(
#         'Ваш запрос был передан в бухгалтерию! Вам ответят в течении суток, не меняйте ник чтобы менеджер мог связаться с вами',
#         reply_markup=main_panel()
#     )
#     await state.set_state(Form.signed_in)

# @router.message(Form.user_accountant_req)
# async def accountant_request(message: Message, state: FSMContext, bot: Bot) -> None:
#     await message.answer(
#         'Напишите ваш запрос по этому адресу: ' + manager_nick,
#         reply_markup= main_panel()
#     )
#     await state.set_state(signed_in)

@router.message(Command(commands=['csv']))
async def csv_text(message: Message, bot: Bot):
    if message.from_user.username in admin_shortnames:
        export_to_excel()
        file = FSInputFile('C:\\Users\\Али\\PycharmProjects\\botv1\\db\\some_file.csv')
        await bot.send_document(message.chat.id, file)