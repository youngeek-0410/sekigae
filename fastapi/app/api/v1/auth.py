from typing import Dict

import firebase_admin
from app.core.exceptions import (
    ApiException,
    ExpiredToken,
    FailureLogin,
    InvalidEmailOrPassword,
    InvalidToken,
    create_error,
)
from app.core.jwt_handler import (
    TYPE_ACCESS_TOKEN,
    jwt_claims_handler,
    jwt_encode_handler,
    jwt_response_handler,
)
from app.core.security import verify_password
from app.core.settings import get_env
from app.crud.user import UserCRUD
from app.models import User
from app.schemas import CreateUserSchema
from app.schemas.auth import FirebaseLoginSchema, PaswordLoginSchema
from firebase_admin import auth, credentials

from fastapi import Request

cred = credentials.Certificate(get_env().firebase_credentials_path)
firebase_admin.initialize_app(cred)


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

    @classmethod
    def firebase_login(
        cls, request: Request, schema: FirebaseLoginSchema
    ) -> Dict[str, str]:
        idtoken = schema.idtoken

        if idtoken:
            user = cls().__authenticate_with_firebase(request, idtoken)
            access_token_claims = jwt_claims_handler(user, token_type=TYPE_ACCESS_TOKEN)
        else:
            raise ApiException(InvalidToken)
        return jwt_response_handler(jwt_encode_handler(access_token_claims))

    def __authenticate_with_firebase(self, request: Request, idtoken: str) -> User:
        firebase_user_data = self.get_firebase_user_data(idtoken)

        user = UserCRUD(request.state.db_session).get_by_email(
            email=firebase_user_data["email"]
        )
        if not user:
            user_schema = CreateUserSchema(
                email=firebase_user_data["email"],
                username=firebase_user_data["username"],
                firebase_uid=firebase_user_data["firebase_uid"],
            )
            user = UserCRUD(request.state.db_session).create(user_schema.dict())
        return user

    def get_firebase_user_data(self, id_token: str):
        """
        This function receives id token sent by Firebase and
        validate the id token then check if the user exist on
        Firebase or not if exist it returns True else False
        """

        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        except auth.RevokedIdTokenError:
            raise ApiException(ExpiredToken)
        except Exception:
            raise ApiException(InvalidToken)

        try:
            firebase_uid: str = decoded_token["firebase_uid"]

            fetch_user = vars(auth.get_user(firebase_uid))
            user_info = fetch_user["_data"]["providerUserInfo"]
            provider: str = [
                d.get("providerId") for d in user_info if d.get("providerId")
            ][0]
            username: str = [
                d.get("displayName") for d in user_info if d.get("displayName")
            ][0]
            email: str = [d.get("email") for d in user_info if d.get("email")][0]
            return {
                "username": username,
                "provider": provider,
                "email": email,
                "firebase_uid": firebase_uid,
            }
        except Exception:
            raise ApiException(create_error("Firebase Error"))
