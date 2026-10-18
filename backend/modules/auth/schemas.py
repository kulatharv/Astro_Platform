from datetime import datetime
from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: str = Field(..., min_length=3, max_length=255)
    phone: str = Field(default="", max_length=32)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class AdminLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    email: str


class UserProfileUpdate(BaseModel):
    name: str
    phone: str = ""
    birth_date: str = ""
    birth_time: str = ""
    birth_city: str = ""
    zodiac_sign: str = ""
    notes: str = ""


class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    phone: str | None = None
    birth_date: str | None = None
    birth_time: str | None = None
    birth_city: str | None = None
    zodiac_sign: str | None = None
    notes: str | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    preferred_language: str = "en"
    created_at: datetime
    last_login_at: datetime | None = None
    profile: UserProfileResponse | None = None

    class Config:
        from_attributes = True
