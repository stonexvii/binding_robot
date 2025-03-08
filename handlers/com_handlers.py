from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ChatType

from database.requests import get_user, unlink_hashtag, unlink_group
from filters import ChatTypeFilter
from keyboards import ikb_select_hashtag

com_handler = Router()


@com_handler.message(Command('start'))
async def com_start(message: Message):
    data = await get_user(message.from_user.id)
    hashtags = {item.hashtag for item in data.all()}
    await message.answer(
        text=f'Приветствую тебя, {message.from_user.full_name}!\nВыбери хештег для управления!',
        reply_markup=ikb_select_hashtag(hashtags)
    )


@com_handler.message(Command('unlink'), ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
async def com_unlink(message: Message, command: CommandObject):
    group_id = message.chat.id
    thread_id = message.message_thread_id
    hashtags = command.args.split() if command.args else None
    if hashtags:
        for hashtag in hashtags:
            await unlink_hashtag(group_id, thread_id, hashtag)
    else:
        await unlink_group(group_id, thread_id)
    await message.answer(
        text='Бот работает!'
    )

