from fastapi import APIRouter, Depends

from project.auth.models.dto.login import LoginRequest, LoginResponse
from project.auth.models.dto.refresh import RefreshResponse, RefreshRequest
from project.auth.use_case import IAuthUseCase
from project.auth.dependencies import get_auth_depend
from project.auth.models.dto.registration import RegistrationRequest, RegistrationResponse

auth = APIRouter(prefix="/api/auth")


@auth.post(path="/registration", response_model=RegistrationResponse)
async def registration(request: RegistrationRequest, use_case: IAuthUseCase = Depends(get_auth_depend)):
    return await use_case.registration(request)


@auth.post(path="/login", response_model=LoginResponse)
async def login(request: LoginRequest, use_case: IAuthUseCase = Depends(get_auth_depend)):
    return await use_case.login(request)


@auth.post(path="/refresh_token", response_model=RefreshResponse)
async def refresh_token(request: RefreshRequest, use_case: IAuthUseCase = Depends(get_auth_depend)):
    return await use_case.refresh(request)
