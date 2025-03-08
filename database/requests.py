from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from classes import Link
from .database import connection
from .models import LinkTable


@connection
async def create_link(link: Link, session: AsyncSession):
    new_link = await session.scalar(select(LinkTable).where(
        LinkTable.channel_id == link.channel.id,
        LinkTable.hashtag == link.hashtag,
        LinkTable.group_id == link.group.id,
        LinkTable.thread_id == link.group.thread_id,
    ))
    report = f'Данная связь уже зарегистрирована!'
    if not new_link:
        session.add(LinkTable(**link.dict_attrs()))
        report = f'Создана связь:\n{link.channel.name} {link.group.name}\nПо хештегу {link.hashtag}'
    await session.commit()
    return report


@connection
async def get_user(user_id: int, session: AsyncSession):
    result = await session.scalars(select(LinkTable).where(LinkTable.user_id == user_id))
    return result


@connection
async def get_channel_hashtags(channel_id: int, session: AsyncSession):
    result = await session.scalars(select(LinkTable).where(LinkTable.channel_id == channel_id))
    return result.all()


@connection
async def get_links_by_hashtag(hashtag: str, session: AsyncSession):
    result = await session.scalars(select(LinkTable).where(LinkTable.hashtag == hashtag))
    return result.all()


# @connection
# async def unlink(group_id: int, thread_id: int, session: AsyncSession, hashtags: list[str] | None = None):
#     if hashtags is None:
#         query = await session.execute(select(LinkTable).where(
#             LinkTable.group_id == group_id,
#             LinkTable.thread_id == thread_id,
#         ))
#         links = query.scalars().all()
#         for link in links:
#             await session.delete(link)
#     else:
#         links = []
#         for hashtag in hashtags:
#             query = await session.execute(select(LinkTable).where(
#                 LinkTable.group_id == group_id,
#                 LinkTable.hashtag == hashtag,
#                 LinkTable.thread_id == thread_id,
#             ))
#             links.append(query.scalar())
#         for link in links:
#             await session.delete(link)
#     await session.commit()

@connection
async def unlink_group(group_id: int, thread_id: int, session: AsyncSession):
    query = await session.execute(select(LinkTable).where(
        LinkTable.group_id == group_id,
        LinkTable.thread_id == thread_id,
    ))
    links = query.scalars().all()
    for link in links:
        await session.delete(link)
    await session.commit()


@connection
async def unlink_hashtag(group_id: int, thread_id: int, hashtag: str, session: AsyncSession):
    query = await session.execute(select(LinkTable).where(
        LinkTable.group_id == group_id,
        LinkTable.hashtag == hashtag,
        LinkTable.thread_id == thread_id,
    ))
    link = query.scalar()
    await session.delete(link)
    await session.commit()
