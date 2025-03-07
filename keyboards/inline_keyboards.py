from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import HashtagData
from database.models import LinkTable


def ikb_start_keyboard(button_list: set[str]):
    keyboard = InlineKeyboardBuilder()
    for button in button_list:
        keyboard.button(
            text=button,
            callback_data=HashtagData(
                button='select_hashtag',
                hashtag=button,
            ),
        )
    return keyboard.as_markup()


def ikb_select_link(link_list: list[LinkTable]):
    keyboard = InlineKeyboardBuilder()
    for link in link_list:

        keyboard.button(
            text=button,
            callback_data=HashtagData(
                button='select_hashtag',
                hashtag=button,
            ),
        )
    return keyboard.as_markup()