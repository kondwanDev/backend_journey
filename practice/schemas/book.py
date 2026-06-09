from pydantic import BaseModel
from typing import Optional

class Book (BaseModel):
    title : str
    author : str
    year : int

class UpdatedBook (BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    year : Optional [int] = None