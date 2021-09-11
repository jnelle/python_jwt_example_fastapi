import time
import uuid

from loguru import logger
from fastapi import APIRouter, status, Response

from .. import user_service, jwt_expire, jwt_secret, jwt_algorithm
from service1.helpers.helpers import check_password, create_access_token, hash_password, refresh_session, verify_access_token
from ..models.auth import AddUserRequest, LoginUserModel, TokenModel, UserModel
from ..models.common import APIResponse


router = APIRouter(prefix="/auth")


@logger.catch
@router.post("/login")
async def login(request: LoginUserModel, response: Response) -> APIResponse:
    """
    email: String (required)\n
    password: String (required)
    """
    user = await user_service.get_by_email(request.email)

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return APIResponse(message="USER_NOT_FOUND")
    else:
        if check_password(user.password, request.password):
            access_token = create_access_token(
                data={"token": user.token}, jwt_expire=jwt_expire, jwt_secret=jwt_secret, jwt_algorithm=jwt_algorithm)
            response.status_code = status.HTTP_200_OK
            return TokenModel(access_token=access_token, token_type="bearer")

        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return APIResponse(message="INVALID_CREDENTAILS")


@logger.catch
@router.post("/add_user")
async def add_user(request: AddUserRequest, response: Response) -> APIResponse:

    decoded_jwt = verify_access_token(request.token, jwt_secret, jwt_algorithm)

    if decoded_jwt:
        request_user = await user_service.get_by_token(decoded_jwt["token"])
        if not request_user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return APIResponse(message="INVALID_TOKEN")
        else:
            if request_user.level == 1 or (
                request_user.level == 2 and request.user.level > 1
            ):
                response.status_code = status.HTTP_403_FORBIDDEN
                return APIResponse(message="NOT_ENOUGH_PERMISSION")

            try:
                await user_service.add(UserModel(
                    name=request.user.name,
                    email=request.user.email,
                    password=hash_password(request.user.password),
                    level=request_user.level,  # user level
                    token=uuid.uuid4().hex,
                    reg_time=time.time(),
                ))
            except:
                response.status_code = status.HTTP_409_CONFLICT
                return APIResponse(message="EMAIL_OR_USERNAME_EXISTS")

            response.status_code = status.HTTP_200_OK
            access_token = await refresh_session(
                decoded_token=decoded_jwt, jwt_secret=jwt_secret, jwt_algorithm=jwt_algorithm, jwt_expire=jwt_expire, user_service=user_service)
            if not access_token:
                access_token = request.token
            return TokenModel(access_token=access_token, token_type="bearer", message="SUCCESS")
