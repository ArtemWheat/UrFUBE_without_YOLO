from sqlalchemy import select

from app.video.models import VideoModel
from app.db import async_session_maker


class VideoBrokerDB:
    async def get(self):
        async with async_session_maker() as session:
            result = await session.scalars(select(VideoModel))
            return [user for user in result]

    async def create(self, video: VideoModel):
        async with async_session_maker() as session:
            session.add(video)
            await session.commit()

    async def get_by_id(self, id):
        async with async_session_maker() as session:
            video = await session.get(VideoModel, id)
            return video

    async def delete_by_id(self, id):
        async with async_session_maker() as session:
            video = await self.get_by_id(id)
            if video is not None:
                await session.delete(video)
                await session.commit()
