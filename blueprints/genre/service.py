"""
Genre table service
"""

from constants.constants import SCHEMA_NAME, GENRE
from db.db_utils import do_query


def get_all():
    """
    Get All records
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{GENRE}"

    result = do_query(sql)
    return result
