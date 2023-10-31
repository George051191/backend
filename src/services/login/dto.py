from typing import Optional

from pydantic import BaseModel, Field


class LoginRequestDTO(BaseModel):
    email: str
    password: str


class LoginResponseDTO(BaseModel):
    jwt_token: str


class RegisterRequestDTO(BaseModel):
    email: str #TODO: add phone login
    password: str


class RegisterResponseDTO(BaseModel):
    jwt_token: str = Field(serialization_alias="jwtToken")


class VerifyEmailRequestDTO(BaseModel):
    code: Optional[str | int] = None
    resend: Optional[bool] = False


class VerifyEmailResponseDTO(BaseModel):
    success: bool

class ChangePasswordRequestDTO(BaseModel):
    old_password: str = Field(alias="oldPassword")
    new_password: str = Field(alias="newPassword")