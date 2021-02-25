from motor.motor_asyncio import AsyncIOMotorClient

from application.core.configs.config import settings
from application.core.db.mongodb import db


async def connect() -> None:
    db.client = AsyncIOMotorClient(settings.DATABASE_URL)


async def disconnect() -> None:
    db.client.close()
