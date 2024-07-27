from fastapi import Request, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app import log
from app.schema.auth import PayloadSchema, LoginOutputSchema, PayloadDataSchema
from app.schema.base_response import BaseAPIResponse
from app.logic.auth import AuthLogic
from app.logic.utilities.jwt_handler import JWTHandler


jwt = JWTHandler()
router = APIRouter()


@router.post(
    "/login",
    description="登入",
    response_model=LoginOutputSchema,
)
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends()) -> LoginOutputSchema:
    """登入.

    Args:
        request (Request): Request
        data (LoginInputSchema): 登入資訊

    Raises:
        ex: _description_

    Returns:
        BaseAPIResponse: BaseAPIResponse
    """
    try:
        return AuthLogic().login(data)
    except Exception as ex:
        log.critical(ex, exc_info=True)
        raise ex


@router.post(
    "/refresh_token",
    description="更新 token",
    response_model=PayloadSchema,
)
def refresh_token(request: Request, payload: PayloadSchema = Depends(jwt.refresh_token)) -> PayloadSchema:
    """更新 token.

    Args:
        request (Request): Request
        payload (dict): Token資料

    Raises:
        credentials_exception (Exception): 401 Unauthorized

    Returns:
        PayloadSchema: PayloadSchema
    """
    try:
        return payload
    except Exception as ex:
        log.critical(ex, exc_info=True)
        raise jwt.credentials_exception


@router.get(
    "/say_my_name",
    description="我的名字",
    response_model=BaseAPIResponse,
)
def say_my_name(request: Request, payload: PayloadDataSchema = Depends(jwt.verify_token)) -> BaseAPIResponse:
    """我的名字.

    Args:
        request (Request): Request
        payload (PayloadDataSchema): Token資料

    Returns:
        BaseAPIResponse: API 結果
    """
    try:
        return BaseAPIResponse(success=True, data=payload.user_info, message="Hello, " + payload.user_info["user_name"])
    except Exception as ex:
        log.critical(ex, exc_info=True)
