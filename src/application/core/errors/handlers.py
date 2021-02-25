from typing import Union, Any

from logging import getLogger
from uuid import uuid4

from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from application.core.errors.exceptions import LogHTTPException


logger = getLogger('request.4XX')


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_id = str(uuid4())
    headers = getattr(exc, 'headers', None)
    response_data = {'detail': exc.errors(), 'error_id': error_id}
    await _generate_log(error_id, request, 422, exc)
    return await _generate_response(headers, response_data, 422)


async def logging_http_exceptions_handler(request: Request,
                                          exc: LogHTTPException) -> JSONResponse:
    error_id = str(uuid4())
    headers = getattr(exc, 'headers', None)
    response_data = {'detail': exc.detail, 'error_id': error_id}
    await _generate_log(error_id, request, exc.status_code, exc)
    return await _generate_response(headers, response_data, exc.status_code)


async def _generate_log(error_id: str,
                        request: Request,
                        status_code: int,
                        exc: Union[LogHTTPException, RequestValidationError]) -> None:
    logger.error(
        msg=exc.detail if hasattr(exc, 'detail') else str(exc.errors()),
        extra={
            'uuid': error_id,
            'status_code': status_code,
            'request.method': request.method,
            'request.path': request.url.path,
            'request.headers': dict(request.headers),
        }
    )


async def _generate_response(headers: Any,
                             data: dict,
                             status_code: int) -> JSONResponse:
    if headers:
        return JSONResponse(data, status_code=status_code, headers=headers)
    return JSONResponse(data, status_code=status_code)
