from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends # for dependency wrapper function
from database import get_connection
from psycopg.rows import dict_row # allow to return dictionary instead of tuples

app = FastAPI()

class Book (BaseModel):
    title : str
    author : str
    year : int
# it tells api to connect endpoint auto when request comes (dependency wrapper)
def get_db():
   # """function that connect endpoints to database automatically"""
    conn = get_connection()
    try:
        yield conn # return connection and wait until request ends
    
    finally:
        conn.close()


@app.post ("/books")
def create_book (book: Book, conn = Depends(get_db)):

    cur =conn.cursor()

    cur.execute(
        """
        INSERT INTO books (title, author, year)
        VALUES (%s, %s, %s)
        """,
        (book.title, book.author, book.year)
    )
    conn.commit()
    cur.close()

    return {"message":"book created successfully"}

@app.get ("/books")
def get_books (conn = Depends (get_db)):

    cur = conn.cursor(row_factory = dict_row) # allows first apply to return dict auto

    cur.execute ("SELECT * FROM books")
    books = cur.fetchall()

   
    cur.close()

    return books

@app.get ("/books/{book_id}")
def get_book_by_id (book_id: int, conn = Depends (get_db)):

    cur = conn.cursor (row_factory = dict_row)
    
    cur.execute ("SELECT * FROM books WHERE id = %s",
                 (book_id,)
                 )
    book = cur.fetchone()

    cur.close ()

    if book is None:
        return {"Message":"no book found"}
    
    return book

@app.put ("/books/{book_id}")
def update_book(book_id: int, book: Book, conn = Depends(get_db)):

    cur = conn.cursor (row_factory = dict_row)

    cur.execute ("SELECT * FROM BOOKS WHERE id = %s",
                 (book_id,))
    
    existing = cur.fetchone()
    
    if existing is None:
        return {"message":"book not found"}
    
    cur.execute ("""
        UPDATE books
        SET title = %s,
            author = %s,
            year   = %s   
        WHERE id   = %s      
         """,
         (book.title, book.author,book.year, book_id)
         )
    
    conn.commit()
    cur.close()

    return {
        "message" : "book updated successfuly",
        "data": {
            "id": book_id,
            "title": book.title,
            "author": book.author,
            "year" : book.year 
        }
    }

@app.delete ("/books/{book_id}")
def delete_book (book_id: int, conn = Depends (get_db)):

    cur = conn.cursor (row_factory = dict_row)

    cur.execute ("SELECT * FROM books WHERE id = %s",
                 (book_id,))
    existing = cur.fetchone()

    if existing is None:
        return {"message" : "book not found"}

    cur.execute ("DELETE FROM books WHERE id = %s",
                 (book_id,))

    conn.commit()
    cur.close()

    return {
        "message" : "book deleted successfuly",
        "deleted_book" : existing
    } 