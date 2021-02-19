from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_verified = Column(Boolean, default=False)

    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    username = Column(String, index=True, unique=True)

    posts = relationship("Post", back_populates="author")
