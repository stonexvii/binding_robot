from database.database import async_session
from database.requests import new_link


class Link:
    def __init__(self, user_id: int, hashtags: list[str], channel_id: int, group_id: int, thread_id: int | None):
        self.user_id = user_id
        self.hashtags = hashtags
        self.channel_id = channel_id
        self.group_id = group_id
        self.thread_id = thread_id if thread_id else 0

    async def create_link(self) -> list[str]:
        reports = await new_link(
            self.user_id,
            self.hashtags,
            self.channel_id,
            self.group_id,
            self.thread_id,
        )
        return reports
