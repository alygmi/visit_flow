from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import api_error
from app.models import User
from app.security import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ] = None,
) -> User:
    unauthorized_headers = {"WWW-Authenticate": "Bearer"}

    if credentials is None or credentials.scheme.lower() != "bearer":
        api_error(
            401,
            "Token autentikasi diperlukan.",
            headers=unauthorized_headers,
        )

    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        api_error(
            401,
            "Sesi tidak valid atau sudah kedaluwarsa.",
            headers=unauthorized_headers,
        )

    user = db.get(User, user_id)
    if user is None:
        api_error(
            401,
            "Sesi tidak valid atau sudah kedaluwarsa.",
            headers=unauthorized_headers,
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
