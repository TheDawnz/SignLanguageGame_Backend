from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.api.auth import verify_token
from app.services.user_service import get_or_create_user

router = APIRouter()

@router.get("/me")
def get_me(
    payload=Depends(verify_token),
    db: Session = Depends(get_db)
):
    user = get_or_create_user(db, payload)

    return {
        "id": user.id,
        "username": user.username
    }