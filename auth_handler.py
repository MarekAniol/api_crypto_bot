from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from passlib.context import CryptContext
import fake_db
import models.user_models as model


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    
    
    def fake_decode_token(self, token):
        user = self.get_user(fake_db.mock_users_db, token)
        return user
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        user = self.fake_decode_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    def fake_hash_password(password: str):
        return "fakehashed" + password
    
    def get_user(db, username: str):
        if username in db: 
            user_dict = db[username]
            return model.UserInDB(**user_dict)
    
    async def get_current_active_user(current_user: model.User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    
