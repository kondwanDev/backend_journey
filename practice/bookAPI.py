from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Book (BaseModel):
    title : str
    author : str
    year : int

books = []

@app.post("/books")
def create_book (book: Book):
    books.append(book)
    return {"message": "book created successfully",
            "book":book}

@app.get("/books")
def get_allBooks ():
    return books

@app.get("/books/id/{book_id}")
def getBookById (book_id: int):
    if book_id < 0 or book_id >= len(books):
        return {"error": "book not found"}
    
    return books[book_id]

@app.get("/books/author/{author}")
def getBookByauth (author: str):
    bookAuthour = []

    for book in books:
      if book.author.lower() == author.lower():
        bookAuthour.append(book)
    
    if len(bookAuthour) == 0:
        return {"message":"book book not found"}
    
    return bookAuthour

@app.patch("/books/{book_id}")
def updateBook (book_id:int, book:Book):
    if book_id < 0 or book_id >= len(books):
        return {"error": "book not found"}
    
    books[book_id] = book
    return {"message": "book updated",
            "book": book}

@app.delete("/books/{book_id}")
def deleteBook(book_id:int):
    if book_id < 0 or book_id >= len(books):
        return {"error":"book not found"}
    
    deleted_book = books.pop(book_id)
    return {
        "message": "book deleted",
        "book" : deleted_book
    }
@app.get("/books/year/{year}")
def getByYear (year:int):
    bookYear = []
    for book in books:
        if book.year == year:
            bookYear.append(book)
    
    if len(bookYear) == 0:
        return {"message": "no book found for that year"}
    
    return bookYear
            