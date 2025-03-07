from aiogram.filters.callback_data import CallbackData


class HashtagData(CallbackData, prefix='HD'):
    button: str
    hashtag: str
    channel_id: int = 0
    group_id: int = 0
    thread_id: int = 0
