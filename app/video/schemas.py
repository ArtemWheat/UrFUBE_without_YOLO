from pydantic import BaseModel


class VideoUpload(BaseModel):
    id: str
    author_id: str
    video: str
    name: str


class VideoForView(BaseModel):
    id: str
    name: str
    video: str
