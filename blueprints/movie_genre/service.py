from constants.constants import SCHEMA_NAME, MOVIE_GENRE
from db.db_utils import do_query


def svc_get():
    """
    Get service
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_GENRE};"

    result = do_query(sql, {})
    return result


def svc_get_by_id(ids_):
    """
    GET by ID service
    """

    ids = ids_.split(",")
    params = {"movie_id": ids[0], "genre_id": ids[1]}
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_GENRE} WHERE movie_id = %(movie_id)s AND genre_id = %(genre_id)s;"

    result = do_query(sql, params)
    return result


def svc_post(payload):
    """
    POST service
    """

    movie_id = payload["movie_id"]
    genre_id = payload["genre_id"]

    sql = f"INSERT INTO {SCHEMA_NAME}.{MOVIE_GENRE}(movie_id, genre_id) VALUES(%s, %s) RETURNING *;"
    params = [movie_id, genre_id]

    result = do_query(sql, params)
    return result


# def svc_put(id, payload):
#     """
#     PUT service
#     """
#     movie_id = payload["movie_id"]
#     genre_id = payload["genre_id"]
#     created_at = payload["created_at"]

#     sql = f"""UPDATE {SCHEMA_NAME}.{MOVIE_GENRE} SET movie_id = %(movie_id)s,
#         genre_id = %(genre_id)s, created_at = %(created_at)s
#         WHERE genre_id = %(genre_id)s
#         RETURNING *;"""
#     params = {"name": name, "created_at": created_at, "genre_id": id}

#     result = do_query(sql, params)
#     return result


def svc_delete(ids_):
    """
    DELETE service
    """

    ids = ids_.split(",")
    movie_id = ids[0]
    genre_id = ids[1]

    sql = f"""DELETE FROM {SCHEMA_NAME}.{MOVIE_GENRE}
            WHERE movie_id = %s AND genre_id = %s
            RETURNING *;"""
    params = [movie_id, genre_id]

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
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_GENRE} WHERE {search_condition};"
    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result
