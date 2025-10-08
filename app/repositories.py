from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update,func
from . import models
from typing import List, Optional



class UserRepository:
    def __init__(self, session : AsyncSession):
        self.session=session
        

    async def create(self, name :str, email : str) -> models.User:
        obj = models.User(name =name ,email =email)
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    async def get_user_by_id(self,user_id : int) ->Optional[models.User]:
        obj = await self.session.get(models.User,user_id)
        return obj
    
    async def get_by_email(self, email: str) -> Optional[models.User]:
        stmt = select(models.User).where(models.User.email == email)
        res = await self.session.execute(stmt)
        return res.scalars().first()
    

class BookRepository:
    def __init__(self, session : AsyncSession):
        self.session = session

    
    async def book_create(self, title : str ,author :Optional[str], isbn :str, published_year : Optional[int],total_copies : int =1,) -> models.Book:
        obj =models.Book(title =title ,author =author , total_copies=total_copies,available_copies=total_copies,published_year=published_year)
        self.session.add(obj)
        await self.session.flush()
        return obj
    
    async def get_by_id(self, book_id : int) -> Optional[models.Book]:
        return await self.session.get(models.Book,book_id)


    async def list_all(self) -> List[models.Book]:
        obj= select(models.Book)
        result = await self.session.execute(obj)
        return result.scalars().all()
    
    async def delete_book(self,book_id : int) -> None:
        book =await self.session.get(models.Book,book_id)
        if not book:
            raise ValueError(f'No Book with Book Id {book_id} found!!')
        await self.session.delete(book)
        await self.session.flush()


    async def add_more(self,books :models.Book) -> None:
        books.total_copies+=1
        await self.session.flush()
    
    async def remove_more(self,books :models.Book) -> None:
        books.total_copies-=1
        await self.session.flush()

    async def increment(self,books : models.Book) -> None:
        books.available_copies+=1
        await self.session.flush()

    async def decrement(self,books : models.Book) -> None:
        if books.available_copies<=0:
            raise ValueError('No copies available')
        books.available_copies -= 1
        await self.session.flush()



class LoanRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create(self, user_id: int, book_id: int) -> models.Loan:
        obj = models.Loan(user_id=user_id, book_id=book_id)
        self.session.add(obj)
        await self.session.flush()
        return obj


    async def get_active_loan(self, user_id: int, book_id: int) -> Optional[models.Loan]:
        stmt = select(models.Loan).where(models.Loan.user_id == user_id, models.Loan.book_id == book_id, models.Loan.returned_at == None)
        res = await self.session.execute(stmt)
        return res.scalars().first()


    async def mark_returned(self, loan: models.Loan) -> None:
        loan.returned_at = func.now()
        await self.session.flush()
                