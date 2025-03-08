from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import HashtagData, LinkData
from classes import Link


def ikb_select_hashtag(button_list: set[str]):
    keyboard = InlineKeyboardBuilder()
    for button in button_list:
        keyboard.button(
            text=button,
            callback_data=HashtagData(
                hashtag=button,
            ),
        )
    return keyboard.as_markup()


def ikb_select_link(link_list: list[Link]):
    keyboard = InlineKeyboardBuilder()
    for link in link_list:
        keyboard.button(
            text=link.for_button(),
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
