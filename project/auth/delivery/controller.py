from fastapi import APIRouter, Depends

from project.auth.models.dto.login import LoginRequest, LoginResponse
from project.auth.use_case import IAuthUseCase
from project.auth.dependencies import get_auth_depend
from project.auth.models.dto.registration import RegistrationRequest, RegistrationResponse

auth = APIRouter()


@auth.post(path="/api/registration", response_model=RegistrationResponse)
async def registration(request: RegistrationRequest, use_case: IAuthUseCase = Depends(get_auth_depend)):
    return await use_case.registration(request)


@auth.post(path="/api/login", response_model=LoginResponse)
async def login(request: LoginRequest, use_case: IAuthUseCase = Depends(get_auth_depend)):
    return await use_case.login(request)
