from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.enums import ChatType, MessageEntityType

from filters import EntityTextFilter, ChatTypeFilter
from classes import Link

group_handler = Router()


@group_handler.message(
    F.forward_origin,
    EntityTextFilter(MessageEntityType.HASHTAG),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
async def forward_group_message(message: Message, entities: list[str], bot: Bot):
    for hashtag in entities:
        link = Link.from_message(message, hashtag)
        await link.load_names(bot)
        report = await link.create_link()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=report,
        )
