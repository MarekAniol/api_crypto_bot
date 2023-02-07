from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from auth_handler import AuthHandler
from schemas import AuthDetails


def env_configure():
    load_dotenv()


app = FastAPI()


mock_users_db = {
    "tomasharoson": {
        "username": "tomasharison",
        "full_name": "Tomas Harison",
        "email": "tomasharison@example.com",
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
