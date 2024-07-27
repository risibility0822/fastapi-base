"""取得env之Host連線字串."""

import os
from enum import Enum
import dotenv

dotenv.load_dotenv()


class HOSTENV(Enum):
    """Host Url .

    Attributes:
        HOST_URL: Host Url
    """

    HOST_URL = os.getenv("HOST_URL", "")
