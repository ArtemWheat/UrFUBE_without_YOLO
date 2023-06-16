from typing import Annotated

from fastapi import Depends, Form, Response
from fastapi_users.jwt import decode_jwt
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.user.auth import get_jwt_strategy
from app.user.schemas import UserCreate, UserRead, UserUpdate
from app.user.user import auth_backend, fastapi_users
from app.video import video_broker

auth_r = fastapi_users.get_auth_router(auth_backend)
register_r = fastapi_users.get_register_router(UserRead, UserCreate)
reset_password_r = fastapi_users.get_reset_password_router()
verify_r = fastapi_users.get_verify_router(UserRead)
users_r = fastapi_users.get_users_router(UserRead, UserUpdate)

user_public_info = InferringRouter()


@cbv(user_public_info)
class VideoRouter:
    def __init__(self):
        self.jwt_strategy = get_jwt_strategy()

    @user_public_info.get("/")
    async def get_user_public_info(self, jwttoken: Annotated[str, Form()]):
        try:
            token = jwttoken.split(' ')[1]
            data = decode_jwt(token,
                              self.jwt_strategy.decode_key,
                              self.jwt_strategy.token_audience,
                              algorithms=[self.jwt_strategy.algorithm])
            user_id = data.get('sub')
            return user_id
        except Exception as e:
            print(e)
            return Response(status_code=401)
