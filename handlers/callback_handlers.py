from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from classes import Link
from keyboards import ikb_select_link
from keyboards.callback_data import HashtagData, LinkData
from database.requests import unlink_hashtag

callback_router = Router()


@callback_router.callback_query(HashtagData)
async def target_hashtag(callback: CallbackQuery, callback_data: HashtagData, bot: Bot):
    links = await Link.user_links(callback.from_user.id, callback_data.hashtag)
    for link in links:
        await link.load_names(bot)
    await bot.edit_message_text(
        text=f'По хештегу {callback_data.hashtag} зарегистрированы связи:',
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_select_link(links),
    )


@callback_router.callback_query(LinkData)
async def target_link(callback: CallbackQuery, callback_data: HashtagData, bot: Bot):
    link = await Link.from_database(
        callback_data.hashtag,
        callback_data.channel_id,
        callback_data.group_id,
        callback_data.thread_id
    )
    await link.load_names(bot)
    await unlink_hashtag(callback_data.group_id, callback_data.thread_id, callback_data.hashtag)
    await callback.answer(
        text=link.for_unlink(),
        show_alert=True,
    )
