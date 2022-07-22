from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_is_user_already_exists() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Новый пользователь")
    kb.button(text="Существующий пользователь")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
