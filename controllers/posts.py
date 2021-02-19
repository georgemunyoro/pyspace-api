from sqlalchemy.orm import Session
import models, schema


def list_posts(db: Session, offset: int, limit: int):
    return db.query(models.post.Post).offset(offset).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(models.post.Post).filter(models.post.Post.id == post_id).first()


def update_post(db: Session, post_id: int, data: schema.PostUpdate):
    post = db.query(models.post.Post).filter(models.post.Post.id == post_id).first()

    if post is None:
        return None

    for key, val in data:
        setattr(post, key, val) if val else None

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def create_post(db: Session, post: schema.PostCreate, user_id: int):
    db_post = models.post.Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
