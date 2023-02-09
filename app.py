from dotenv import load_dotenv
from fastapi import FastAPI
from .routers import users

def env_configure():
    load_dotenv()


app = FastAPI()


app.include_router(users.router)


mock_users_db = {
    "tomasharoson": {
        "username": "tomasharoson",
        "full_name": "Tomas Haroson",
        "email": "tomasharoson@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "grace": {
        "username": "grace",
        "full_name": "Grace Kennedy",
        "email": "grace@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


def main():
    env_configure()
