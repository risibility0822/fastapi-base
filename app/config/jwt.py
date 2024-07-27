import os
import dotenv
from enum import Enum

dotenv.load_dotenv()


class JWTEnvs(Enum):
    """JWT Token

    To get a string like JWT_SECRET_KEY, run:
    > openssl rand -hex 32

    Attributes:
        JWT_ALGORITHM: 演算法
        JWT_SECRET_KEY: Token secret key
        JWT_EXPIRE_MINUTES: Token 過期分鐘
        JWT_RE_SECRET_KEY: Refresh Token secret key
        JWT_RE_EXPIRE_MINUTES: Refresh Token 過期分鐘
    """

    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_EXPIRE_MINUTES = os.getenv("JWT_EXPIRE_MINUTES", "0")
    JWT_RE_SECRET_KEY = os.getenv("JWT_RE_SECRET_KEY")
    JWT_RE_EXPIRE_MINUTES = os.getenv("JWT_RE_EXPIRE_MINUTES", "0")
