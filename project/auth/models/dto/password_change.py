from dataclasses import dataclass

from pydantic import BaseModel, Field

from project.auth.models.token import Token


class PasswordChangeRequest(BaseModel):
    tokens: Token
    password: str = Field(min_length=6, max_length=20)


@dataclass
class PasswordChangeResponse:
    detail: str
