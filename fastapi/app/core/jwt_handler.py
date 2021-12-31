from datetime import datetime, timedelta
from typing import Any, Dict

from app.core.settings import get_env
from app.models import User
from jose import jwt  # python-jose

TYPE_ACCESS_TOKEN = "access_token"
TYPE_REFRESH_TOKEN = "refresh_token"

PROTECTED_TOKEN_TYPES = TYPE_ACCESS_TOKEN


def jwt_claims_handler(user: User, token_type: str = "") -> Dict[str, Any]:
    assert (
        token_type in PROTECTED_TOKEN_TYPES
    ), f'引数token_type には{"".join(PROTECTED_TOKEN_TYPES)}を指定してください'

    claims = {
        "token_type": token_type,
        "user_uuid": str(user.uuid),
    }
    if claims["token_type"] == TYPE_ACCESS_TOKEN:
        claims["exp"] = datetime.utcnow() + timedelta(
            seconds=get_env().jwt_access_token_expire_sec
        )
    return claims


def jwt_encode_handler(claims: dict) -> str:
    return jwt.encode(claims, get_env().jwt_secret_key, get_env().jwt_algorithm)


def jwt_decord_handler(jwt_string: str) -> Dict[str, Any]:
    return jwt.decode(
        jwt_string,
        get_env().jwt_secret_key,
        algorithms=get_env().jwt_algorithm,
    )


def jwt_response_handler(access_token: str) -> Dict[str, str]:
    return {"token_type": "bearer", TYPE_ACCESS_TOKEN: access_token}
