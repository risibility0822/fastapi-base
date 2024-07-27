from fastapi.security import OAuth2PasswordRequestForm
from app.schema.auth import PayloadDataSchema, LoginOutputSchema
from app.logic.utilities.time_process import TimeProcess
from app.logic.utilities.jwt_handler import JWTHandler


jwt = JWTHandler()


class AuthLogic:
    """登入及權限驗證"""

    def login(self, data: OAuth2PasswordRequestForm) -> LoginOutputSchema:
        """登入驗證

        若登入成功，回傳 token
        若登入失敗，回傳 401 Unauthorized

        Args:
            data (OAuth2PasswordRequestForm): 登入資料

        Returns:
            PayloadSchema: token

        Raises:
            credentials_exception: 401 Unauthorized 登入失敗
        """
        user_name = data.username
        password = data.password

        if len(user_name) > 0 and password == "JCTech":
            result = {"user_name": user_name}
            jwt_token = jwt.generate_payload(
                PayloadDataSchema(
                    token_time=TimeProcess().get_now_str(),
                    user_info=result,
                    token_expire_minutes=jwt.expire_minutes,
                    re_token_expire_minutes=jwt.re_expire_minutes,
                )
            )
            return LoginOutputSchema(**result, **jwt_token.model_dump())
        else:
            raise jwt.credentials_exception
