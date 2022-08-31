from typing import Union
from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from config import admin_shortnames, manager_shortnames


class ChatTypeFilter(BaseFilter):
    chat_type: Union[str, list]

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type != self.chat_type
        else:
            return message.chat.type not in self.chat_type


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.username in admin_shortnames:
            print('Its an Admin')
            return True
        print('It is not an Admin')
        return False


class IsManager(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.username in manager_shortnames:
            print('Its manager')
            return True
        return False
