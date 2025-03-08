from aiogram.filters.callback_data import CallbackData


class HashtagData(CallbackData, prefix='HD'):
    hashtag: str


class LinkData(CallbackData, prefix='LD'):
    hashtag: str
    channel_id: int
    group_id: int
    thread_id: int
