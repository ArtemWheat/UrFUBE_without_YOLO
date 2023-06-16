from typing import Any

from app.db import Base
from sqlalchemy import Column, String

from app.video.schemas import VideoUpload


class VideoModel(Base):
    __tablename__ = 'video'
    id = Column(String, primary_key=True, index=True)
    author_id = Column(String, primary_key=False, index=False)
    video_url = Column(String, primary_key=False, index=False)
    name = Column(String, primary_key=False, index=True)

    def __init__(self, upload: VideoUpload, **kw: Any):
        super().__init__(**kw)
        self.id = upload.id
        self.author_id = upload.author_id
        self.name = upload.name
        self.video_url = upload.video
