from fastapi import FastAPI
from app.db.database import Base, engine
from app.api import user, leaderboard

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(user.router, prefix="/user")
app.include_router(leaderboard.router, prefix="/leaderboard")