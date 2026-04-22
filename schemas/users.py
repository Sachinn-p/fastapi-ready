from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: SecretStr) -> SecretStr:
        # Get raw string for checking, though it remains a SecretStr
        password_raw = v.get_secret_value()
        if not any(char.isdigit() for char in password_raw):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in password_raw):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


