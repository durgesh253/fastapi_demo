from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from scemas import BookCreate, BookUpdate, BookResponse
from typing import List

router = APIRouter()

@router.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Create a new book
    new_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        published_year=book.published_year,
        isbn=book.isbn
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# @router.get("/books/", response_model=List[BookResponse])
# def get_books(db: Session = Depends(get_db)):
#     # Get all books
#     return db.query(Book).all()



@router.get("/books/", response_model=dict)
def get_books(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100, description="Number of books to retrieve (1-100)"),
    offset: int = Query(0, ge=0, description="Number of books to skip")
):
    # Get total count of books
    total_books = db.query(func.count(Book.id)).scalar()

    # Fetch books with limit and offset
    books = db.query(Book).offset(offset).limit(limit).all()

    return {
        "total": total_books,
        "limit": limit,
        "offset": offset,
        "books": books
    }

@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    # Get a single book by ID
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_data: BookUpdate, db: Session = Depends(get_db)):
    # Update a book by ID
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # Delete a book by ID
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
