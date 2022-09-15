from dataclasses import dataclass

from pydantic import BaseModel

from project.auth.models.dto.token import Token


class RefreshRequest(BaseModel):
    token: Token


@dataclass
class RefreshResponse:
    token: Token
