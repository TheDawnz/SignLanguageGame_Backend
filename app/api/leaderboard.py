from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, Score

router = APIRouter()


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    results = (
        db.query(User.username, func.max(Score.score).label("best_score"))
        .join(Score)
        .group_by(User.username)
        .order_by(func.max(Score.score).desc())
        .limit(10)
        .all()
    )
    return [
        {"rank": i + 1, "name": s[0], "score": s[1]}
        for i, s in enumerate(results)
    ]