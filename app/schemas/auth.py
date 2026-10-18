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
