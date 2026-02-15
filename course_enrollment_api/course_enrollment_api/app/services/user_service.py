from app.storage.datastore import datastore
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        user_id = datastore.user_counter
        new_user = User(
            id=user_id,
            name=user_data.name,
            email=str(user_data.email),
            role=user_data.role
        )
        datastore.users[user_id] = new_user
        datastore.user_counter += 1
        return new_user

    @staticmethod
    def get_all_users():
        return list(datastore.users.values())

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        user = datastore.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
