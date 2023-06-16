import io
import uuid
from io import BytesIO
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.responses import Response, RedirectResponse
from fastapi import File, Form, UploadFile, Depends, FastAPI
from typing import Annotated

from app.user.auth import get_jwt_strategy
from app.user.user import User, get_user_manager
from app.video import video_broker
from app.video.async_uploader import upload_object, remove_object
from app.video.schemas import VideoUpload
from app.video.models import VideoModel
from fastapi_users.jwt import decode_jwt
from config import MAX_UPLOAD_SIZE, BUCKET, ENDPOINT_URL

video_r = InferringRouter()


@cbv(video_r)
class VideoRouter:
    def __init__(self):
        self.manager = video_broker.VideoBrokerDB()
        self.jwt_strategy = get_jwt_strategy()

    @video_r.post("/upload", response_class=Response)
    async def upload(self, name: Annotated[str, Form()],
                     file: Annotated[UploadFile, File()],
                     jwttoken: Annotated[str, Form()]):
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

        try:
            if list(reversed(file.filename.split('.')))[0] != 'mp4':  # TODO переделать через magic
                return Response(status_code=415, headers={'Location': '/upload'})
            if file.size > MAX_UPLOAD_SIZE:
                return Response(status_code=415, headers={'Location': '/upload'})

            id = str(uuid.uuid4()) + file.filename
            upload = VideoUpload(id=id,
                                 author_id=user_id,
                                 video=f'{ENDPOINT_URL}/{BUCKET}/{id}',
                                 name=name)

            await upload_object(file, io.BytesIO(await file.read()), upload.id)

            await self.manager.create(VideoModel(upload))
            return Response(status_code=202, content=upload.id, headers={'Location': '/upload'})
        except Exception as e:
            print(e)
            return Response(status_code=500, headers={'Location': '/upload'})

    @video_r.post("/delete", response_class=Response)
    async def delete(self, id: str, jwttoken: Annotated[str, Form()]):
        try:
            token = jwttoken.split(' ')[1]
            data = decode_jwt(token,
                              self.jwt_strategy.decode_key,
                              self.jwt_strategy.token_audience,
                              algorithms=[self.jwt_strategy.algorithm])
            user_id = data.get('sub')
        except Exception as e:
            print(e)
            return RedirectResponse(url=f'/video/{id}', status_code=401)

        video = await self.manager.get_by_id(id)
        if video.author_id != user_id:
            return RedirectResponse(url=f'/video/{video.id}', status_code=401)
        else:
            await remove_object(video.id)
            await self.manager.delete_by_id(video.id)
            return RedirectResponse(url="/", status_code=200)
