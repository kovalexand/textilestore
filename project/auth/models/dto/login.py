from dataclasses import dataclass

from pydantic import BaseModel, Field, EmailStr

from project.auth.models.dto.token import Token


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


@dataclass
class LoginResponse:
    name: str
    token: Token
