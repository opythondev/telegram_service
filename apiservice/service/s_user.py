from database.models.user import UserData, User


class UserService:

    async def create_user(self, user: UserData):
        ...

    async def get_user(self, uid):
        ...


