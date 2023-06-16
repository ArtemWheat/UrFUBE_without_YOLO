import json.encoder

from fastapi_users.jwt import decode_jwt
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.responses import Response
from fastapi import Depends

from app.like.manager_likes import LikeManager
from app.user.auth import get_jwt_strategy
from app.user.user import User, current_active_user
from app.like.models import Like

like_r = InferringRouter()


@cbv(like_r)
class LikeRouter:
    def __init__(self):
        self.manager = LikeManager()
        self.jwt_strategy = get_jwt_strategy()

    @like_r.post("/video/{video_id}/like/{jwttoken}", response_class=Response)
    async def put_like(self, video_id: str, jwttoken: str):
        try:
            token = jwttoken.split(' ')[1]
            data = decode_jwt(token,
                              self.jwt_strategy.decode_key,
                              self.jwt_strategy.token_audience,
                              algorithms=[self.jwt_strategy.algorithm])
            user_id = data.get('sub')
        except Exception as e:
            print(e)
            return Response(status_code=401)
        create = Like(str(user_id), video_id)
        await self.manager.create(create)
        return Response(status_code=201)

    @like_r.post("/video/{video_id}/dislike/{jwttoken}", response_class=Response)
    async def remove_video(self, video_id: str, jwttoken: str):
        try:
            token = jwttoken.split(' ')[1]
            data = decode_jwt(token,
                              self.jwt_strategy.decode_key,
                              self.jwt_strategy.token_audience,
                              algorithms=[self.jwt_strategy.algorithm])
            user_id = data.get('sub')
        except Exception as e:
            print(e)
            return Response(status_code=401)
        like = Like(str(user_id), video_id)
        delete = await self.manager.delete(like)
        if not delete:
            return Response(status_code=409)
        return Response(status_code=200)

    @like_r.get("/video/{video_id}/is_liked/{jwttoken}", response_class=Response)
    async def is_liked(self, video_id: str, jwttoken: str):
        try:
            token = jwttoken.split(' ')[1]
            data = decode_jwt(token,
                              self.jwt_strategy.decode_key,
                              self.jwt_strategy.token_audience,
                              algorithms=[self.jwt_strategy.algorithm])
            user_id = data.get('sub')
        except Exception as e:
            print(e)
            return Response(status_code=401)
        like = Like(str(user_id), video_id)
        like = await self.manager.get_like(like)
        response = {'is_liked': True if like is not None else False}
        return Response(status_code=200, content=json.encoder.JSONEncoder().encode(response))
