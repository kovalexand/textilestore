import uuid
import hashlib
from abc import ABC, abstractmethod

from project.auth.exceptions import UserDoesNotExistException
from project.auth.models.dto.login import LoginRequest, LoginResponse
from project.auth.models.dto.password_change import PasswordChangeRequest, PasswordChangeResponse
from project.auth.models.dto.refresh import RefreshRequest, RefreshResponse
from project.auth.models.dto.user_info import UserInfoRequest, UserInfoResponse
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

    @abstractmethod
    async def refresh(self, request: RefreshRequest) -> RefreshResponse:
        """
        :param request:
        :return:
        """

    @abstractmethod
    async def password_change(self, request: PasswordChangeRequest) -> PasswordChangeResponse:
        """
        :param request:
        :return:
        """

    @abstractmethod
    async def get_user_info(self, request: UserInfoRequest) -> UserInfoResponse:
        """
        :param request:
        :return:
        """


class AuthUseCase(IAuthUseCase):
    def __init__(self, user: IUserRepository, token: ITokenService):
        self.user = user
        self.token = token

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
        await self.user.create(user)
        return RegistrationResponse(name=request.name)

    async def login(self, request: LoginRequest) -> LoginResponse:
        user = await self.user.find_by_email(request.email)
        if not user or not self.validate_password(request.password, user.key, user.password):
            exp_body = {'detail': 'email or password uncorrected'}
            raise UserDoesNotExistException(body=exp_body)
        token = await self.token.create(qualifier=str(user.id))
        return LoginResponse(name=str(user.name), tokens=token)

    async def refresh(self, request: RefreshRequest) -> RefreshResponse:
        token = await self.token.refresh(request.tokens)
        return RefreshResponse(tokens=token)

    async def password_change(self, request: PasswordChangeRequest) -> PasswordChangeResponse:
        _id = await self.token.authentication(request.tokens)
        user = await self.user.find_by_id(_id)
        password = self.get_hashed_password(request.password, user.key)
        await self.user.password_change(user, password)
        return PasswordChangeResponse(detail="password is changed")

    async def get_user_info(self, request: UserInfoRequest) -> UserInfoResponse:
        _id = await self.token.authentication(request.tokens)
        user = await self.user.find_by_id(_id)
        name = str(user.name)
        email = str(user.email)
        is_verified = bool(user.is_verified)
        return UserInfoResponse(name=name, email=email, is_verified=is_verified)
