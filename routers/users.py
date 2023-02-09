from fastapi import APIRouter, Depends, HTTPException
import models.user_models as user_model
from auth_handler import AuthHandler
from fastapi.security import OAuth2PasswordRequestForm
import fake_db


router = APIRouter()

auth_handler = AuthHandler()

    
@router.get("/users/me")
async def read_users_me(current_user: user_model.User = Depends(auth_handler.get_current_user)):
    return current_user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_db.mock_users_db.get(form_data.username)
    
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = user_model.UserInDB(**user_dict)
    hashed_password = AuthHandler.fake_hash_password(form_data.password)
    
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}