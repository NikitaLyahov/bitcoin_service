from logging import config as logging_config

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from application.api.v1.points import router
from application.core.configs.config import settings
from application.core.db.connection import connect, disconnect
from application.core.configs.loggers_config import get_logging
from application.core.middlewares.logging import LoggingServerErrorMiddleware
from application.core.errors.exceptions import LogHTTPException
from application.core.errors.handlers import (
    logging_http_exceptions_handler,
    validation_exception_handler
)


logging_config.dictConfig(
    get_logging(settings.LOGS_DIR)
)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json'
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(item) for item in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.add_exception_handler(LogHTTPException, logging_http_exceptions_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_middleware(LoggingServerErrorMiddleware)
app.include_router(router)


@app.on_event('startup')
async def startup():
    await connect()


@app.on_event('shutdown')
async def shutdown():
    await disconnect()
