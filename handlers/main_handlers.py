from aiogram import Router
from aiogram.types import Message

main_handler = Router()


@main_handler.message()
async def all_messages(message: Message):
    await message.answer(
        text=f'Перехвачено сообщение:\n{message.text}'
    )
