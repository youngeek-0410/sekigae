from typing import Dict

from app.core.exceptions import ApiException, FailureLogin, InvalidEmailOrPassword
from app.core.jwt_handler import (
    TYPE_ACCESS_TOKEN,
    jwt_claims_handler,
    jwt_encode_handler,
    jwt_response_handler,
)
from app.core.security import verify_password
from app.crud.user import UserCRUD
from app.models import User
from app.schemas.auth import PaswordLoginSchema

from fastapi import Request


class AuthAPI:
    @classmethod
    def password_login(
        cls, request: Request, schema: PaswordLoginSchema
    ) -> Dict[str, str]:
        credentials = {"email": schema.email, "password": schema.password}

        if all(credentials.values()):
            user = cls().__authenticate_with_password(request, **credentials)
            access_token_claims = jwt_claims_handler(user, token_type=TYPE_ACCESS_TOKEN)
        else:
            raise ApiException(InvalidEmailOrPassword)
        return jwt_response_handler(jwt_encode_handler(access_token_claims))

    def __authenticate_with_password(
        self, request: Request, email: str, password: str
    ) -> User:
        user = UserCRUD(request.state.db_session).get_by_email(email=email)

        if not user:
            raise ApiException(FailureLogin)
        if not verify_password(password, user.hashed_password) or not user.is_active:
            raise ApiException(FailureLogin)
        return user
