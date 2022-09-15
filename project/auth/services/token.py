from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from uuid import UUID
import random
import string

from project.auth.models.dto.token import Token
from project.core.config import get_token_settings
from project.auth.exceptions import TokenNotValidatedException


class ITokenService(ABC):
    @abstractmethod
    async def create_access_token(self, payload: dict) -> str:
        """
        :return:
        """

    @abstractmethod
    async def create_refresh_token(self, payload: dict, access_token: str) -> str:
        """
        :param payload:
        :param access_token:
        :return:
        """

    @abstractmethod
    async def create_new_token(self, user_id: str) -> Token:
        """
        :param user_id:
        :return:
        """

    @abstractmethod
    async def refresh_token(self, token: Token) -> Token:
        """
        :param token:
        :return:
        """

    @abstractmethod
    async def authentication(self, token: Token) -> UUID:
        """
        :param token:
        :return:
        """


class TokenService(ITokenService):
    def __init__(self):
        settings = get_token_settings()
        self.access_secret_key = settings.access_secret_key
        self.refresh_secret_key = settings.refresh_secret_key
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_minutes = settings.refresh_token_expire_minutes
        self.algorythm = 'HS256'

    async def create_access_token(self, payload: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        payload.update({'exp': expire})
        token = jwt.encode(
            payload, self.access_secret_key, algorithm=self.algorythm
        )
        return token

    async def create_refresh_token(self, payload: dict, access_token: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.refresh_token_expire_minutes)
        payload.update({'exp': expire})
        token = jwt.encode(
            payload, self.refresh_secret_key, algorithm=self.algorythm, access_token=access_token
        )
        return token

    async def create_new_token(self, user_id: str) -> Token:
        payload = {'id': user_id}
        access_token = await self.create_access_token(payload)
        refresh_token = await self.create_refresh_token(payload, access_token)
        token = Token(access=access_token, refresh=refresh_token)
        return token

    async def refresh_token(self, token: Token) -> Token:
        try:
            payload = jwt.decode(
                token.refresh, self.refresh_secret_key, self.algorythm, access_token=token.access
            )
            token = await self.create_new_token(payload['id'])
        except JWTError or ExpiredSignatureError or JWTClaimsError or KeyError:
            body = {'detail': 'Refresh-Token not validated'}
            raise TokenNotValidatedException(body=body)
        return token

    async def authentication(self, token: Token) -> UUID:
        try:
            payload = jwt.decode(
                token.access, self.access_secret_key, self.algorythm
            )
            user_id = payload['id']
        except JWTError or ExpiredSignatureError or JWTClaimsError or KeyError:
            body = {'detail': 'Access-Token not validated'}
            raise TokenNotValidatedException(body=body)
        return user_id
