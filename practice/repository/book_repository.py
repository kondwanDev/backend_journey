from psycopg.rows import dict_row
from schemas.book import Book,UpdatedBook

class BookRepository:

    @staticmethod
    def get_books(conn):

        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("SELECT * FROM books")
        books = cur.fetchall()
        
        cur.close()
        return books
    
    @staticmethod
    def create_book (book:Book, conn):
        
        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("""
                     INSERT INTO books (title, author, year)
                     VALUES (%s, %s, %s)
                     RETURNING id, title, author, year
                 """,
                 (book.title, book.author, book.year)
                 )
        created_book = cur.fetchone()
        
        conn.commit()
        cur.close()

        return created_book

    @staticmethod
    def get_book_by_id (book_id: int, conn):

        cur = conn.cursor(row_factory = dict_row)

        cur.execute ("SELECT * FROM books WHERE id = %s",
                     (book_id,))
        
        existing = cur.fetchone() # this always return dictionary
    
        cur.close()

        return existing
    
    @staticmethod
    def update_book (book_id:int, book:Book, conn):

        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("""
                     UPDATE books
                     SET title = %s,
                         author = %s,
                         year = %s
                     WHERE id = %s
                     RETURNING id, title, author, year
                 """,
                 (book.title, book.author, book.year, book_id)
                 )
        updated_book = cur.fetchone()

        conn.commit()
        cur.close()

        return updated_book

    @staticmethod
    def delete_book (book_id:int, conn):

        cur = conn.cursor () # we're not returning anything

        cur.execute ("DELETE FROM books WHERE id = %s",
                     (book_id,)
                      )
        
        conn.commit()
        cur.close()

    @staticmethod
    def patch_books (book_id:int, title:str, author:str, year:int, conn): #patch we pass updated data

        cur = conn.cursor (row_factory = dict_row)

        cur.execute ("""
                     UPDATE books
                     SET title = %s,
                         author = %s,
                         year = %s
                     WHERE id = %s
                     RETURNING id, title, author, year
                 """,
                 (title, author, year, book_id)
                 )
        Updated_book = cur.fetchone()
        
        conn.commit()
        cur.close()

        return Updated_book
      