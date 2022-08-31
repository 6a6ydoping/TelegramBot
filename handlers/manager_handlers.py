from aiogram import Router
from aiogram import Bot
from filters.filter import IsManager
from other_functions.time import get_datetime_now, is_working_time
from config import manager_id, admin_shortnames, manager_shortnames, analyst_shortnames, accountant_id
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, Message
from keyboards.user_kb import get_is_user_already_exists, check_users_data, main_panel, get_user_classification, \
    get_request_keyboard
from aiogram.dispatcher.fsm.context import FSMContext
from db.all_requests_db import add_request, is_user_in_db, get_status, export_to_excel
from db.new_clients_db import add_new_user
from aiogram.dispatcher.fsm.state import State, StatesGroup
from filters.filter import ChatTypeFilter
from aiogram.types import FSInputFile

router = Router()
router.message.filter(
    IsManager()
)

# @router.message()