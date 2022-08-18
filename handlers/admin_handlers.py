from aiogram import Router
from aiogram import Bot
from db.managers_db import get_manager_tg_names, add_manager
import config
from other_functions.time import get_datetime_now
from config import admin_shortnames, manager_shortnames, analyst_shortnames
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.start_kb import get_is_user_already_exists, check_users_data, main_panel, get_user_classification, \
    get_request_keyboard
from aiogram.dispatcher.fsm.context import FSMContext
from db.all_requests_db import add_request, is_user_in_db, get_status
from db import all_requests_db, managers_db, new_clients_db
from aiogram.dispatcher.fsm.state import State, StatesGroup
from filters.filter import ChatTypeFilter, IsAdmin
from aiogram.types import FSInputFile

router = Router()
router.message.filter(
    IsAdmin()
)


class AdminForm(StatesGroup):
    new_manager = State()
    new_analyst = State()


@router.message(Command(commands=['admin']))
async def cmd_admin(message: Message):
    await message.answer("<b>Список команд админа:</b>"
                         "\nдобавить менеджера - /add_manager"
                         "\nсписок менеджеров - /manager_list"
                         "\nExcel файл с новыми клиентами - /excel_new_clients"
                         "\nExcel файл с существующими клиентами - /excel_clients (НЕ РАБОТАЕТ)"
                         "\nExcel файл с заявками - /excel_requests"
                         "\nExcel файл с работниками - /excel_workers"
                         )


@router.message(Command(commands=['add_manager']))
async def cmd_add_manager(message: Message, state: FSMContext):
    await message.answer("Напишите ник менеджера")
    await state.set_state(AdminForm.new_manager)


@router.message(AdminForm.new_manager)
async def adding_new_manager(message: Message, state: FSMContext):
    config.manager_shortnames.append(message.text)
    add_manager(message.text)
    await message.answer('Менеджер успешно добавлен!')
    await state.clear()


@router.message(Command(commands=['manager_list']))
async def cmd_manager_list(message: Message, state: FSMContext):
    workers = ''
    for i in get_manager_tg_names():
        workers += str(i) + '\n'
    await message.answer(workers)


@router.message(Command(commands=['excel_workers']))
async def cmd_excel_workers(message: Message, bot: Bot):
    managers_db.export_to_excel()
    file = FSInputFile('C:\\Users\\Али\\PycharmProjects\\botv1\\db\\manager_file.csv')
    await bot.send_document(message.chat.id, file)


@router.message(Command(commands=['excel_new_clients']))
async def cmd_excel_new_clients(message: Message, bot: Bot):
    new_clients_db.export_to_excel()
    file = FSInputFile('C:\\Users\\Али\\PycharmProjects\\botv1\\db\\new_clients_file.csv')
    await bot.send_document(message.chat.id, file)


@router.message(Command(commands=['excel_requests']))
async def cmd_excel_clients(message: Message, bot: Bot):
    all_requests_db.export_to_excel()
    file = FSInputFile('C:\\Users\\Али\\PycharmProjects\\botv1\\db\\requests_file.csv')
    await bot.send_document(message.chat.id, file)
