from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from project.auth.models.token import Token
from project.core.config import get_token_settings
from project.auth.exceptions import TokenNotValidatedException


class ITokenService(ABC):
    @abstractmethod
    async def create(self, qualifier: str) -> Token:
        """
        :param qualifier:
        

        :return:
        """

    @abstractmethod
    async def refresh(self, token: Token) -> Token:
        """
        :param token:
        :return:
        """

    @abstractmethod
    async def authentication(self, token: Token) -> str:
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

    async def create(self, qualifier: str) -> Token:
        access_expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        access_payload = {'id': qualifier, 'exp': access_expire}
        refresh_expire = datetime.utcnow() + timedelta(minutes=self.refresh_token_expire_minutes)
        refresh_payload = {'id': qualifier, 'exp': refresh_expire}
        access = jwt.encode(
            access_payload, self.access_secret_key, algorithm=self.algorythm
        )
        refresh = jwt.encode(
            refresh_payload, self.refresh_secret_key, algorithm=self.algorythm, access_token=access
        )
        return Token(access=access, refresh=refresh)

    async def refresh(self, token: Token) -> Token:
        try:
            payload = jwt.decode(
                token.refresh, self.refresh_secret_key, self.algorythm, access_token=token.access
            )
            token = await self.create(qualifier=payload['id'])
        except JWTError or ExpiredSignatureError or JWTClaimsError or KeyError:
            body = {'detail': 'Refresh-Token not validated'}
            raise TokenNotValidatedException(body=body)
        return token

    async def authentication(self, token: Token) -> str:
        try:
            payload = jwt.decode(token.access, self.access_secret_key, self.algorythm)
            _id = payload['id']
        except JWTError or ExpiredSignatureError or JWTClaimsError or KeyError:
            body = {'detail': 'Access-Token not validated'}
            raise TokenNotValidatedException(body=body)
        return _id
