from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    username: str
    email: EmailStr
    role: str
    level: int
    rating: int
    created_at: datetime

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )
