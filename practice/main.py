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


@app.post ("/book")
def create_book (book: Book, conn = Depends(get_db)):

    conn = get_connection()
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