from typing import Iterable

from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.enums import ChatType


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_types: Iterable[ChatType] | ChatType):
        self.types = set(chat_types) if isinstance(chat_types, Iterable) else {chat_types}

    async def __call__(self, message: Message):
        return message.chat.type in self.types
