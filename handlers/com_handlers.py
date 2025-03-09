from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ChatType

from classes import Link, User
from database.requests import get_group_links
from filters import ChatTypeFilter
from keyboards import ikb_select_hashtag

com_handler = Router()



@com_handler.message(Command('start'))
async def com_start(message: Message, bot: Bot):
    user = User(message.from_user.id, bot)
    user_hashtags = await user.hashtags
    await message.answer(
        text=f'Приветствую тебя, {message.from_user.full_name}!\nВыбери хештег для управления!',
        reply_markup=ikb_select_hashtag(user_hashtags)
    )


@com_handler.message(Command('unlink'), ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
async def com_unlink(message: Message, command: CommandObject, bot: Bot):
    user_id = message.from_user.id
    group_id = message.chat.id
    thread_id = message.message_thread_id
    hashtags = command.args.split() if command.args else None
    response = await get_group_links(user_id, group_id, thread_id)
    if response:
        links = [Link(entry.hashtag, entry.channel_id, entry.group_id, entry.thread_id) for entry in response]
        for link in links:
            await link.load_names(bot)
            if hashtags and link.hashtag in hashtags:
                await link.unlink()
                await bot.send_message(
                    chat_id=user_id,
                    text=link.unlink_text,
                )
            else:
                await link.unlink()
                await bot.send_message(
                    chat_id=user_id,
                    text=link.unlink_text,
                )

