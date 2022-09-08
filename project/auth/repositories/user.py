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
