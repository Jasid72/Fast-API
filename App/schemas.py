from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class CreatePost(PostBase):
    pass