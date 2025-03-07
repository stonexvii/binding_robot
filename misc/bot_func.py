from datetime import datetime


def bot_on_start():
    print(f'Bot is started at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}...')


def bot_on_shutdown():
    print(f'Bot is shutdown at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}...')
