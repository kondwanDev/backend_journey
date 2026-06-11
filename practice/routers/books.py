from fastapi import APIRouter, Depends
from psycopg.rows import dict_row # allow to return dictionary instead of tuples
from service.book_service import BookService

from dependencies import get_db
from schemas.book import Book, UpdatedBook
from fastapi import status

router = APIRouter() #a mini FastAPI app for books only

@router.post ("/books", status_code= status.HTTP_201_CREATED)
def create_book (book: Book, conn = Depends(get_db)):

    return BookService.create_book(book, conn)

@router.get("/books")
def get_books(conn = Depends(get_db)):
   
   return BookService.get_books(conn)
    

@router.get ("/books/{book_id}")
def get_book_by_id (book_id: int, conn = Depends (get_db)):

    return BookService.get_book_by_id (book_id, conn)

@router.put ("/books/{book_id}")
def update_book(book_id: int, book: Book, conn = Depends(get_db)):

   return BookService.update_book (book_id, book, conn)

@router.delete ("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book (book_id: int, conn = Depends (get_db)):

    return BookService.delete_book (book_id, conn)

@router.patch ("/books/{book_id}")
def patch_book (
    book_id: int,
    book: UpdatedBook,
    conn = Depends(get_db)
):
  
  return BookService.patch_book(book_id, book, conn)