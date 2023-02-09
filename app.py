from dotenv import load_dotenv
from fastapi import FastAPI
from routers import users

def env_configure():
    load_dotenv()


app = FastAPI()


app.include_router(users.router)


def main():
    env_configure()
