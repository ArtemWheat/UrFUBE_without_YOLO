from app.like.models import Like
from app.db import async_session_maker
from sqlalchemy import select


class LikeManager:
    async def get(self) -> list[Like]:
        async with async_session_maker() as session:
            result = await session.scalars(select(Like))
            return [like for like in result]

    async def create(self, like: Like):
        async with async_session_maker() as session:
            session.add(like)
            await session.commit()

    async def get_likes_count(self, video_id: str) -> int:
        likes = await self.get()
        likes = list(filter(lambda x: x.video_id == video_id, likes))
        return len(likes)

    async def get_like(self, like: Like) -> Like:
        likes = await self.get()
        likes = list(filter(lambda x: x.video_id == like.video_id, likes))
        like = list(filter(lambda x: x.user_id == like.user_id, likes))
        return None if len(like) == 0 else like[0]

    async def delete(self, like):
        async with async_session_maker() as session:
            likes = await self.get()
            like = list(filter(lambda x: x.user_id == like.user_id and x.video_id == like.video_id, likes))
            if len(like) != 0:
                like = like[0]
                await session.delete(like)
                await session.commit()
                return True
