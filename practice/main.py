from fastapi import FastAPI
from routers import books, users

app = FastAPI()

app.include_router(books.router)
app.include_router (users.router)