from logging import getLogger

from app.core.auth import AuthenticatedUser, UnauthenticatedUser
from app.core.exceptions import ApiException, ExpiredToken
from app.core.jwt_handler import jwt_decord_handler
from app.crud.user import UserCRUD
from jose import jwt
from starlette.middleware import authentication

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

logger = getLogger(__name__)


class BackendAuth(authentication.AuthenticationBackend):
    """
    このミドルウェアを認証バックエンドとして使用することで、リクエストのユーザー情報に「request.user」でアクセス可能になる
    """

    async def authenticate(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, access_token = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            return (
                authentication.AuthCredentials(["unauthenticated"]),
                UnauthenticatedUser(),
            )

        try:
            claims = jwt_decord_handler(access_token)
        except jwt.ExpiredSignatureError:
            raise ApiException(ExpiredToken)
        except Exception as e:
            logger.info(e)
            return (
                authentication.AuthCredentials(["unauthenticated"]),
                UnauthenticatedUser(),
            )

        user = UserCRUD(request.state.db_session).get_by_uuid(claims["user_uuid"])
        if not user or not user.is_active:
            # raise ApiException(InvalidToken)
            return (
                authentication.AuthCredentials(["unauthenticated"]),
                UnauthenticatedUser(),
            )
        return authentication.AuthCredentials(["authenticated"]), AuthenticatedUser(
            user
        )
