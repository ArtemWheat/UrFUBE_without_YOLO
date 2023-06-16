from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import create_db
from app.user.routers import user_public_info, register_r, reset_password_r, verify_r, users_r
from app.site.router import template_r
from app.user.routers import auth_r
from app.video.router import video_r
from app.like.router import like_r

app = FastAPI()

app.include_router(user_public_info, prefix="/user_info", tags=["users_info"])
app.include_router(auth_r, prefix="/auth/jwt", tags=["auth"])
app.include_router(register_r, prefix="/auth", tags=["auth"], )
app.include_router(reset_password_r, prefix="/auth", tags=["auth"])
app.include_router(verify_r, prefix="/auth", tags=["auth"])
app.include_router(users_r, prefix="/users", tags=["users_info"])
app.include_router(template_r, tags=["pages"])
app.include_router(video_r, tags=["video_cr"])
app.include_router(like_r, tags=["like"])
app.mount('/static', StaticFiles(directory='./static'), name="static")


@app.on_event("startup")
async def on_startup():
    await create_db()
