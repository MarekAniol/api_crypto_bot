from fastapi import APIRouter, Depends, HTTPException, status
from models import user_models as u_model, token_models as t_model
from auth_handler import AuthHandler
from fastapi.security import OAuth2PasswordRequestForm
import fake_db
import os


router = APIRouter()

auth_handler = AuthHandler()

    
@router.get("/users/me")
async def read_users_me(current_user: u_model.User = Depends(auth_handler.get_current_user)):
    return current_user

@router.get("/users/me/items/")
async def read_own_items(current_user: u_model.User = Depends(auth_handler.get_current_active_user)):
    return [{"item_id": "1", "owner": current_user.username}]

@router.post("/token", response_model=t_model.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_handler.authenticate_user(fake_db.mock_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth_handler.timedelta(minutes=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    access_token = auth_handler.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}