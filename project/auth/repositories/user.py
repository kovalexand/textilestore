from abc import ABC, abstractmethod
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from project.auth.exceptions import EmailAlreadyExistException
from project.auth.models.entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        """
        :return:
        """

    @abstractmethod
    async def get_user(self, email: str) -> User | None:
        """
        :param email:
        :return:
        """


class UserRepository(IUserRepository):
    def __init__(self, db: sessionmaker):
        self.db = db

    async def create(self, user: User) -> User:
        exc_body = {'detail': 'Email already exist'}
        with self.db() as session:
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise EmailAlreadyExistException(body=exc_body)
        return user

    async def get_user(self, email: str) -> User | None:
        with self.db() as session:
            user = session.query(User).filter_by(email=email).first()
        return user
