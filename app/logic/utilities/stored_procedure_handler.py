import pyodbc
import json
from app import log
from app.schema.base_response import BaseSPResponse
from app.config.stored_procedure_mapping import StoredProcedureMapping
from app.logic.core.db_manager import use_with_create_connection


class StoredProcedureHandler:
    """Stored Procedure Handler"""

    def __init__(self, connection: pyodbc.Connection):
        """初始化

        Args:
            connection (pyodbc.Connection): DB 連線
        """
        self.connection = connection

    def execute(self, sp_name: str, params: dict = {}) -> BaseSPResponse:
        """執行 Stored Procedure

        ※ 若有輸入參數, 例如: @@DRIVERID VARCHAR(20)
        則需在 params 中加入所有輸入參數
        例如: params = {"DRIVERID": "T123"}

        ※ 若有輸出參數, 例如: @O_MSG VARCHAR(200) OUTPUT
        則需在 params 中加入 outparam 參數, 並將所有輸出參數包含在內
        例如: params = {"outparam": {"O_MSG": ""}}

        Args:
            sp_name (str): SP 名稱
            params (dict, optional): SP 所需參數. Defaults to {}.
                ※ outparam (dict): 輸出參數

        Raises:
            Error: 執行 SP 錯誤
            ex: 執行 SP 錯誤

        Returns:
            BaseSPResponse: SP 執行結果
        """
        try:
            result_set = []
            output_params = params.pop("outparam", {})
            input_params = params

            sql = self.build_sql(sp_name, input_params, output_params)

            cursor = self.connection.cursor()
            cursor.execute(sql)

            if cursor.description:
                result_set = self.fetchall_as_dict(cursor)

                if output_params and result_set[0].keys() == output_params.keys():
                    output_params = result_set[0]
                    cursor.close()
                    return BaseSPResponse(result_set=[], output_parameters=output_params)

                elif output_params:
                    cursor.nextset()
                    output_params_result = self.fetchall_as_dict(cursor)
                    output_params = output_params_result[0]

                cursor.close()
                return BaseSPResponse(result_set=result_set, output_parameters=output_params)

            else:
                raise pyodbc.Error("SP 執行完成，但沒有收到任何回傳資料。")

        except pyodbc.Error as ex:
            log.critical(f"Stored Procedure 執行錯誤 [{sp_name}] {json.dumps(params)}")
            self.connection.rollback()
            raise ex

    def build_sql(self, sp_name: str, input_params: dict, output_params: dict) -> str:
        """建構完整的 SQL 語句, 且支援多個輸入參數與輸出參數

        回傳範例:
            DECLARE @O_MSG nvarchar(max);
            EXEC [dbo].[SP_TEST] @O_MSG = @O_MSG OUTPUT, @DRIVERID = 'T123';
            SELECT @O_MSG AS O_MSG;

        Args:
            sp_name (str): SP 名稱
            input_params (dict): 輸入參數
            output_params (dict): 輸出參數

        Returns:
            str: SQL 語句
        """
        # DECLARE statement
        declare_stmt = ""
        if output_params:
            declare_stmt = ", ".join([f"@{key} nvarchar(max)" for key in output_params.keys()])
            declare_stmt = f"DECLARE {declare_stmt};"

        # EXEC statement
        input_stmt = ""
        output_stmt = ""

        if input_params:
            input_stmt = ", ".join(
                [
                    f"@{key} = '{value}'" if value is not None else f"@{key} = NULL"
                    for key, value in input_params.items()
                ]
            )
        if output_params:
            output_stmt = ", ".join([f"@{key} = @{key} OUTPUT" for key in output_params.keys()])

        if input_stmt and output_stmt:
            input_stmt += ", "

        exec_stmt = f"EXEC [dbo].[{sp_name}] {input_stmt}{output_stmt};"

        # SELECT statement
        select_stmt = ""
        if output_params:
            select_stmt = ", ".join([f"@{key} AS {key}" for key in output_params.keys()])
            select_stmt = f"SELECT {select_stmt};"

        # final SQL
        sql = f"{declare_stmt} {exec_stmt} {select_stmt}"
        return sql

    def fetchall_as_dict(self, cursor: pyodbc.Cursor) -> list:
        """將 cursor 結果轉換為 dict, 並以 list 回傳

        Args:
            cursor (pyodbc.Cursor): Cursor

        Returns:
            list: 轉換後的 dict list
        """
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def simple_sp_execution(sp_name: str, params: dict = {}) -> BaseSPResponse:
    """一個簡單的執行 Stored Procedure 的方法

    ※ 若有輸入參數, 例如: @@DRIVERID VARCHAR(20)
    則需在 params 中加入所有輸入參數
    例如: params = {"DRIVERID": "T123"}

    ※ 若有輸出參數, 例如: @O_MSG VARCHAR(200) OUTPUT
    則需在 params 中加入 outparam 參數, 並將所有輸出參數包含在內
    例如: params = {"outparam": {"O_MSG": ""}}

    Args:
        sp_name (str): SP 名稱
        params (dict, optional): SP 所需參數. Defaults to {}.
            ※ outparam (dict): 輸出參數

    Returns:
        BaseSPResponse: SP 執行結果
    """
    db = StoredProcedureMapping[sp_name].db
    with use_with_create_connection(database=db) as connection:
        sp = StoredProcedureHandler(connection)
        sp_result = sp.execute(sp_name, params)

    return sp_result
