from fastapi import APIRouter
from app.core.game import start_game, submit_answer

router = APIRouter()

@router.post("/start")
def start():
    return start_game()

@router.post("/submit")
def submit(data: dict):
    return submit_answer(data)