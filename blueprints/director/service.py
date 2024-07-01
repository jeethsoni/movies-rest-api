"""Service file for director"""

from db.db_utils import do_query
from constants.constants import DIRECTOR, SCHEMA_NAME


def svc_get():
    """
    A GET service to get all records
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{DIRECTOR};"
    result = do_query(sql, {})

    return result


def svc_get_by_id(director_id):
    """
    A GET service to get by ID
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{DIRECTOR} WHERE director_id = %s;"
    params = [director_id]
    result = do_query(sql, params)

    return result


def svc_post(payload):
    """
    A POST service
    """

    # parameters for the query
    first_name = payload["first_name"]
    last_name = payload["last_name"]

    # SQL statement
    sql = f"INSERT INTO {SCHEMA_NAME}.{DIRECTOR}(first_name, last_name) VALUES (%s, %s) RETURNING *;"
    params = [first_name, last_name]

    result = do_query(sql, params)

    return result


def svc_put(payload, id):
    """
    A PUT service
    """

    first_name = payload["first_name"]
    last_name = payload["last_name"]
    created_at = payload["created_at"]

    # SQL Statement
    sql = f"""
            UPDATE {SCHEMA_NAME}.{DIRECTOR} SET first_name = %(first_name)s, 
            last_name = %(last_name)s, created_at = %(created_at)s
            WHERE director_id = %(id)s
            RETURNING *;"""

    params = {
        "first_name": first_name,
        "last_name": last_name,
        "created_at": created_at,
        "id": id,
    }

    result = do_query(sql, params)
    return result


def svc_delete(id):
    """
    A DELETE service
    """

    sql = (
        f"DELETE FROM {SCHEMA_NAME}.{DIRECTOR} WHERE director_id = %(id)s RETURNING *;"
    )
    params = {
        "id": id,
    }

    result = do_query(sql, params)
    return result


def svc_exact_search(payload):
    """
    An Exact search service
    """
    search_fields = payload["fields"]

    for idx, field_obj in enumerate(search_fields):
        field = field_obj["field"]
        value = field_obj["value"]

        if idx == 0:
            exact_clause = f"{field} = '{value}';"

    sql = f"SELECT * FROM {SCHEMA_NAME}.{DIRECTOR} WHERE {exact_clause}"
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result


def svc_like_search(payload):
    """
    LIKE Search service
    """

    search_fields = payload["fields"]
    like_clause = ""

    for idx, field_obj in enumerate(search_fields):
        field = field_obj["field"]
        value = field_obj["value"]

        if idx == 0:
            like_clause = f"{field} LIKE '%%{value}%%'"

    sql = f"SELECT * FROM {SCHEMA_NAME}.{DIRECTOR} WHERE {like_clause};"
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result


def svc_in_search(payload):
    """
    In Search service
    """

    field = payload["field"]
    values = payload["values"]
    in_clause = ""

    for idx, value in enumerate(values):
        val = value["value"]
        if idx == 0:
            in_clause = f"'{val}'"
        else:
            in_clause = f"{in_clause}, '{val}'"

    sql = f"SELECT * FROM {SCHEMA_NAME}.{DIRECTOR} WHERE {field} IN ({in_clause});"
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result
