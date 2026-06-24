from psycopg.rows import dict_row
from schemas.book import Book, UpdatedBook
from  fastapi import HTTPException,status
from repository.book_repository import BookRepository

class BookService:

    @staticmethod
    def get_existing_book (book_id, conn):
        book = BookRepository.get_book_by_id (book_id, conn)
        if book is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail= "Book not found"
                                 )
        
        return book

    @staticmethod
    def get_books(conn, title:str = None, author: str = None, limit:int = 10, offset:int = 0):

        return BookRepository.get_books (conn, title, author,limit,offset)
    
    @staticmethod
    def create_book (book:Book, conn):
       
       created_book = BookRepository.create_book(book, conn)

       return created_book
    
    @staticmethod
    def get_book_by_id (book_id: int, conn):
        
       return BookService.get_existing_book (book_id, conn)
    
    @staticmethod
    def update_book (book_id: int, book: Book, conn):
        
        updated_book = BookRepository.update_book (book_id, book, conn)
                                            
        if updated_book is None:# no helper here cuz repo is doing checking by itself
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail= "Book not found")
        
        return updated_book

    @staticmethod
    def delete_book (book_id:int, conn):
        
        BookService.get_existing_book (book_id, conn)
        
        BookRepository.delete_book (book_id, conn)
        
        return None
    
    @staticmethod
    def patch_books (book_id: int, book: UpdatedBook, conn):
        
        existing = BookService.get_existing_book (book_id, conn)
        
        
        #take new title if title is not none or else take the existing title
        new_title = book.title if book.title is not None else existing["title"]
        new_author = book.author if book.author is not None else existing["author"]
        new_year = book.year if book.year is not None else existing["year"]

        
        updated_book = BookRepository.patch_books (book_id, new_title, new_author, new_year, conn)

        return updated_book