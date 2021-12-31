from app.core.auth import OAuth2PasswordBearer
from app.core.exceptions import ApiException, InvalidToken, PermissionDenied

from fastapi import Depends, Request

PASSWORD_LOGIN = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/password")


async def login_required(
    request: Request, password_login=Depends(PASSWORD_LOGIN)
) -> None:
    if not request.user.is_authenticated:
        raise ApiException(InvalidToken)


async def admin_required(
    request: Request, password_login=Depends(PASSWORD_LOGIN)
) -> None:
    if not request.user.is_authenticated:
        raise ApiException(InvalidToken)
    if not request.user.is_admin:
        raise ApiException(PermissionDenied)
