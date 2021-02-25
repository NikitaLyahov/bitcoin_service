from enum import Enum
from pydantic import Field

from application.schemas.base import CamelModel


class UpdatingUSDActions(Enum):
    withdraw = 'withdraw'
    deposit = 'deposit'


class UpdatingBitcoinActions(Enum):
    buy = 'buy'
    sell = 'sell'


class BalanceUpdatingUSDSchema(CamelModel):
    action: UpdatingUSDActions
    amount: float = Field(ge=0)

    class Config:
        use_enum_values = True
        schema_extra = {
            'example': {
                'action': 'withdraw',
                'amount': 40.05
            }
        }


class BalanceUpdatingBitcoinSchema(CamelModel):
    action: UpdatingBitcoinActions
    amount: float = Field(ge=0)

    class Config:
        use_enum_values = True
        schema_extra = {
            'example': {
                'action': 'sell',
                'amount': 0.05
            }
        }


class TotalBalanceResponseSchema(CamelModel):
    total_balance: float = Field(ge=0)

    class Config:
        schema_extra = {
            'example': {
                'totalBalance': 1345.5
            }
        }
