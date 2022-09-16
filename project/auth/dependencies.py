from functools import cache

from project.auth.services.token import ITokenService, TokenService
from project.auth.use_case import IAuthUseCase, AuthUseCase
from project.auth.repositories.user import IUserRepository, UserRepository
from project.core.database import session_factory


def get_user_repository() -> IUserRepository:
    repo = UserRepository(db=session_factory)
    return repo


def get_token_service() -> ITokenService:
    service = TokenService()
    return service


@cache
def get_auth_depend() -> IAuthUseCase:
    user = get_user_repository()
    token = get_token_service()
    use_case = AuthUseCase(user=user, token=token)
    return use_case
