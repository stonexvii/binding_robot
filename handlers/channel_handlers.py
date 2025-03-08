from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.enums import MessageEntityType

from database.requests import get_channel_hashtags
from filters import EntityTextFilter, EntityCaptionFilter

channel_handler = Router()


@channel_handler.channel_post(EntityCaptionFilter(MessageEntityType.HASHTAG))
@channel_handler.channel_post(EntityTextFilter(MessageEntityType.HASHTAG))
async def channel_post_hashtag(message: Message, entities: list[str], bot: Bot):
    print('CATCH')
    links = await get_channel_hashtags(message.chat.id)
    for link in links:
        if link.hashtag in entities:
            await bot.forward_message(
                chat_id=link.group_id,
                message_thread_id=link.thread_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )


