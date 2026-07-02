from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class UserRegister (BaseModel):
    username: str = Field (min_length= 3, max_length= 50)
    email: EmailStr
    password: str = Field (min_length = 8)

class UserLogin (BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    