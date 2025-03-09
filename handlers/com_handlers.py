from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ChatType

from classes import Group, User
from database.requests import unlink_hashtag, unlink_group
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
    user = User(message.from_user.id, bot)
    links = await user.links
    group_id = message.chat.id
    thread_id = message.message_thread_id
    hashtags = command.args.split() if command.args else None
    if hashtags:
        for hashtag in set(links).intersection(hashtags):
            for link in links[hashtag]:
                if link.group.id == group_id and link.group.thread_id == thread_id:
                    await link.unlink_group()
    else:

        for hashtag in hashtags:
            await unlink_hashtag(group_id, thread_id, hashtag)
            await bot.send_message(
                chat_id=message.from_user.id,
                text=
            )
    else:
        await unlink_group(group_id, thread_id)
