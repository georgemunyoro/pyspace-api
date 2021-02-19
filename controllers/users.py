from sqlalchemy.orm import Session
import models, schema
from bcrypt import gensalt, hashpw, checkpw
import base64
import hashlib


def hash_password(password: str):
    return hashpw(
        str(password).encode("utf-8"),
        gensalt(),
    ).decode("utf-8")


def get_user(db: Session, user_id: int):
    return db.query(models.user.User).filter(models.user.User.id == user_id).first()


def get_users(db: Session, offset: int = 0, limit: int = 50):
    return db.query(models.user.User).offset(offset).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.user.User).filter(models.user.User.email == email).first()


def create_user(db: Session, user: schema.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.user.User(
        email=user.email,
        password=hashed_password,
        is_verified=False,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(
    db: Session, user_id: int, old_password: str, new_password: str
):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()

    if user is None:
        return None

    print(user.password)
    print(old_password)
    print(str(hash_password(old_password)))

    if checkpw(str(old_password).encode("utf-8"), str(user.password).encode("utf-8")):
        setattr(user, "password", hash_password(new_password))

        db.add(user)
        db.commit()
        db.refresh(user)

    return None
