from db.db_utils import do_query
from constants.constants import SCHEMA_NAME, MOVIE


def svc_get():
    """
    GET service to get all records
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE};"
    result = do_query(sql, {})

    return result


def svc_get_by_id(id):
    """
    GET service to get by ID
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE} WHERE movie_id = %s;"
    params = [id]
    result = do_query(sql, params)

    return result
