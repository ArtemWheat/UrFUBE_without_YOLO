from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.like import manager_likes
from app.video import video_broker
from app.video.schemas import VideoForView

templates = Jinja2Templates(directory="templates")

template_r = InferringRouter()
manager_videos = video_broker.VideoBrokerDB()
manager_like = manager_likes.LikeManager()


@template_r.get("/video/{id}", response_class=HTMLResponse)
async def video_page(request: Request, id: str):
    video = await manager_videos.get_by_id(id)
    if not video:
        return templates.TemplateResponse("video.html", {"request": request, "video": video})
    count_like = await manager_like.get_likes_count(id)
    video_for_view = VideoForView(id=video.id, name=video.name, video=video.video_url)
    return templates.TemplateResponse("video.html", {"request": request, "video": video_for_view, 'count_like': count_like})


@cbv(template_r)
class TemplateRouter:
    def __init__(self):
        self.manager = video_broker.VideoBrokerDB()

    @template_r.get("/login", response_class=HTMLResponse)
    async def login_page(self, request: Request):
        return templates.TemplateResponse("login.html", {"request": request})

    @template_r.get("/registration", response_class=HTMLResponse)
    async def video_page(self, request: Request):
        return templates.TemplateResponse("registration.html", {"request": request})

    @template_r.get("/", response_class=HTMLResponse)
    async def index_page(self, request: Request):
        videos = await self.manager.get()
        videos_urls = [VideoForView(id=video.id, name=video.name, video=video.video_url) for video in videos]
        return templates.TemplateResponse("index.html", {"request": request, "videos": videos_urls})

    @template_r.get("/upload", response_class=HTMLResponse)
    async def upload_page(self, request: Request):
        return templates.TemplateResponse("upload.html", {"request": request})
