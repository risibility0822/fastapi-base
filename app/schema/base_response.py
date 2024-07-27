"""Base api response."""

from typing import Any
from pydantic import BaseModel


class BaseAPIResponse(BaseModel):
    """API 回傳資料結構

    Attributes:
        success: 成功 or 失敗
        message: 回傳訊息
        data: 回傳的結構, 可能為任何結構的資料, 或甚至是不需回傳資料(None)
    """

    success: bool = False  # 成功 or 失敗
    message: str = ""  # 回傳訊息
    data: Any = None


class BaseSPResponse(BaseModel):
    """Stored Procedure 回傳資料結構

    Attributes:
        result_set (list): 回傳資料
        output_parameters (dict): 輸出參數
    """

    result_set: list = []
    output_parameters: dict = {}


class BaseSPAPIResponse(BaseAPIResponse):
    """Stored Procedure API 回傳資料結構

    Attributes:
        data (BaseSPResponse): SP的回傳資料結構
    """

    data: BaseSPResponse = BaseSPResponse()
