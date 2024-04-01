"""
Genre table service
"""

from constants.constants import SCHEMA_NAME, GENRE
from db.db_utils import do_query


def svc_get():
    """
    Get All service
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{GENRE}"

    result = do_query(sql, {})
    return result


def svc_get_by_id(id):
    """
    Get all by id service
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{GENRE} WHERE genre_id = %s"
    params = [id]

    result = do_query(sql, params)
    return result


def svc_post(payload):
    """
    POST service
    """
    name = payload["name"]

    sql = f"INSERT INTO {SCHEMA_NAME}.{GENRE}(name) VALUES(%s) RETURNING *;"
    params = [name]

    result = do_query(sql, params)
    return result


def svc_put(id, payload):
    """
    POST service
    """
    name = payload["name"]
    created_at = payload["created_at"]

    sql = f"""UPDATE {SCHEMA_NAME}.{GENRE} SET name = %(name)s, 
        created_at = %(created_at)s WHERE genre_id = %(genre_id)s
        RETURNING *;"""
    params = {"name": name, "created_at": created_at, "genre_id": id}

    result = do_query(sql, params)
    return result


def svc_delete(id):
    """
    Delete service
    """

    sql = f"DELETE FROM {SCHEMA_NAME}.{GENRE} WHERE genre_id = %s RETURNING *;"
    params = [id]

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

    sql = f"SELECT * FROM {SCHEMA_NAME}.{GENRE} WHERE {field} IN ({in_clause});"
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result


def svc_like_search(payload):
    """
    Like Search service
    """

    fields = payload["fields"]
    like_clause = ""

    for idx, field_obj in enumerate(fields):
        field = field_obj["field"]
        value = field_obj["value"]

        if idx == 0:
            like_clause = f"{field} LIKE '%%{value}%%'"

    sql = f"SELECT * FROM {SCHEMA_NAME}.{GENRE} WHERE {like_clause}"
    params = {
        "field": field,
        "value": value
    }

    result = do_query(sql, params)
    return result


def svc_exact_search(payload):
    """
    Exact search service
    """

    search_condition = ""
    search_fields = payload["fields"]

    for idx, field_obj in enumerate(search_fields):
        field = field_obj["field"]
        value = field_obj["value"]
        if idx == 0:
            search_condition = f"{field} = '{value}'"
    sql = f"SELECT * FROM {SCHEMA_NAME}.{GENRE} WHERE {search_condition};"
    params = {
        "field": field,
        "value": value
    }

    result = do_query(sql, params)
    return result
