from constants.constants import SCHEMA_NAME, MOVIE_REVIEW
from db.db_utils import do_query


def svc_get():
    """
    Get service
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_REVIEW};"

    result = do_query(sql, {})
    return result


def svc_get_by_id(ids_):
    """
    GET by ID service
    """

    ids = ids_.split(",")
    params = {"movie_id": ids[0], "review_id": ids[1]}
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_REVIEW} WHERE movie_id = %(movie_id)s AND review_id = %(review_id)s;"

    result = do_query(sql, params)
    return result


def svc_post(payload):
    """
    POST service
    """

    movie_id = payload["movie_id"]
    review = payload["review"]

    sql = f"""INSERT INTO {SCHEMA_NAME}.{MOVIE_REVIEW}(movie_id, review)
            VALUES(%s, %s) RETURNING *;"""
    params = [movie_id, review]

    result = do_query(sql, params)
    return result


def svc_put(id, payload):
    """
    PUT service
    """

    # payload
    movie_id = payload["movie_id"]
    review = payload["review"]
    created_at = payload["created_at"]

    sql = f"""UPDATE {SCHEMA_NAME}.{MOVIE_REVIEW} SET movie_id = %(movie_id)s, review = %(review)s,
        created_at = %(created_at)s WHERE review_id = %(review_id)s
        RETURNING *;"""
    params = {
        "review": review,
        "created_at": created_at,
        "movie_id": movie_id,
        "review_id": id
    }

    result = do_query(sql, params)
    return result


def svc_delete(ids_):
    """
    DELETE service
    """

    ids = ids_.split(",")
    movie_id = ids[0]
    review_id = ids[1]

    sql = f"""DELETE FROM {SCHEMA_NAME}.{MOVIE_REVIEW}
            WHERE movie_id = %s AND review_id = %s
            RETURNING *;"""
    params = [movie_id, review_id]

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

    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_REVIEW} WHERE {field} IN ({in_clause});"
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result


def svc_exact_search(payload):
    """
    EXACT search service
    """

    search_condition = ""
    search_fields = payload["fields"]

    for idx, field_obj in enumerate(search_fields):
        field = field_obj["field"]
        value = field_obj["value"]
        if idx == 0:
            search_condition = f"{field} = '{value}'"
    sql = f"""SELECT * FROM {SCHEMA_NAME}.{MOVIE_REVIEW}
              WHERE {search_condition};"""
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result
