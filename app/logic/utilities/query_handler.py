from typing import List, Dict, Iterable, Optional, Type
from sqlalchemy.engine.row import RowProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.inspection import inspect

Base = declarative_base()


def model_to_dict(model_instance: Optional[Type[Base]]) -> Optional[Dict]:  # type: ignore
    """Convert a single SQLAlchemy ORM model instance to a dictionary.

    Args:
        model_instance (Optional[Base]): The instance of a SQLAlchemy ORM model or None

    Returns:
        Optional[Dict]: A dictionary representing the model data or None if input is None
    """
    if model_instance is None:
        return None

    return {c.key: getattr(model_instance, c.key) for c in inspect(model_instance).mapper.column_attrs}


def row_to_dict_list(query_result: Iterable[RowProxy]) -> List[Dict]:
    """Convert SQLAlchemy query result to a list of dictionaries.

    Args:
        query_result (Iterable[RowProxy]): The result of a SQLAlchemy query

    Returns:
        List[Dict]: A list of dictionaries, each representing a row from the query
    """
    # Initialize an empty list to hold dictionaries
    dict_list = []

    # Iterate through the query result
    for row in query_result:
        # Convert each row to a dictionary
        row_dict = {column: getattr(row, column) for column in row.keys()}
        # Append the dictionary to the list
        dict_list.append(row_dict)

    return dict_list
