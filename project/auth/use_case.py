import uuid
import hashlib
from abc import ABC, abstractmethod

from project.auth.exceptions import UserDoesNotExistException
from project.auth.models.dto.login import LoginRequest, LoginResponse
from project.auth.models.entities import User
from project.auth.models.dto.registration import RegistrationRequest, RegistrationResponse
from project.auth.repositories.user import IUserRepository
from project.auth.services.token import ITokenService


class IAuthUseCase(ABC):
    @abstractmethod
    async def registration(self, request: RegistrationRequest) -> RegistrationResponse:
        """
        :param request:
        :return:
        """

    @abstractmethod
    async def login(self, request: LoginRequest) -> LoginResponse:
        """
        :param request:
        :return:
        """


class AuthUseCase(IAuthUseCase):
    def __init__(self, repo: IUserRepository, token: ITokenService):
        self.repo = repo
        self.token_service = token

    @staticmethod
    def get_hashed_password(password: str, salt: str) -> str:
        return hashlib.sha512((password + salt).encode()).hexdigest()

    @staticmethod
    def validate_password(password: str, salt: str, hashed_password: str) -> bool:
        return True if hashlib.sha512((password + salt).encode()).hexdigest() == hashed_password else False

    async def registration(self, request: RegistrationRequest) -> RegistrationResponse:
        salt = uuid.uuid4().hex
        password = self.get_hashed_password(request.password, salt)
        user = User(name=request.name, email=request.email, password=password, key=salt)
        await self.repo.create(user)
        return RegistrationResponse(name=request.name)

    async def login(self, request: LoginRequest) -> LoginResponse:
        user = await self.repo.get_user(request.email)
        if not user or not self.validate_password(request.password, user.key, user.password):
            exp_body = {'detail': 'email or password uncorrected'}
            raise UserDoesNotExistException(body=exp_body)
        token = await self.token_service.create_new_token(user_id=str(user.id))
        return LoginResponse(name=str(user.name), access_token=token.access_token, refresh_token=token.refresh_token)
