from pydantic import BaseModel, Field
from typing import Optional

class Book (BaseModel):
    title : str
    author : str
    year : int = Field (ge= 1900, le= 2026)

class UpdatedBook (BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    year : Optional [int]  = Field (default=None, ge= 1900, le= 2026)