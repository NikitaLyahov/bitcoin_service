from typing import Optional
from datetime import datetime

from pydantic import (
    EmailStr,
    validator,
    Field,
)

from application.schemas.base import CamelModel


class UserCreationSchema(CamelModel):
    name: str
    username: str
    email: EmailStr
    created_at: datetime = None
    updated_at: datetime = None

    @validator('created_at', pre=True, always=True)
    def default_created(cls, v):
        return v or datetime.now()

    @validator('updated_at', pre=True, always=True)
    def default_modified(cls, v, values):
        return v or values['created_at']

    class Config:
        schema_extra = {
            'example': {
                'name': 'John Doe',
                'username': 'john_doe',
                'email': 'jdoe@x.edu.ng'
            }
        }


class UserUpdatingSchema(CamelModel):
    name: Optional[str]
    email: Optional[EmailStr]
    updated_at: datetime = None

    @validator('updated_at', pre=True, always=True)
    def default_modified(cls, v, values):
        return v or datetime.now()

    class Config:
        schema_extra = {
            'example': {
                'name': 'John Doe',
                'email': 'jdoe@x.edu.ng'
            }
        }


class UserResponseSchema(CamelModel):
    id: str
    name: str
    username: str
    email: EmailStr
    bitcoin_amount: float = Field(ge=0)
    usd_balance: float = Field(ge=0)
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            'example': {
                'id': 'e0965e3b-d92c-44e7-b79a-6e7c6654c3a8',
                'name': 'John Doe',
                'username': 'john_doe',
                'email': 'jdoe@x.edu.ng',
                'bitcoinAmount': 0.0,
                'usdBalance': 0.0,
                'createdAt': '2021-01-04T00:12:01.000Z',
                'updatedAt': '2021-01-04T00:12:01.000Z'
            }
        }
