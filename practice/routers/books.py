from fastapi import APIRouter, Depends
from psycopg.rows import dict_row # allow to return dictionary instead of tuples

from dependencies import get_db
from schemas.book import Book, UpdatedBook
from fastapi import HTTPException,status

router = APIRouter() #a mini FastAPI app for books only

@router.post ("/books", status_code= status.HTTP_201_CREATED)
def create_book (book: Book, conn = Depends(get_db)):

    if book.year < 0:
        raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                             detail= "Year cannot be negative"
                             )

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

    return {"message":"book created successfully",
            "Book":{
                "title":book.title,
                "author":book.author,
                "year":book.year
            }
            }

@router.get("/books")
def get_books(conn = Depends(get_db)):

    cur = conn.cursor(row_factory=dict_row)

    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    cur.close()
    return books

@router.get ("/books/{book_id}")
def get_book_by_id (book_id: int, conn = Depends (get_db)):

    cur = conn.cursor (row_factory = dict_row)
    
    cur.execute ("SELECT * FROM books WHERE id = %s",
                 (book_id,)
                 )
    book = cur.fetchone()

    cur.close ()

    if book is None:
        raise HTTPException (
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Book not found"
        )
    
    return book

@router.put ("/books/{book_id}")
def update_book(book_id: int, book: Book, conn = Depends(get_db)):

    if book.year  < 0:
        raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                             detail= "Year cannot be negative"
                             )

    cur = conn.cursor (row_factory = dict_row)

    cur.execute ("SELECT * FROM books WHERE id = %s",
                 (book_id,))
    
    existing = cur.fetchone()
    
    if existing is None:
        raise HTTPException (
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Book not found"
        )
    
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

@router.delete ("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_book (book_id: int, conn = Depends (get_db)):

    cur = conn.cursor (row_factory = dict_row)

    cur.execute ("SELECT * FROM books WHERE id = %s",
                 (book_id,))
    existing = cur.fetchone()

    if existing is None:
        raise HTTPException (
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Book not found"
        )

    cur.execute ("DELETE FROM books WHERE id = %s",
                 (book_id,))

    conn.commit()
    cur.close()

    return #already include no content in Func




@router.patch ("/books/{book_id}")
def patch_book (
    book_id: int,
    book: UpdatedBook,
    conn = Depends(get_db)
):
  
  if book.year is not None and book.year< 0: # not none because here we can have none
        raise HTTPException (status_code= status.HTTP_400_BAD_REQUEST,
                             detail= "Year cannot be negative"
                             )
  cur = conn.cursor (row_factory = dict_row)

  cur.execute ("SELECT * FROM books WHERE id = %s",
             (book_id,))

  existing = cur.fetchone()

  if existing is None:
    raise HTTPException (
        status_code= status.HTTP_404_NOT_FOUND,
        detail= "Book not found"
    )

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
  (new_title, new_author, new_year, book_id))

  conn.commit()
  cur.close()

  return {
    "message": "book updated successfully",
    "updated_book":{
        "id" : book_id,
        "title": new_title,
        "author": new_author,
        "year": new_year
    }
}