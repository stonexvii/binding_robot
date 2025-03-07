from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from .database import engine


class Base(AsyncAttrs, DeclarativeBase):
    pass


class LinkTable(Base):
    __tablename__ = 'link_table'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    hashtag: Mapped[str] = mapped_column(String(100))
    channel_id: Mapped[int] = mapped_column(BigInteger)
    group_id: Mapped[int] = mapped_column(BigInteger)
    thread_id: Mapped[int] = mapped_column(BigInteger)


async def create_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
