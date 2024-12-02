from pydantic import BaseModel, Field
from typing import Optional


class UserBase(BaseModel):
    name : str
    email : str



class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True





class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    published_year: Optional[int] = Field(None, gt=0, description="Year must be greater than 0")
    isbn: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    published_year: Optional[int]
    isbn: Optional[str]

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True  # Allows using SQLAlchemy models directly