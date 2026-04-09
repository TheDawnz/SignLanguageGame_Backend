from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schema.user_schema import UserCreate
from app.api.auth import get_current_user

router = APIRouter()

@router.post("/me")
def create_or_get_user(
    current=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.cognito_id == current["cognito_id"]).first()
    
    if not user:
        user = User(
            cognito_id=current["cognito_id"],
            username=current["username"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user