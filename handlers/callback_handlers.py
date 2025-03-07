from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.callback_data import HashtagData
from database.requests import get_links_by_hashtag

callback_router = Router()


@callback_router.callback_query(HashtagData.filter(F.button == 'select_hashtag'))
async def target_hashtag(callback: CallbackQuery, callback_data: HashtagData):
    links = await get_links_by_hashtag(callback_data.hashtag)
    chat_id = links[0].group_id
    channel_name = await callback.bot.get_chat(chat_id=chat_id,)
    print(channel_name.full_name)
    await callback.answer(
        text=callback_data.hashtag,
        show_alert=True,
    )
