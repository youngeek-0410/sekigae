from app.core.settings import get_env
from starlette.middleware import cors
from starlette.types import ASGIApp


class CORSMiddleware(cors.CORSMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            allow_origins=get_env().allow_origins,
            allow_methods=cors.ALL_METHODS,
            allow_headers=get_env().allow_headers,
            allow_credentials=True,
        )
