from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import LinkTable
from database.database import async_session, connection


class Chat:
    def __init__(self, tg_id: int):
        self.id = tg_id
        self.name = None

    async def load_name(self, bot: Bot):
        name = await bot.get_chat(self.id)
        self.name = name.title


class Channel(Chat):
    def __init__(self, channel_id: int):
        super().__init__(channel_id)


class Group(Chat):
    def __init__(self, group_id: int, thread_id: int):
        super().__init__(group_id)
        self.thread_id = thread_id


class Link:
    def __init__(self, user_id: int, hashtag: str, channel_id: int, group_id: int, thread_id: int):
        self.user_id = user_id
        self.hashtag = hashtag
        self.channel = Channel(channel_id)
        self.group = Group(group_id, thread_id or 0)

    @classmethod
    def from_message(cls, message: Message, hashtag: str):
        instance = cls(
            message.from_user.id,
            hashtag,
            message.forward_origin.chat.id,
            message.chat.id,
            message.message_thread_id,
        )
        return instance

    @classmethod
    @connection
    async def user_links(cls, user_id: int, hashtag: str, session: AsyncSession):
        links = await session.scalars(select(LinkTable).where(
            LinkTable.user_id == user_id,
            LinkTable.hashtag == hashtag,
        ))
        return [cls(link.user_id, link.hashtag, link.channel_id, link.group_id, link.thread_id) for link in links.all()]

    @classmethod
    @connection
    async def from_database(cls, hashtag: str, channel_id: int, group_id: int, thread_id: int, session: AsyncSession):
        link = await session.scalar(select(LinkTable).where(
            LinkTable.hashtag == hashtag,
            LinkTable.group_id == group_id,
            LinkTable.channel_id == channel_id,
            LinkTable.thread_id == thread_id,
        ))
        return cls(link.user_id, link.hashtag, link.channel_id, link.group_id, link.thread_id)

    def dict_attrs(self):
        dct = {
            'user_id': self.user_id,
            'hashtag': self.hashtag,
            'channel_id': self.channel.id,
            'group_id': self.group.id,
            'thread_id': self.group.thread_id,
        }
        return dct

    async def load_names(self, bot: Bot):
        await self.channel.load_name(bot)
        await self.group.load_name(bot)

    @connection
    async def create_link(self, session: AsyncSession):
        new_link = await session.scalar(select(LinkTable).where(
            LinkTable.channel_id == self.channel.id,
            LinkTable.hashtag == self.hashtag,
            LinkTable.group_id == self.group.id,
            LinkTable.thread_id == self.group.thread_id,
        ))
        report = f'Данная связь уже зарегистрирована!'
        if not new_link:
            session.add(LinkTable(**self.dict_attrs()))
            report = f'Создана связь:\n{self.channel.name} ▶ {self.group.name}\nПо хештегу {self.hashtag}'
        await session.commit()
        return report

    def for_button(self):
        return f'{self.channel.name} ▶ {self.group.name} ({self.group.thread_id})'

    def for_unlink(self):
        return f'Связь:\n{self.channel.name} ▶ {self.group.name} ({self.group.thread_id})\nУдалена!'
