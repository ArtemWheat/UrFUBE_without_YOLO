from typing import Any
from sqlalchemy import Column, String
from app.db import Base


class Like(Base):
    __tablename__ = 'likes'
    user_id = Column(String, primary_key=True, index=False)
    video_id = Column(String, primary_key=True, index=False)

    def __init__(self, user_id, video_id, **kw: Any):
        super().__init__(**kw)
        self.user_id = user_id
        self.video_id = video_id
