from repository.user_repository import UserRepository
from schemas.user import UserRegister
from utils.security import hash_password, password_verify, create_access_token
from  fastapi import HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

class UserService:

    @staticmethod
    def create_user (user:UserRegister, conn):

        existing_user = UserRepository.get_user_by_email (conn, user.email)
        if existing_user:
            raise HTTPException (
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "Email already exist"

            )
        
        existing_name = UserRepository.get_user_by_name(conn, user.username)
        if existing_name:
            raise HTTPException (
                status_code= status.HTTP_400_BAD_REQUEST,
                detail= "username already exist"
            )

        hashed_password = hash_password(user.password)

        created_user = UserRepository.create_user(
            conn,
            user.username,
            user.email,
            hashed_password
        )

        return created_user
    
    @staticmethod
    def login_user (form_data: OAuth2PasswordRequestForm , conn):

        existing_user = UserRepository.get_user_by_email(conn, form_data.username)
        if existing_user is None:
            raise HTTPException (
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "invalid email or password" #to prevent hacker to be aware which is wrong
            )
        
        password_match = password_verify (form_data.password, existing_user["password_hash"])

        if not password_match:
            raise HTTPException (
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail= "invalid email or password"
            )
        
        payload = {
            "sub" : str (existing_user ["id"])
        }

        access_token = create_access_token (payload)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }