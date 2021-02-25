import secrets
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    API_V1_STR: str = '/API_V1_STR'
    SECRET_KEY: str = secrets.token_urlsafe(32)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str = 'Bitcoin Service'

    DATABASE_URL: Optional[str] = None
    MONGO_INITDB_DATABASE: Optional[str] = None

    BASE_DIR: Path = Path(__file__).parent.parent.parent.parent
    LOGS_DIR: Path = None

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator('LOGS_DIR', pre=True)
    def create_logs_dir(cls, v: Optional[Path], values: Dict[str, Any]) -> Path:
        if v is not None:
            log_dir = Path(v)
        else:
            log_dir = values['BASE_DIR'].joinpath('logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    class Config:
        case_sensitive = True


settings = Settings()
