from pydantic import BaseModel, Field
from typing import Optional

#What the client should send (POST, PUT)
class Book (BaseModel):
    title : str = Field (min_length= 1)
    author : str = Field (min_length= 1)
    year : int = Field (ge= 1900, le= 2026)

#What the client should send (PATCH)
class UpdatedBook (BaseModel):
    title : Optional[str] = Field(default= None, min_length= 1 )
    author : Optional[str] = Field(default= None, min_length= 1 )
    year : Optional [int]  = Field (default=None, ge= 1900, le= 2026)

#What the client should receive
class BookResponse (BaseModel):
    id : int
    title : str
    author : str
    year : int