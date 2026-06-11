from psycopg.rows import dict_row
from schemas.book import Book, UpdatedBook
from  fastapi import HTTPException,status

class BookService:
    @staticmethod
    def get_books(conn):

        cur = conn.cursor(row_factory = dict_row)
        
        cur.execute ("SELECT * FROM books ")
        books = cur.fetchall()
        cur.close()

        return books
    
    @staticmethod
    def create_book (book:Book, conn):
        if book.year < 0:
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                 detail= "year should be positive")

        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("""INSERT INTO books (title,author,year)
                     VALUES (%s,%s,%s)
                         
                    """,
                    (book.title,book.author,book.year)
                    )
        
        conn.commit()
        cur.close()
        return {"message":"Book created successfully",
                "created Book":{
                    "title":book.title,
                    "author":book.author,
                    "year":book.year
                }}
    
    @staticmethod
    def get_book_by_id (book_id: int, conn):
        
        cur = conn.cursor (row_factory = dict_row)
        cur.execute ("SELECT * FROM books WHERE id = %s",
                     (book_id,))
        
        book = cur.fetchone()
        if book is None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                detail="book not found"
                                )
        cur.close()

        return book 
    
    @staticmethod
    def update_book (book_id: int, book: Book, conn):
        if book.year < 0:
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                 detail= "year cannot be negative")
        
        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("SELECT * FROM books WHERE id = %s",
                     (book_id,))
        
        existing = cur.fetchone() #produces a dict
        if existing is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail= "Book not found")
        
        cur.execute ("""UPDATE books
                     SET title = %s,
                         author = %s,
                         year = %s
                    WHERE id = %s""",
                    (book.title, book.author, book.year, book_id)
                    )
        
        conn.commit()
        cur.close()

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

        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("SELECT * FROM books  WHERE id = %s",
                     (book_id,)) 
        existing = cur.fetchone()

        if existing is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail="Book not found")
        
        cur.execute ("DELETE FROM books WHERE id = %s",
                     (book_id,))
        
        conn.commit()
        cur.close()
        
        return # already included 204 in route
    
    @staticmethod
    def patch_book (book_id: int, book: UpdatedBook, conn):
        if book.year is not None and book.year < 0:
            raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                                 detail= "year cannot be negative")
        
        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("SELECT * FROM books WHERE id = %s",
                     (book_id,))
        
        existing = cur.fetchone()
        if existing is None:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND,
                                 detail= "Book not found")
        
        #take new title if title is not none or else take the existing title
        new_title = book.title if book.title is not None else existing["title"]
        new_author = book.author if book.author is not None else existing["author"]
        new_year = book.year if book.year is not None else existing["year"]

        cur.execute ("""
                     UPDATE books
                     SET title = %s,
                         author = %s,
                         year = %s
                     WHERE id = %s

                  """,
                  (new_title, new_author, new_year, book_id)
                  )
        
        conn.commit()
        cur.close()

        return {
            "message": "Book updated successfullly",
            "updated book": {
                "id" : book_id,
                "title" : new_title,
                "author" : new_author,
                "year" : new_year
            }
        }