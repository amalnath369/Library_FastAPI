from pydantic import BaseModel,EmailStr,field_validator
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name : str
    email : EmailStr


class UserRead(BaseModel):
    id : int
    name :str
    email :EmailStr
    is_active :bool
    created_at : datetime

    class Config:
        orm_mode = True

    

class BookCreate(BaseModel):

    title : str
    author :Optional[str]
    isbn : str
    total_copies : int = 1
    published_year : Optional[int]

    @field_validator(published_year)
    def check_year(cls,v):
        if v is  not None :
            current = datetime.now().year
            if v < 1000 or v > current:
                 raise ValueError(f"published_year must be between 1000 and {current}")
        return v
    


class BookRead(BaseModel):
    id : int
    title : str
    author :Optional[str]
    isbn : str
    total_copies : int 
    available_copies : int
    published_year : Optional[int]
    created_at : datetime

    class Config:
        orm_mode = True


class LoanCreate(BaseModel):
    user_id: int
    book_id : int


class LoanRead(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    returned_at: Optional[datetime]


    class Config:
        orm_mode = True