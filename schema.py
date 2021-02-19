from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    firstname: str
    lastname: str


class PostBase(BaseModel):
    title: str
    contents: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: Optional[str]
    contents: Optional[str]


class Post(PostBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_verified: bool
    posts: List[Post] = []

    class Config:
        orm_mode = True


class UserPasswordReset(BaseModel):
    old_password: str
    new_password: str
