from fastapi import APIRouter, Depends
import models.users_models as user_model
from auth_handler import AuthHandler


router = APIRouter()

auth_handler = AuthHandler()

    
@router.get("/users/me")
async def read_users_me(current_user: user_model.User = Depends(auth_handler.get_current_user)):
    return current_user