from dataclasses import dataclass

from project.core.exceptions import ApplicationException


@dataclass
class UserNotValidatedException(ApplicationException):
    code_status: int = 409


@dataclass
class EmailAlreadyExistException(ApplicationException):
    code_status: int = 409


@dataclass
class UserDoesNotExistException(ApplicationException):
    code_status: int = 404


@dataclass
class TokenNotValidatedException(ApplicationException):
    code_status: int = 401
