import base64
import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional

from bcrypt import checkpw, gensalt, hashpw
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import models
import schema

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        user_id: int = pauload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schema.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = get_user(db=db, user_id=token_data.user_id)

    if user is None:
        raise credentials_exception
    return user


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


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.user.User).filter(models.user.User.email == email).first()

    try:
        if checkpw(str(password).encode("utf-8"), str(user.password).encode("utf-8")):
            return user
    except:
        raise HTTPException(
            status_code=400,
            detail="An error ocurred while attempting to login with provided credentials.",
        )


def update_user_password(
    db: Session, user_id: int, old_password: str, new_password: str
):
    user = db.query(models.user.User).filter(models.user.User.id == user_id).first()

    if user is None:
        return None

    if checkpw(str(old_password).encode("utf-8"), str(user.password).encode("utf-8")):
        setattr(user, "password", hash_password(new_password))

        db.add(user)
        db.commit()
        db.refresh(user)

    return None
