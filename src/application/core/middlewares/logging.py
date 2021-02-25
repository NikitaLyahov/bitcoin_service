import logging
import typing
from traceback import TracebackException
from uuid import uuid4

from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


RequestResponseEndpoint = typing.Callable[
    [Request], typing.Awaitable[Response]
]

logger = logging.getLogger('request.5XX')


class LoggingServerErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next: RequestResponseEndpoint) -> Response:

        try:
            response = await call_next(request)
        except Exception as exc:
            error_id = str(uuid4())
            await self._generate_log(error_id, request, exc)
            return await self._generate_response(error_id, exc)
        return response

    @staticmethod
    async def _generate_log(error_id: str, request: Request, exc: Exception) -> None:
        traceback_exception = TracebackException.from_exception(exc)
        logger.error(
            msg=str(exc),
            extra={
                'uuid': error_id,
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                'request.method': request.method,
                'request.path': request.url.path,
                'request.headers': dict(request.headers),
                'traceback': ''.join(traceback_exception.format())
            }
        )

    @staticmethod
    async def _generate_response(error_id: str, exc: Exception) -> JSONResponse:
        return JSONResponse({
            'detail': [{
                'type': f'Unexpected error: [{type(exc).__name__}]',
                'msg': str(exc),
                'error_id': str(error_id)
            }]
        }, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
