from typing import Optional

from app.core.exceptions import ApiException, InvalidToken
from app.models import User
from starlette import authentication

from fastapi import Request, security


class OAuth2PasswordBearer(security.OAuth2PasswordBearer):
    """OAuth2PasswordBearerのラッパー"""

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.headers.get("Authorization")
        scheme, param = security.utils.get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise ApiException(InvalidToken)
            else:
                return None
        return param


class AuthenticatedUser(authentication.SimpleUser):
    def __init__(self, user: User) -> None:
        self.uuid = user.uuid
        self.is_admin = user.is_admin
        self.is_active = user.is_active


class UnauthenticatedUser(authentication.UnauthenticatedUser):
    pass
