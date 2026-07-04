from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dependencies import get_db

from utils.security import decode_access_token
from repository.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer (
    tokenUrl= "/login"
)

def get_current_user (token: str = Depends (oauth2_scheme), conn = Depends (get_db)):
    payload = decode_access_token (token)

    user_id = payload.get("id")

    if user_id is None:
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid authentication credentials"
        )
    
    current_user = UserRepository.get_user_by_id(conn, int(user_id)) # we converted payload remember?

    if current_user is None:
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "User not found"
        )

    return current_user 