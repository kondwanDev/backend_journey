from fastapi import APIRouter,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import get_db
from schemas.user import UserRegister,UserResponse

from service.user_service import UserService


router = APIRouter()

@router.post ("/register", status_code= status.HTTP_201_CREATED, response_model= UserResponse)

def register_user (user: UserRegister, conn = Depends(get_db)):
    return UserService.create_user (user, conn)

@router.post ("/login")
 
def user_login (form_data: OAuth2PasswordRequestForm = Depends(),
                 conn= Depends (get_db)):
   return UserService.login_user (form_data, conn)

    