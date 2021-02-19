from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgres://postgres:root@localhost:5432/pyspace"

engine = create_engine(DATABASE_URL)
SessonLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
