from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import HashtagData, LinkData
from classes import HashTag, Link


def ikb_select_hashtag(user_hashtags: list[HashTag]):
    keyboard = InlineKeyboardBuilder()
    for hashtag in user_hashtags:
        keyboard.button(
            text=hashtag.hashtag,
            callback_data=HashtagData(
                hashtag=hashtag.hashtag,
            ),
        )
    return keyboard.as_markup()


def ikb_select_link(link_list: list[Link]):
    keyboard = InlineKeyboardBuilder()
    for link in link_list:
        keyboard.button(
            text=link.button_text,
            callback_data=LinkData(
                hashtag=link.hashtag,
                channel_id=link.channel.id,
                group_id=link.group.id,
                thread_id=link.group.thread_id,
            ),
        )
    keyboard.button(
        text='Назад',
        callback_data=HashtagData(
            hashtag='back_button',
        ),
    )
    keyboard.adjust(*[1] * len(link_list), 1)
    return keyboard.as_markup()
