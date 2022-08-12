import aiogram.types.keyboard_button
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, \
    KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import types


def get_is_user_already_exists() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Я новый клиент")
    kb.button(text="Я существующий клиент")
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
    kb.button(text="Новый запрос")
    kb.button(text="Связаться с тех поддержкой")
    return kb.as_markup(resize_keyboard=True)


def get_user_classification():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Юридическое лицо")
    kb.button(text="Физическое лицо")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def get_request_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Новый отчет")
    kb.button(text="Связаться с бухгалтерией")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)