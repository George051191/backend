from typing import Annotated

import fastapi

import src.services.login.dto as dto
from src.database import Database
from src.services.login.dependencies import JWTBearer
from src.utils import check_password, JWTAbc

router = fastapi.APIRouter()


@router.post(
    "/login",
    response_model=dto.LoginResponseDTO,
    tags=["login"],
    summary="Login existing user",
)
async def login(
    data: dto.LoginRequestDTO,
    jwt: Annotated[JWTAbc, fastapi.Depends()] = None,
    db: Annotated[Database, fastapi.Depends()] = None,
):
    check = await db.user_login(data.email, data.password)
    if not check:
        raise fastapi.HTTPException(400, {"message": "Invalid credentials"})
    return dto.RegisterResponseDTO(jwt_token=jwt.encode({"id": 1, "email": data.email}))


@router.post(
    "/register",
    response_model=dto.RegisterResponseDTO,
    tags=["login"],
    summary="Register new user",
    responses={
        200: {
            "model": dto.RegisterResponseDTO,
            "description": "User registered successfully",
        },
    },
)
async def register(
    data: dto.RegisterRequestDTO,
    jwt: Annotated[JWTAbc, fastapi.Depends()] = None,
    db: Annotated[Database, fastapi.Depends()] = None,
):
    check = await db.get_user_by_email(data.email)
    if check:
        raise fastapi.HTTPException(409, {"message": "User already exists"})
    if not check_password(data.password):
        raise fastapi.HTTPException(
            400, {"message": "Password does not match requirements"}
        )
    user = await db.create_user(
        data.email, data.password
    )
    return dto.RegisterResponseDTO(
        jwt_token=jwt.encode(
            {"role": user.role, "email": user.email}
        )
    )


# @router.post(
#     "/verify-email",
#     response_model=dto.VerifyEmailResponseDTO,
#     tags=["login"],
#     summary="Verify email for new users",
# )
# async def verify_email(
#         data: dto.VerifyEmailRequestDTO, jwt: Annotated[JWTAbc, fastapi.Depends()] = None
# ):
#     if data.code:
#         check = ...  # check code
#         if not check:
#             raise fastapi.HTTPException(400, "Invalid code")
#         return {"success": True}
#     elif data.resend:
#         check = ...  # check if some time has passed since last email
#         if not check:
#             raise fastapi.HTTPException(400, "Too soon to resend")
#         return {"success": True}
#     else:
#         raise fastapi.HTTPException(400, "Invalid request")

@router.patch("/change-password", tags=["login"], summary="Change password", dependencies=[fastapi.Depends(JWTBearer(

))])
async def change_password(
    data: dto.ChangePasswordRequestDTO,
    db: Annotated[Database, fastapi.Depends()] = None,
    request: fastapi.Request = None,
):
    check = await db.user_login(request.state.user["email"], data.old_password)
    if not check:
        raise fastapi.HTTPException(400, {"message": "Invalid credentials"})
    if not check_password(data.new_password):
        raise fastapi.HTTPException(
            400, {"message": "Password does not match requirements"}
        )
    user = await db.get_user_by_email(request.state.user["email"])
    await db.change_password(user, data.new_password)
    return {"success": True}