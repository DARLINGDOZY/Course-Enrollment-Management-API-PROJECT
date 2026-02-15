from fastapi import APIRouter, status
from typing import List
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    return UserService.create_user(user_data)

@router.get("", response_model=List[UserResponse])
async def get_users():
    return UserService.get_all_users()

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    return UserService.get_user_by_id(user_id)
