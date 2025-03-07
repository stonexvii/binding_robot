from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ChatType

from database.requests import get_user, unlink
from filters import ChatTypeFilter
from keyboards import ikb_start_keyboard

com_handler = Router()


@com_handler.message(Command('start'))
async def com_start(message: Message):
    data = await get_user(message.from_user.id)
    hashtags = {item.hashtag for item in data.all()}
    await message.answer(
        text=f'Приветствую тебя, {message.from_user.full_name}!\nВыбери хештег для управления!',
        reply_markup=ikb_start_keyboard(hashtags)
    )


@com_handler.message(Command('unlink'), ChatTypeFilter([ChatType.GROUP, ChatType.SUPERGROUP]))
async def com_unlink(message: Message, command: CommandObject):
    group_id = message.chat.id
    thread_id = message.message_thread_id
    hashtags = command.args.split() if command.args else None
    await unlink(group_id, thread_id, hashtags=hashtags)
    await message.answer(
        text='Бот работает!'
    )
