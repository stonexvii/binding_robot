from typing import Iterable

from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.enums import MessageEntityType


class EntityFilter(BaseFilter):
    def __init__(self, entity_type: MessageEntityType, values: Iterable[str] | None = None):
        self.type = entity_type
        self.values = set(values) if values else None

    async def __call__(self, message: Message):
        if message.entities:
            entities = [entity for entity in message.entities if entity.type == self.type]
            if entities:
                entities_list = [entity.extract_from(message.text) for entity in entities]
                if self.values is None:
                    return {'entities': entities_list}
                if target_entities_list := set(entities_list).intersection(self.values):
                    return {'entities': target_entities_list}
                return False
            return False
        return False
