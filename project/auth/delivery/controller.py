from fastapi import APIRouter, Depends

from project.auth.models.dto.login import LoginRequest, LoginResponse
from project.auth.models.dto.password_change import PasswordChangeResponse, PasswordChangeRequest
from project.auth.models.dto.refresh import RefreshResponse, RefreshRequest
from project.auth.models.dto.send_verify_link import SendVerifyLinkResponse, SendVerifyLinkRequest
from project.auth.models.dto.user_info import UserInfoResponse, UserInfoRequest
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


@auth.post(path="/password_change", response_model=PasswordChangeResponse)
async def password_change(request: PasswordChangeRequest, use_case: IAuthUseCase = Depends(get_auth_depend)):
    return await use_case.password_change(request)


@auth.post(path="/user_info", response_model=UserInfoResponse)
async def get_user_info(request: UserInfoRequest, use_case=Depends(get_auth_depend)):
    return await use_case.get_user_info(request)


@auth.post(path="/send_verify_link", response_model=SendVerifyLinkResponse)
async def send_verify_link(request: SendVerifyLinkRequest, use_case=Depends(get_auth_depend)):
    return await use_case.send_verify_link(request)
