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
    async def password_change(self, user: User, password: str) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, _id: str) -> User | None:
        """
        :param _id:
        :return:
        """

    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
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

    async def password_change(self, user: User, password: str) -> User:
        user.password = password
        with self.db() as session:
            session.add(user)
            session.commit()
        return user

    async def find_by_id(self, _id: str) -> User | None:
        with self.db() as session:
            user = session.query(User).filter_by(id=_id).first()
        return user

    async def find_by_email(self, email: str) -> User | None:
        with self.db() as session:
            user = session.query(User).filter_by(email=email).first()
        return user
