from functools import cache

from project.auth.use_case import IAuthUseCase, AuthUseCase
from project.auth.repositories.user import IUserRepository, UserRepository
from project.core.database import session_factory


def get_user_repository() -> IUserRepository:
    repo = UserRepository(db=session_factory)
    return repo


@cache
def get_auth_depend() -> IAuthUseCase:
    user_repo = get_user_repository()
    use_case = AuthUseCase(repo=user_repo)
    return use_case
