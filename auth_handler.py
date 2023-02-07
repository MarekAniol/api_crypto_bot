import jwt
from fastapi import Security, HTTPException, Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from passlib.context import CryptContext
import models.users_models as model


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    
    def fake_decode_token(self, token):
        return model.User(
            username=token + 'fakedecoded',
            email='marekaniol1@gmail.com',
            full_name='Marek Anioł'
        )
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        user = self.fake_decode_token(token)
        return user
