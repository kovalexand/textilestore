import uuid
import hashlib
from abc import ABC, abstractmethod

from project.auth.models.entities import User
from project.auth.models.dto.registration import RegistrationRequest, RegistrationResponse
from project.auth.repositories.user import IUserRepository


class IAuthUseCase(ABC):
    @abstractmethod
    async def registration(self, request: RegistrationRequest) -> RegistrationResponse:
        """
        :param request:
        :return:
        """


class AuthUseCase(IAuthUseCase):
    def __init__(self, repo: IUserRepository):
        self.repo = repo

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
