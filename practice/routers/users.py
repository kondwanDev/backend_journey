from fastapi import APIRouter,Depends,status
from dependencies import get_db
from schemas.user import UserRegister,UserResponse, UserLogin

from service.user_service import UserService

router = APIRouter()

@router.post ("/register", status_code= status.HTTP_201_CREATED, response_model= UserResponse)

def register_user (user: UserRegister, conn = Depends(get_db)):
    return UserService.create_user (user, conn)

@router.post ("/login")
 
def user_login (user: UserLogin, conn= Depends (get_db)):
   return UserService.login_user (user, conn)

    