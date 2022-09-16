from dataclasses import dataclass

from pydantic import BaseModel

from project.auth.models.token import Token


class UserInfoRequest(BaseModel):
    tokens: Token


@dataclass
class UserInfoResponse:
    name: str
    email: str
    is_verified: bool
