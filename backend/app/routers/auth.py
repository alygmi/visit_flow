from fastapi import APIRouter
from sqlalchemy import select

from app.deps import DbSession
from app.errors import api_error
from app.models import User
from app.schemas import LoginRequest, LoginResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: DbSession) -> LoginResponse:
    user = db.scalar(select(User).where(User.username == payload.username))
    if user is None or not verify_password(payload.password, user.password_hash):
        api_error(401, "Username atau password salah.")

    return LoginResponse(
        token=create_access_token(user.id),
        user={"id": user.id, "name": user.name},
    )
