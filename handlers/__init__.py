from aiogram import Router

from .com_handlers import com_handler
from .channel_handlers import channel_handler
from .group_handlers import group_handler
from .main_handlers import main_handler
from .callback_handlers import callback_router

all_handlers = Router()
all_handlers.include_routers(
    com_handler,
    channel_handler,
    group_handler,
    callback_router,
    main_handler,
)

__all__ = [
    'all_handlers',
]
