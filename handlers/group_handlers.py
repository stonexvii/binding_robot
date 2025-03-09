from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.enums import ChatType, MessageEntityType

from filters import EntityTextFilter, EntityCaptionFilter, ChatTypeFilter
from classes import Link, User

group_handler = Router()


@group_handler.message(
    F.forward_origin,
    EntityTextFilter(MessageEntityType.HASHTAG),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
@group_handler.message(
    F.forward_origin,
    EntityCaptionFilter(MessageEntityType.HASHTAG),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
async def create_new_link(message: Message, entities: list[str], bot: Bot):
    user = User(message.from_user.id, bot)
    for hashtag in entities:
        await user.create_link()
        link = Link.from_message(message, hashtag)
        await link.load_names(bot)
        report = await link.create_link()
        await bot.send_message(
            chat_id=message.from_user.id,
            text=report,
        )
