from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import ApiException, SystemException


async def api_exception_handler(request: Request, exception: ApiException) -> None:
    return JSONResponse(exception.detail, status_code=exception.status_code)


async def system_exception_handler(request: Request, exception: Exception) -> None:
    exception = SystemException(exception)
    return JSONResponse(exception.detail, status_code=exception.status_code)
