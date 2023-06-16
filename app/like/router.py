import json.encoder

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.responses import Response
from fastapi import Depends

from app.like.manager_likes import LikeManager
from app.user.user import User, current_active_user
from app.like.models import Like

like_r = InferringRouter()


@cbv(like_r)
class LikeRouter:
    def __init__(self):
        self.manager = LikeManager()

    @like_r.post("/video/{video_id}/like", response_class=Response)
    async def put_like(self, video_id: str, user: User = Depends(current_active_user)):
        create = Like(str(user.id), video_id)
        await self.manager.create(create)
        return Response(status_code=201)

    @like_r.post("/video/{video_id}/dislike", response_class=Response)
    async def remove_like(self, video_id: str, user: User = Depends(current_active_user)):
        like = Like(str(user.id), video_id)
        delete = await self.manager.delete(like)
        if not delete:
            return Response(status_code=409)
        return Response(status_code=200)

    @like_r.get("/video/{video_id}/is_liked", response_class=Response)
    async def is_liked(self, video_id: str, user: User = Depends(current_active_user)):
        like = Like(str(user.id), video_id)
        like = await self.manager.get_like(like)
        response = {'is_liked': True if like is not None else False}
        return Response(status_code=200, content=json.encoder.JSONEncoder().encode(response))
