from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User, Score
from sqlalchemy import func

router = APIRouter()

@router.post("/score")
def save_score(
    score: int,
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.cognito_id == current["cognito_id"]).first()
    
    new_score = Score(user_id=user.id, score=score)
    db.add(new_score)
    db.commit()
    
    return {"message": "Score saved"}

@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    results = (
        db.query(User.username, func.max(Score.score).label("best_score"))
        .join(Score, User.id == Score.user_id)
        .group_by(User.username)
        .order_by(func.max(Score.score).desc())
        .limit(10)
        .all()
    )
    
    return results