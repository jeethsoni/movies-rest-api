from constants.constants import SCHEMA_NAME, MOVIE_ACTOR
from db.db_utils import do_query


def svc_get():
    """
    Get service
    """

    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_ACTOR};"

    result = do_query(sql, {})
    return result


def svc_get_by_id(ids_):
    """
    GET by ID service
    """

    ids = ids_.split(",")
    params = {"movie_id": ids[0], "actor_id": ids[1]}
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE_ACTOR} WHERE movie_id = %(movie_id)s AND actor_id = %(actor_id)s;"

    result = do_query(sql, params)
    return result


def svc_post(payload):
    """
    POST service
    """

    movie_id = payload["movie_id"]
    actor_id = payload["actor_id"]

    sql = f"INSERT INTO {SCHEMA_NAME}.{MOVIE_ACTOR}(movie_id, actor_id) VALUES(%s, %s) RETURNING *;"
    params = [movie_id, actor_id]

    result = do_query(sql, params)
    return result


# def svc_put(id, payload):
#     """
#     PUT service
#     """
#     movie_id = payload["movie_id"]
#     actor_id = payload["actor_id"]
#     created_at = payload["created_at"]

#     sql = f"""UPDATE {SCHEMA_NAME}.{MOVIE_ACTOR} SET movie_id = %(movie_id)s,
#         actor_id = %(actor_id)s, created_at = %(created_at)s 
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
    actor_id = ids[1]

    sql = f"""DELETE FROM {SCHEMA_NAME}.{MOVIE_ACTOR} 
            WHERE movie_id = %s AND actor_id = %s
            RETURNING *;"""
    params = [movie_id, actor_id]

    result = do_query(sql, params)
    return result
