from fastapi import APIRouter

from application.core.db.layer import MongoDBDatabaseLayer
from services.bitcoin_cost import BitcoinCostService
from services.user import UserService
from application.schemas.balance import (
    TotalBalanceResponseSchema,
    BalanceUpdatingUSDSchema,
    BalanceUpdatingBitcoinSchema,
)
from application.schemas.bitcoin_cost import (
    BitcoinCostUpdatingSchema,
    BitcoinCostResponseSchema,
)
from application.schemas.users import (
    UserUpdatingSchema,
    UserCreationSchema,
    UserResponseSchema,
)


router = APIRouter()


@router.get('/bitcoin', response_model=BitcoinCostResponseSchema, status_code=200)
async def get_bitcoin_cost() -> dict:
    service = BitcoinCostService(database=MongoDBDatabaseLayer())
    return await service.get()


@router.put('/bitcoin', response_model=BitcoinCostResponseSchema, status_code=200)
async def update_bitcoin_cost(params: BitcoinCostUpdatingSchema) -> dict:
    service = BitcoinCostService(database=MongoDBDatabaseLayer())
    return await service.update(params.dict())


@router.post('/users', response_model=UserResponseSchema, status_code=200)
async def create_user(params: UserCreationSchema) -> dict:
    service = UserService(database=MongoDBDatabaseLayer())
    return await service.create(params.dict())


@router.get('/users/{user_id}', response_model=UserResponseSchema, status_code=200)
async def get_user(user_id: str) -> dict:
    service = UserService(user_id=user_id, database=MongoDBDatabaseLayer())
    return await service.get()


@router.put('/users/{user_id}', response_model=UserResponseSchema, status_code=200)
async def update_user(user_id: str, params: UserUpdatingSchema) -> dict:
    service = UserService(user_id=user_id, database=MongoDBDatabaseLayer())
    return await service.update(params.dict())


@router.get('/users/{user_id}/balance', response_model=TotalBalanceResponseSchema, status_code=200)
async def get_user_balance(user_id: str) -> dict:
    user_service = UserService(user_id=user_id, database=MongoDBDatabaseLayer())
    bitcoin_cost_service = BitcoinCostService(database=MongoDBDatabaseLayer())
    cost = await bitcoin_cost_service.get()
    return await user_service.get_balance(cost)


@router.post('/users/{user_id}/usd', response_model=UserResponseSchema, status_code=200)
async def update_user_usd(user_id: str, params: BalanceUpdatingUSDSchema) -> dict:
    service = UserService(user_id=user_id, database=MongoDBDatabaseLayer())
    return await service.update_balance_usd(params.dict())


@router.post('/users/{user_id}/bitcoin', response_model=UserResponseSchema, status_code=200)
async def update_user_bitcoin(user_id: str, params: BalanceUpdatingBitcoinSchema) -> dict:
    user_service = UserService(user_id=user_id, database=MongoDBDatabaseLayer())
    bitcoin_cost_service = BitcoinCostService(database=MongoDBDatabaseLayer())
    cost = await bitcoin_cost_service.get()
    return await user_service.update_balance_bitcoins(params.dict(), cost)
