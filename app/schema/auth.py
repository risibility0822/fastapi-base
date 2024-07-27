from pydantic import BaseModel
from typing import Optional


class RefreshTokenSchema(BaseModel):
    """更新Token

    Attributes:
        refreshed_access_token (str): 更新後的 access token
    """

    refreshed_access_token: str


class PayloadDataSchema(BaseModel):
    """Payload Token 所搭載的資料

    Attributes:
        token_time (str): token 產生時間
        user_info (UserInfoSchema): 已登入的使用者資訊
        token_expire_minutes (int): token 有效時間(分鐘)
        re_token_expire_minutes (int): refresh token 有效時間(分鐘)
    """

    token_time: str
    user_info: dict
    token_expire_minutes: int
    re_token_expire_minutes: int


class PayloadSchema(BaseModel):
    """Payload

    Attributes:
        access_token (str): access token
        refresh_token (Optional[str]): refresh token
        token_type (str): token 類型
    """

    access_token: str
    refresh_token: Optional[str] = ""
    token_type: str = "bearer"


class LoginOutputSchema(BaseModel):
    """SP_DRIVERAPP_LOGIN Output

    Attributes:
        access_token (str): access token
        refresh_token (Optional[str]): refresh token
        token_type (str): token 類型
    """

    access_token: str
    refresh_token: Optional[str] = ""
    token_type: str = "bearer"
