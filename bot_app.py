import asyncio
import os

from aiogram import Bot, Dispatcher

from database import create_tables
from handlers import all_handlers
from misc import *


async def start_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp = Dispatcher()
    print('DataBase is', end=' ')
    try:
        await create_tables()
        print('OK!!!')
    except:
        print('Failed :(')
    dp.startup.register(bot_on_start)
    dp.shutdown.register(bot_on_shutdown)
    dp.include_router(all_handlers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
