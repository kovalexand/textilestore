from dataclasses import dataclass

from pydantic import BaseModel

from project.auth.models.token import Token


class RefreshRequest(BaseModel):
    tokens: Token


@dataclass
class RefreshResponse:
    tokens: Token
