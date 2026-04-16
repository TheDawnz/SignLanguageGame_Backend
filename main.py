from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user, leaderboard, game
from app.db.database import Base, engine
from app.db import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/user")
app.include_router(leaderboard.router, prefix="/leaderboard")
app.include_router(game.router, prefix="/game")

Base.metadata.create_all(bind=engine)