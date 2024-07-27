from enum import Enum
from app.config.database import DBENV

db1 = DBENV.DB_FIX_DB1.value
db2 = DBENV.DB_FIX_DB2.value


class StoredProcedureMapping(Enum):
    """Stored procedure 名稱與DB對應

    [使用方式]
    取得SP名稱: StoredProcedureMapping.SP_FAKE1.name
    取得對應的DB名稱: StoredProcedureMapping.SP_FAKE1.db

    Attributes:
        SP_FAKE1: 假的SP 1
        SP_FAKE2: 假的SP 2
        name: SP名稱
        db: SP所對應的DB名稱

    """

    SP_FAKE1 = ("SP_FAKE1", db1)
    SP_FAKE2 = ("SP_FAKE2", db2)

    @property
    def name(self) -> str:
        """SP名稱"""
        return self.value[0]

    @property
    def db(self) -> str:
        """SP所對應的DB名稱"""
        return self.value[1]
