from typing import Optional

from application.core.errors.exceptions import LogHTTPException
from application.core.db.layer import AbstractDatabaseLayer


class UserService:

    def __init__(self, user_id: Optional[str] = None, *, database: AbstractDatabaseLayer) -> None:
        self.user_id = user_id
        self.database = database
        self.model_name = 'users'
        self.balance_model_name = 'balance'
        self.id_key = '_id'

    async def get(self) -> dict:
        user = await self.database.get(self.model_name, {self.id_key: self.user_id})
        balance = await self._get_balance()
        await self._is_user_exists(user)
        return await self._convert_user_object(user, balance)

    async def create(self, params: dict) -> dict:
        user = await self.database.create(self.model_name, params)
        balance = await self.database.create(self.balance_model_name, {
            'user_id': user.get(self.id_key),
            'usd': 0.0,
            'bitcoin': 0.0
        })

        return await self._convert_user_object(user, balance)

    async def update(self, params: dict) -> dict:
        filters = {self.id_key: self.user_id}
        user = await self.database.update(self.model_name, filters, params)
        balance = await self._get_balance()
        return await self._convert_user_object(user, balance)

    async def get_balance(self, cost: Optional[dict]) -> dict:
        await self._is_cost_exists(cost)
        balance = await self._get_balance()
        return await self._get_balance_of_user(balance, cost)

    async def update_balance_usd(self, params: dict) -> Optional[dict]:
        balance = await self._get_balance()
        await self._is_updating_usd_balance_valid(params, balance)

        update_filters = {'user_id': self.user_id}
        update_params = await self._get_updating_usd_balance_params(params, balance)
        await self.database.update(self.balance_model_name, update_filters, update_params)

        return await self.get()

    async def update_balance_bitcoins(self, params: dict, cost: Optional[dict]) -> Optional[dict]:
        balance = await self._get_balance()
        await self._is_updating_bitcoin_balance_valid(params, cost, balance)

        update_filters = {'user_id': self.user_id}
        update_params = await self._get_updating_bitcoin_balance_params(params, cost, balance)
        await self.database.update(self.balance_model_name, update_filters, update_params)

        return await self.get()

    async def _get_balance(self) -> dict:
        return await self.database.get(self.balance_model_name, {'user_id': self.user_id})

    async def _convert_user_object(self, user: dict, balance: dict) -> dict:
        user_id = {'id': str(user.pop(self.id_key, 'none'))}
        user_balance = {
            'bitcoin_amount': balance.get('bitcoin', 0.0),
            'usd_balance': balance.get('usd', 0.0)
        }

        return user | user_balance | user_id

    async def _is_updating_usd_balance_valid(self, params: dict, balance: dict) -> None:
        await self._is_balance_exists(balance)

        if params.get('action') == 'withdraw' and params.get('amount') > balance.get('usd', 0):
            raise LogHTTPException(status=400, detail='Insufficient USD on the balance')

    async def _is_updating_bitcoin_balance_valid(self, params: dict, cost: dict, balance: dict) -> None:
        action = params.get('action')
        amount = params.get('amount')
        action_cost = cost.get('price', 0) * amount

        await self._is_cost_exists(cost)
        await self._is_balance_exists(balance)

        if action == 'buy' and action_cost > balance.get('usd', 0):
            raise LogHTTPException(status=400, detail='Insufficient USD on the balance')

        if action == 'sell' and amount > balance.get('bitcoin', 0):
            raise LogHTTPException(status=400, detail='Insufficient Bitcoins on the balance')

    @staticmethod
    async def _get_balance_of_user(balance: dict, cost: dict) -> dict:
        usd = balance.get('usd', 0)
        bitcoin = balance.get('bitcoin', 0)
        price = cost.get('price', 100)
        return {'total_balance': usd + bitcoin * price}

    @staticmethod
    async def _get_updating_usd_balance_params(params: dict, balance: dict) -> dict:
        action = params.get('action')
        amount = params.get('amount')
        current_amount = balance.get('usd', 0)
        update_params = {'usd': current_amount}

        if action == 'deposit':
            update_params['usd'] = current_amount + amount

        if action == 'withdraw':
            update_params['usd'] = current_amount - amount

        return update_params

    @staticmethod
    async def _get_updating_bitcoin_balance_params(params: dict, cost: dict, balance: dict) -> dict:
        action = params.get('action')
        amount = params.get('amount')
        current_usd = balance.get('usd', 0)
        current_bitcoin = balance.get('bitcoin', 0)
        update_params = {'usd': current_usd, 'bitcoin': current_bitcoin}
        action_cost = cost.get('price') * amount

        if action == 'buy':
            update_params['usd'] = current_usd - action_cost
            update_params['bitcoin'] = current_bitcoin + amount

        if action == 'sell':
            update_params['usd'] = current_usd + action_cost
            update_params['bitcoin'] = current_bitcoin - amount

        return update_params

    @staticmethod
    async def _is_user_exists(user: Optional[dict]) -> None:
        if not user:
            raise LogHTTPException(status=403)

    @staticmethod
    async def _is_cost_exists(cost: Optional[dict]) -> None:
        if not cost:
            raise LogHTTPException(status=424, detail='No information on the cost of bitcoin')

    @staticmethod
    async def _is_balance_exists(balance: Optional[dict]) -> None:
        if not balance:
            raise LogHTTPException(status=424, detail='No balance for this user')
