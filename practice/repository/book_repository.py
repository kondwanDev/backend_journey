from psycopg.rows import dict_row
from schemas.book import Book,UpdatedBook

class BookRepository:

    @staticmethod
    def get_books(conn, title:str = None, author: str = None, limit:int = 10, offset:int = 0, sort_by:str = "id", order_by:str = "desc"):

        cur = conn.cursor (row_factory = dict_row)

        query = "SELECT * FROM books"
        query_count = "SELECT COUNT(*) AS total FROM books"

        condition = []
        params = []

        if title:
            condition.append ("title ILIKE %s")
            params.append (f"%{title}%")
        
        if author:
            condition.append ("author ILIKE %s")
            params.append (f"%{author}%")

        if condition:
            query_clause= " WHERE " + " AND ".join(condition)
            query += query_clause
            query_count += query_clause

        # get total
        cur.execute (query_count, params)

        total = cur.fetchone()["total"] # count return one row "total"

        # pagination
        query += F" ORDER BY {sort_by} {order_by.upper()} LIMIT %s OFFSET %s "
        cur.execute (query, params + [limit, offset])
        books = cur.fetchall()

        
        cur.close()

        return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": books
    }
    
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
      