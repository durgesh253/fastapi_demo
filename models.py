from sqlalchemy import Column,Integer,String,Text
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50),nullable=False)
    email = Column(String(50),unique=True,index=False)


class Book(Base):
    __tablename__ = "Books"
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String,index=True, nullable=False)
    author = Column(String,index=True, nullable=False)
    description = Column(Text,nullable=True)
    published_year = Column(Integer,nullable=True)
    isbn = Column(String, unique=True, nullable=False)

  