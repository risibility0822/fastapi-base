"""DB Time."""

import pytz
from datetime import datetime


class TimeProcess:
    """處理時間相關操作."""

    def __init__(self) -> None:
        """Init."""
        pass

    def get_now(self) -> datetime:
        """現在時間

        Returns:
            datetime: 現在時間
        """
        return datetime.now()

    def get_utc_time_now(self) -> datetime:
        """Utc 現在時間

        Returns:
            datetime: utc現在時間
        """
        return datetime.utcnow()

    def get_now_str(self) -> str:
        """現在時間字串

        Returns:
            str: 現在時間字串
        """
        return str(datetime.now())

    def get_utc_now_str(self) -> str:
        """Utc 現在時間字串

        Returns:
            str: Utc 現在時間字串
        """
        return str(datetime.utcnow())

    def get_forever_time(self) -> datetime:
        """最大時間值.

        Returns:
            datetime: 9999/12/31
        """
        return datetime(year=9999, month=12, day=31)

    def utc_into_local(self, utc_time: datetime, timezone_str: str) -> str:
        """Utc時間轉換為本地時間.

        Args:
            utc_time (datetime): UTC 時間。
            timezone_str (str): 目標時區的字符串表示。

        Returns:
            str: 轉換後的本地時間，格式為 "%Y/%m/%d %H:%M:%S"。
        """
        timezo = pytz.timezone(timezone_str)
        utc_timezo = pytz.timezone("UTC")
        utc_dt = utc_timezo.localize(utc_time)
        loc_dt = utc_dt.astimezone(timezo)
        return loc_dt.strftime("%Y/%m/%d %H:%M:%S")
