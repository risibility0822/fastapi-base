"""取得env之AzureFileStorage連線字串."""

import os
from enum import Enum
import dotenv


dotenv.load_dotenv()


class AFSENV(Enum):
    """Azure File Storage env.

    Attributes:
        CONNECTION_STRING: 預設的 AFS 連線字串
        SHARE_NAME: MongoDB 連線字串
        QR_CODE_SHARE_NAME: QR code share name
    """

    CONNECTION_STRING = os.getenv("AFS_CONNECTION_STRING")
    SHARE_NAME = os.getenv("AFS_SHARE_NAME")
    QR_CODE_SHARE_NAME = os.getenv("AFS_QR_CODE_SHARE_NAME", "qr-code")
