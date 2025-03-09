from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .database import connection
from .models import LinkTable


@connection
async def new_link(user_id: int, hashtag: int, channel_id: int, group_id: int, thread_id: int, session: AsyncSession):
    link = await session.scalar(select(LinkTable).where(
        LinkTable.hashtag == hashtag,
        LinkTable.channel_id == channel_id,
        LinkTable.group_id == group_id,
        LinkTable.thread_id == thread_id,
    ))
    if not link:
        session.add(LinkTable(
            user_id=user_id,
            hashtag=hashtag,
            channel_id=channel_id,
            group_id=group_id,
            thread_id=thread_id,
        ))
        await session.commit()
        return True


@connection
async def get_user(user_id: int, session: AsyncSession):
    response = await session.scalars(select(LinkTable).where(LinkTable.user_id == user_id))
    return response.all()


@connection
async def get_hashtag(user_id: int, hashtag: str, session: AsyncSession):
    response = await session.scalars(select(LinkTable).where(
        LinkTable.user_id == user_id,
        LinkTable.hashtag == hashtag,
    ))
    return response.all()


@connection
async def get_channel_hashtags(channel_id: int, session: AsyncSession):
    response = await session.scalars(select(LinkTable).where(LinkTable.channel_id == channel_id))
    return response.all()


@connection
async def get_group_links(user_id: int, group_id: int, thread_id: int, session: AsyncSession):
    response = await session.scalars(select(LinkTable).where(
        LinkTable.user_id == user_id,
        LinkTable.group_id == group_id,
        LinkTable.thread_id == thread_id,
    ))
    return response.all()


#
#
# # @connection
# # async def unlink(group_id: int, thread_id: int, session: AsyncSession, hashtags: list[str] | None = None):
# #     if hashtags is None:
# #         query = await session.execute(select(LinkTable).where(
# #             LinkTable.group_id == group_id,
# #             LinkTable.thread_id == thread_id,
# #         ))
# #         links = query.scalars().all()
# #         for link in links:
# #             await session.delete(link)
# #     else:
# #         links = []
# #         for hashtag in hashtags:
# #             query = await session.execute(select(LinkTable).where(
# #                 LinkTable.group_id == group_id,
# #                 LinkTable.hashtag == hashtag,
# #                 LinkTable.thread_id == thread_id,
# #             ))
# #             links.append(query.scalar())
# #         for link in links:
# #             await session.delete(link)
# #     await session.commit()
#


# @connection
# async def unlink_group(group_id: int, thread_id: int, session: AsyncSession):
#     response = await session.scalars(select(LinkTable).where(
#         LinkTable.group_id == group_id,
#         LinkTable.thread_id == thread_id,
#     ))
#     for link in response.all():
#         await session.delete(link)
#     await session.commit()


@connection
async def unlink(channel_id: int, group_id: int, thread_id: int, hashtag: str, session: AsyncSession):
    response = await session.scalar(select(LinkTable).where(
        LinkTable.channel_id == channel_id,
        LinkTable.group_id == group_id,
        LinkTable.hashtag == hashtag,
        LinkTable.thread_id == thread_id,
    ))
    await session.delete(response)
    await session.commit()
#
#
# @connection
# async def unlink_channel(channel_id: int, hashtag: str, session: AsyncSession):
#     response = await session.scalar(select(LinkTable).where(
#         LinkTable.channel_id == channel_id,
#         LinkTable.hashtag == hashtag,
#     ))
#     await session.delete(response)
#     await session.commit()
