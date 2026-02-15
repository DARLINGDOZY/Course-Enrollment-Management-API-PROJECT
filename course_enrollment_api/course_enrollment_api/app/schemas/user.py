from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal

class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: Literal["student", "admin"]

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
