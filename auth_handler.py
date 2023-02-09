from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from passlib.context import CryptContext
import fake_db
from models import token_models as t_model, user_models as u_model
from jose import JWTError, jwt
import os


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    SECRET_KEY = os.getenv('JWT_SECRET')
    ALGORITHM = os.getenv('JWT_ALGORITHM')
    
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def authenticate_user(self, fake_db, username: str, password: str):
        user = self.get_user(fake_db, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )
        return encoded_jwt

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=self.ALGORITHM)
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = t_model.TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(fake_db.mock_users_db, username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    
    def get_user(db, username: str):
        if username in db: 
            user_dict = db[username]
            return u_model.UserInDB(**user_dict)
    
    async def get_current_active_user(current_user: u_model.User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    