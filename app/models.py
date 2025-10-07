from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base    


class BaseClass(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)


class User(BaseClass):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_staff = Column(Boolean,default =False)
    items = relationship("Item", back_populates="owner")


class Book(BaseClass):
    __tablename__ = "books"
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    isbn = Column(String, unique=True, index=True, nullable=False)
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)
    published_year = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    items = relationship("Item", back_populates="book")

    type = Column(String(50))  # Discriminator column

    __mapper_args__ = {
        "polymorphic_identity": "book",
        "polymorphic_on": type,  # Allows subclass recognition
    }

    items = relationship("Item", back_populates="book")
    description = relationship("Description", back_populates="book", uselist=False)

class Description(BaseClass):
    __tablename__ = "descriptions"
    
    content = Column(String, nullable=False)

    book_id = Column(Integer, ForeignKey("books.id"), unique=True)

    book = relationship("Book", back_populates="description")


class EBook(Book):
    __tablename__ = "ebooks"
    id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    file_format = Column(String, nullable=False)
    file_size_mb = Column(Integer, nullable=False)
    total_page = Column(Integer,nullable=False)
    download_link = Column(String, nullable=False)
    duration_days = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "ebook",
    }


class AudioBook(Book):
    __tablename__ = "audiobooks"
    id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    narrator = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    audio_format = Column(String, nullable=False)
    file_size_mb = Column(Integer, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "audiobook",
    }


class Loan(BaseClass):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    borrowed_at = Column(DateTime(timezone=True), server_default=func.now())
    returned_at = Column(DateTime(timezone=True), nullable=True)


    user = relationship('User', back_populates='loans')
    book = relationship('Book', back_populates='loans')