from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import Session
from database import SessonLocal, engine, Base
import models, schema, controllers

Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessonLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=List[schema.User])
def get_user_list(offset: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = controllers.users.get_users(db=db, offset=offset, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schema.User)
def get_user_info(user_id: int, db: Session = Depends(get_db)):
    user = controllers.users.get_user(db=db, user_id=user_id)
    return user


@app.post("/users", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = controllers.users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return controllers.users.create_user(db=db, user=user)


@app.post("/users/{user_id}/posts")
def create_post(user_id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    post = controllers.posts.create_post(db=db, post=post, user_id=user_id)
    return post


@app.get("/users/{user_id}/posts", response_model=List[schema.Post])
def get_user_posts(
    user_id: int, offset: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    posts = controllers.posts.list_posts(db=db, offset=offset, limit=limit)
    return posts


@app.get("/users/{user_id}/posts/{post_id}", response_model=schema.Post)
def get_user_post_info(user_id: int, post_id: int, db: Session = Depends(get_db)):
    post = controllers.posts.get_post(db=db, post_id=post_id)
    if post:
        if post.author_id == user_id:
            return post
    return None


@app.patch("/users/{user_id}/posts/{post_id}", response_model=schema.Post)
def update_post(post_id: int, data: schema.PostUpdate, db: Session = Depends(get_db)):
    return controllers.posts.update_post(db=db, post_id=post_id, data=data)


@app.post("/users/{user_id}/reset-password")
def reset_user_password(user_id: int, passwords: schema.UserPasswordReset, db: Session = Depends(get_db)):
    return controllers.users.update_user_password(
        db=db,
        user_id=user_id,
        old_password=passwords.old_password,
        new_password=passwords.new_password,
    )
