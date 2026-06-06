from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Depends
from database import get_connection

app = FastAPI()

class Book (BaseModel):
    title : str
    author : str
    year : int

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

    cur = conn.cursor()

    cur.execute ("SELECT * FROM books")
    rows = cur.fetchall()

    books = [
      { 
         "id":row[0],
            "title": row[1],
            "author": row[2],
            "year":row[3]
      }
       for row in rows
    ]

  
    cur.close()

    return books