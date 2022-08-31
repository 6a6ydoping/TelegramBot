import aiogram.types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



def get_inline_is_done(request) -> InlineKeyboardMarkup:
    buttons = [
        [aiogram.types.InlineKeyboardButton(text="Выполнена✅", callback_data=f"done{request}")]
    ]
    keyboard = aiogram.types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
