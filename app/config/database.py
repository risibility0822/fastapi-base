"""取得env之DB連線字串."""

import os
from enum import Enum
import dotenv

dotenv.load_dotenv()


class DBENV(Enum):
    """DB connection.

    Attributes:
        DB_SERVER: DB Server
        DB_DATABASE: DB Name
        DB_USER: DB User
        DB_PASSWORD: DB Password
        DB_FIX_DB1: DB1
        DB_FIX_DB2: DB2

    """

    DB_SERVER = os.getenv("DB_SERVER", "")
    DB_DATABASE = os.getenv("DB_DATABASE", "LIMO")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_FIX_DB1 = "DB1"
    DB_FIX_DB2 = "DB2"
