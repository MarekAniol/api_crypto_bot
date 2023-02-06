from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
from schemas import AuthDetails



def env_configure():
    load_dotenv()


app = FastAPI()


auth_handler = AuthHandler()

users = []

@app.post('/register')
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, details='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password
    })
    return

@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    if (user == None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, details='Invalid usernaem and/or password')
    token = auth_handler.enecode_token(user['username'])
    return {'token': token}

@app.get('/unprotected')
def unprotected():
    return {'status': 'unprotected'}

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}


def main():
    env_configure()
