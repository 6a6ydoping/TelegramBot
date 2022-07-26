import aiogram.types.keyboard_button
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import types


def get_is_user_already_exists() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Зарегистрироваться")
    kb.button(text="Авторизоваться")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def check_users_data():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Вернуться назад")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def main_panel():
    kb = ReplyKeyboardBuilder()
    kb.row(
        KeyboardButton(text="Статус отчета"),
        KeyboardButton(text="Новый отчет")
    )
    kb.row(KeyboardButton(text="Связаться с тех поддержкой"))
    return kb.as_markup(resize_keyboard=True)


def get_user_classification():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Юридическое лицо")
    kb.button(text="Физическое лицо")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)