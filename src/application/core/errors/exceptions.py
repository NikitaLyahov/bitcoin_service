from typing import Dict, Union

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class LogHTTPException(HTTPException):
    def __init__(self,
                 status: int = HTTP_400_BAD_REQUEST,
                 detail: Union[Dict, str] = None) -> None:
        super().__init__(status_code=status, detail=detail)
