from fastapi import FastAPI
from app.api import game

app = FastAPI()

app.include_router(game.router, prefix="/game")

@app.get("/")
def root():
    return {"message": "Sign Language Game API"}