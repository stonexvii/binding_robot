from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .models import LinkTable


@connection
async def new_link(user_id: int, hashtags: list[str], channel_id, group_id: int, thread_id: int, session: AsyncSession):
    report = []
    for hashtag in hashtags:
        link = await session.scalar(select(LinkTable).where(
            LinkTable.channel_id == channel_id,
            LinkTable.hashtag == hashtag,
            LinkTable.group_id == group_id,
            LinkTable.thread_id == thread_id,
        )
        )
        if not link:
            session.add(
                LinkTable(
                    user_id=user_id,
                    hashtag=hashtag,
                    channel_id=channel_id,
                    group_id=group_id,
                    thread_id=thread_id,
                )
            )
            report.append(hashtag)
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


@connection
async def unlink(group_id: int, thread_id: int, session: AsyncSession, hashtags: list[str] | None = None):
    if hashtags is None:
        query = await session.execute(select(LinkTable).where(
            LinkTable.group_id == group_id,
            LinkTable.thread_id == thread_id,
        ))
        links = query.scalars().all()
        for link in links:
            await session.delete(link)
    else:
        links = []
        for hashtag in hashtags:
            query = await session.execute(select(LinkTable).where(
                LinkTable.group_id == group_id,
                LinkTable.hashtag == hashtag,
                LinkTable.thread_id == thread_id,
            ))
            links.append(query.scalar())
        for link in links:
            await session.delete(link)
    await session.commit()
