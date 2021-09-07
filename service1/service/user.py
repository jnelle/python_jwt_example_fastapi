from typing import Optional

from service1.helpers.helpers import load_model
from service1.models.auth import UserModel


class UserService:
    def __init__(self, collection) -> None:
        self.collection = collection

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        user = await self.collection.find_one({"email": email})
        if user:
            return load_model(UserModel, user)

    async def get_by_token(self, token: str) -> Optional[UserModel]:
        user = await self.collection.find_one({"token": token})
        if user:
            return load_model(UserModel, user)

    async def add(self, user: UserModel):
        await self.collection.insert_one(user.dict())

    async def refresh_session(self, token: str, new_token: str) -> None:
        user = await self.collection.find_one({"token": token})
        user["token"] = new_token
        await self.collection.update_one({"token": token}, {"$set": user})
