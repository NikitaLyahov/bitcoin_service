from typing import Optional


class BitcoinCostService:

    def __init__(self, *, database) -> None:
        self.database = database
        self.model_name = 'bitcoin'
        self.id_key = '_id'

    async def get(self) -> Optional[dict]:
        return await self.database.first(self.model_name)

    async def update(self, params: dict) -> Optional[dict]:
        bitcoin = await self.get()
        filters = {self.id_key: bitcoin.get(self.id_key, '')}
        return await self.database.update(self.model_name, filters, params)
