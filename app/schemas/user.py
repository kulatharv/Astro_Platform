from datetime import datetime
from pydantic import BaseModel


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
