from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LiffLoginRequest, LiffLoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/liff-login", response_model=LiffLoginResponse)
def liff_login(payload: LiffLoginRequest, db: Session = Depends(get_db)) -> LiffLoginResponse:
    user = db.query(User).filter(User.line_user_id == payload.line_user_id).first()
    if user is None:
        user = User(
            line_user_id=payload.line_user_id,
            display_name=payload.display_name,
            avatar_url=payload.avatar_url,
            role="buyer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    if user.id is None:
        raise HTTPException(status_code=500, detail="Failed to create user")
    return LiffLoginResponse(access_token=f"dev-token-{user.id}", user_id=user.id, role=user.role)
