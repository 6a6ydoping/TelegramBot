import aiogram.types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import types


def get_is_user_already_exists() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Новый пользователь")
    kb.button(text="Существующий пользователь")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def inline_yes_or_no():
    pass
