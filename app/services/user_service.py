from app.db.models import User

def get_or_create_user(db, payload):
    user = db.query(User).filter(
        User.cognito_id == payload["sub"]
    ).first()

    if not user:
        user = User(
            cognito_id=payload["sub"],
            username=payload.get("username", "unknown")
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user