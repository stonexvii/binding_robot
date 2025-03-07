from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.enums import ChatType, MessageEntityType

from filters import EntityFilter, ChatTypeFilter
from classes import Link

group_handler = Router()


@group_handler.message(
    F.forward_origin,
    EntityFilter(MessageEntityType.HASHTAG),
    ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
async def forward_group_message(message: Message, entities: list[str], bot: Bot):
    user_id = message.from_user.id
    hashtags = entities
    channel_id = message.forward_origin.chat.id
    group_id = message.chat.id
    message_thread_id = message.message_thread_id
    link = Link(user_id, hashtags, channel_id, group_id, message_thread_id)
    reports = await link.create_link()
    for report in reports:
        await bot.send_message(
            chat_id=user_id,
            text=f'Link c {report} добавлен!',
        )
