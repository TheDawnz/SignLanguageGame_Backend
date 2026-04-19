from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.auth import verify_token
from app.core.game import start_game, submit_answer
from app.db.database import get_db
from app.db.models import Score
from app.services.user_service import get_or_create_user
from app.ai.model import predict_sign

router = APIRouter()


class ImageRequest(BaseModel):
    image: str


class ScoreRequest(BaseModel):
    score: int = Field(..., ge=0)


@router.post("/start")
def start():
    return start_game()


@router.post("/submit")
def submit(data: ImageRequest):
    return submit_answer({"image": data.image})


@router.post("/detect")
def detect(data: ImageRequest):
    """Run AI prediction only — no game state changes."""
    predicted = predict_sign(data.image)
    return {"predicted": predicted}


@router.post("/score")
def post_score(
    data: ScoreRequest,
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = get_or_create_user(db, payload)

    score_row = Score(user_id=user.id, score=data.score)
    db.add(score_row)
    db.commit()
    db.refresh(score_row)

    return {
        "message": "Score saved",
        "score_id": score_row.id,
        "user_id": user.id,
        "score": score_row.score,
    }