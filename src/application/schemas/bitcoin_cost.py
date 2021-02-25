from datetime import datetime

from pydantic import (
    Field,
    validator,
)

from application.schemas.base import CamelModel


class BitcoinCostUpdatingSchema(CamelModel):
    price: float = Field(ge=0)
    updated_at: datetime = None

    @validator('updated_at', pre=True, always=True)
    def default_modified(cls, v, values):
        return v or datetime.now()

    class Config:
        schema_extra = {
            'example': {
                'price': 100.0
            }
        }


class BitcoinCostResponseSchema(CamelModel):
    price: float = Field(ge=0)
    updated_at: datetime

    class Config:
        schema_extra = {
            'example': {
                'price': 100.0,
                'updatedAt': '2021-01-04T00:12:01.000Z'
            }
        }
