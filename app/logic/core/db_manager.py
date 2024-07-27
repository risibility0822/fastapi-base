"""PYODBC DB Manager."""

from app.config.database import DBENV
import pyodbc
from contextlib import contextmanager


def create_connection_string(
    driver: str = "ODBC Driver 18 for SQL Server",
    server: str = DBENV.DB_SERVER.value,
    database: str = DBENV.DB_DATABASE.value,
    username: str = DBENV.DB_USER.value,
    password: str = DBENV.DB_PASSWORD.value,
) -> str:
    """
    Create a connection string for the database.

    Args:
        driver (str): The ODBC driver name.
        server (str): The server name or IP address.
        database (str): The database name.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The formatted connection string.
    """
    return (
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
        f"UID={username};PWD={password};TrustServerCertificate=yes;"
    )


def create_connection(database: str = DBENV.DB_DATABASE.value) -> pyodbc.Connection:
    """
    Create a database connection.

    Args:
        database (str): The database name.

    Yields:
        pyodbc.Connection: The database connection object.

    Raises:
        ex (pyodbc.Error): An error occurred while creating the connection.
    """
    connection_string = create_connection_string(database=database)
    conn = None
    try:
        conn = pyodbc.connect(connection_string)
        yield conn
        conn.commit()
    except pyodbc.Error as ex:
        if conn:
            conn.rollback()
        print(f"An error occurred: {ex}")
        raise ex
    finally:
        if conn:
            conn.close()


@contextmanager
def use_with_create_connection(database: str = DBENV.DB_DATABASE.value) -> pyodbc.Connection:
    """
    Context manager for creating a database connection and using it.

    Args:
        database (str): The database name.

    Returns:
        pyodbc.Connection: The database connection object.
    """
    return create_connection(database=database)
