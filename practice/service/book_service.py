from psycopg.rows import dict_row
from schemas.book import Book, UpdatedBook
from  fastapi import HTTPException,status
from repository.book_repository import BookRepository

class BookService:
    @staticmethod
    def get_books(conn):

        return BookRepository.get_books (conn)
    
    @staticmethod
    def create_book (book:Book, conn):
        if book.year < 0:
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                 detail= "year should be positive")

        BookRepository.create_book(book, conn)

        return {"message":"Book created successfully",
                "created Book":{
                    "title":book.title,
                    "author":book.author,
                    "year":book.year
                }}
    
    @staticmethod
    def get_book_by_id (book_id: int, conn):
        
       book = BookRepository.get_book_by_id (book_id, conn)
       if book is None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail="book not found"
                                )
       
       return book 
    
    @staticmethod
    def update_book (book_id: int, book: Book, conn):
        
        existing = BookRepository.get_book_by_id (book_id,conn) # we are re_using the getbyid()
                                                     
        if existing is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail= "Book not found")
        
        if book.year < 0:
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                 detail= "year cannot be negative")
        
        BookRepository.update_book (book_id, book, conn)

        return {
            "message": "Book updated successfully",
            "Updated_book": {
                "id" : book_id,
                "title" : book.title,
                "author" : book.author,
                "year" : book.year
            }
        } 

    @staticmethod
    def delete_book (book_id:int, conn):
        
        existing = BookRepository.get_book_by_id(book_id, conn)

        if existing is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail="Book not found")
        
        BookRepository.delete_book (book_id, conn)
        
        return None
    
    @staticmethod
    def patch_books (book_id: int, book: UpdatedBook, conn):
        
        existing = BookRepository.get_book_by_id (book_id, conn)
        
        if existing is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail= "Book not found")
        
        if book.year is not None and book.year < 0:
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                 detail= "year cannot be negative")
        
        #take new title if title is not none or else take the existing title
        new_title = book.title if book.title is not None else existing["title"]
        new_author = book.author if book.author is not None else existing["author"]
        new_year = book.year if book.year is not None else existing["year"]

        
        BookRepository.patch_books (book_id, new_title, new_author, new_year, conn)

        return {
            "message": "Book updated successfullly",
            "updated book": {
                "id" : book_id,
                "title" : new_title,
                "author" : new_author,
                "year" : new_year
            }
        }