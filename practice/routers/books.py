from fastapi import APIRouter, Depends
from psycopg.rows import dict_row # allow to return dictionary instead of tuples
from service.book_service import BookService

from dependencies import get_db
from schemas.book import Book, UpdatedBook, BookResponse, PaginatedBooks
from fastapi import status
from typing import Optional
from fastapi import Query

router = APIRouter() #a mini FastAPI app for books only

@router.post ("/books", 
              status_code= status.HTTP_201_CREATED,
              response_model= BookResponse
              )
def create_book (book: Book, conn = Depends(get_db)):

    return BookService.create_book(book, conn)

@router.get("/books",
            response_model= PaginatedBooks
            
            ) #list[] bcuz repo returns a list of dicts
def get_books(title:Optional[str]=None,
              author:Optional[str]=None,
              limit:int = Query (10, ge=1),
              offset:int = Query (0, ge=0),
              sort_by:str = Query ("id"),
              order_by:str = Query ("desc"),
               conn = Depends(get_db)):
   
   return BookService.get_books(conn, title, author, limit, offset, sort_by, order_by)
    

@router.get ("/books/{book_id}",
             response_model= BookResponse
             )
def get_book_by_id (book_id: int, conn = Depends (get_db)):

    return BookService.get_book_by_id (book_id, conn)

@router.put ("/books/{book_id}",
             response_model= BookResponse
             )
def update_book(book_id: int, book: Book, conn = Depends(get_db)):

   return BookService.update_book (book_id, book, conn)

@router.delete ("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book (book_id: int, conn = Depends (get_db)):

    return BookService.delete_book (book_id, conn)

@router.patch ("/books/{book_id}",
               response_model= BookResponse
               
               )
def patch_books (
    book_id: int,
    book: UpdatedBook,
    conn = Depends(get_db)
):
  
  return BookService.patch_books(book_id, book, conn)