from app import log
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config.jwt import JWTEnvs
from app.schema.auth import PayloadDataSchema, PayloadSchema
from app.logic.utilities.time_process import TimeProcess


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


class JWTHandler:
    """JWT Token 處理"""

    def __init__(self) -> None:
        """初始化"""
        self.token_fields = {"user_name"}
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"Authorization": "Bearer"},
        )

        self.algorithm = JWTEnvs.JWT_ALGORITHM.value
        self.secret_key = JWTEnvs.JWT_SECRET_KEY.value
        self.expire_minutes = int(JWTEnvs.JWT_EXPIRE_MINUTES.value)
        self.re_secret_key = JWTEnvs.JWT_RE_SECRET_KEY.value
        self.re_expire_minutes = int(JWTEnvs.JWT_RE_EXPIRE_MINUTES.value)

    def create_token(self, data: dict, is_access_token: bool = True) -> str:
        """產生 Token

        Args:
            data (dict): 放入Token的資料
            is_access_token (bool, optional): Token類型識別, True: Access Token, False: Refresh Token. 預設為 True.

        Returns:
            str: Token
        """
        raw_data = data.copy()

        if is_access_token:
            expire = datetime.now() + timedelta(minutes=int(self.expire_minutes))
            raw_data.update({"exp": expire})
            encoded_jwt = jwt.encode(raw_data, self.secret_key, algorithm=self.algorithm)
        else:
            expire = datetime.now() + timedelta(minutes=int(self.re_expire_minutes))
            raw_data.update({"exp": expire})
            encoded_jwt = jwt.encode(raw_data, self.re_secret_key, algorithm=self.algorithm)

        return encoded_jwt

    def verify_token(self, request: Request, access_token: str = Depends(oauth2_scheme)) -> PayloadDataSchema:
        """驗證 Token

        Args:
            request (Request): 請求物件
            access_token (str, optional): Access Token, 預設為 Depends(oauth2_scheme)

        Raises:
            credentials_exception: 驗證失敗

        Returns:
            PayloadDataSchema: Token資料
        """
        try:
            payload = jwt.decode(access_token, self.secret_key, algorithms=[self.algorithm])

            # if not (self.token_fields == set(payload["user_info"].keys())):
            #     raise self.credentials_exception

            return PayloadDataSchema(**payload)
        except JWTError as ex:
            log.critical(ex, exc_info=True)
            raise self.credentials_exception

    def refresh_token(self, refresh_token: str = Depends(oauth2_scheme)) -> PayloadSchema:
        """驗證 Token

        Args:
            refresh_token (str, optional): Refresh Token, 預設為 Depends(oauth2_scheme)

        Raises:
            credentials_exception: 驗證失敗

        Returns:
            PayloadSchema: Token資料
        """
        try:
            payload = jwt.decode(refresh_token, self.re_secret_key, algorithms=[self.algorithm])

            if not (self.token_fields == set(payload["user_info"].keys())):
                raise self.credentials_exception

            refreshed_payload = self.generate_payload(
                PayloadDataSchema(
                    token_time=TimeProcess().get_now_str(),
                    user_info=payload["user_info"],
                    token_expire_minutes=self.expire_minutes,
                    re_token_expire_minutes=self.re_expire_minutes,
                ),
                with_refresh_token=False,
            )

            return refreshed_payload
        except JWTError as ex:
            log.critical(ex, exc_info=True)
            raise self.credentials_exception

    def generate_payload(self, data: PayloadDataSchema, with_refresh_token: bool = True) -> PayloadSchema:
        """產生 Payload

        Args:
            data (PayloadDataSchema): Payload所搭載的資料
            with_refresh_token (bool, optional): 是否連同產生 Refresh Token. 預設為 True.

        Raises:
            ex: _description_

        Returns:
            PayloadSchema: Payload
        """
        try:
            if with_refresh_token:
                result = PayloadSchema(
                    access_token=self.create_token(data.model_dump(), is_access_token=True),
                    refresh_token=self.create_token(data.model_dump(), is_access_token=False),
                )
            else:
                result = PayloadSchema(
                    access_token=self.create_token(data.model_dump(), is_access_token=True),
                )
            return result
        except Exception as ex:
            log.critical(ex, exc_info=True)
            raise ex
