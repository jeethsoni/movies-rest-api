"""
Service file for movie_genre
"""

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


def svc_put(ids_, payload):
    """
    PUT service
    """

    # splitting the ids
    ids = ids_.split(",")

    # payload
    movie_id = payload["movie_id"]
    genre_id = payload["genre_id"]

    # deletes the record
    delete_stat_sql = f"""DELETE FROM {SCHEMA_NAME}.{MOVIE_GENRE} 
            WHERE movie_id = %(movie_id)s AND genre_id = %(genre_id)s
            RETURNING *;"""
    delete_sql_params = {"movie_id": ids[0], "genre_id": ids[1]}

    insert_stat_sql = f"""INSERT INTO {SCHEMA_NAME}.{MOVIE_GENRE}(movie_id, genre_id)
                        VALUES(%s, %s) RETURNING *;"""
    insert_sql_params = [movie_id, genre_id]

    # executes the query to delete the record from the table
    do_query(delete_stat_sql, delete_sql_params)

    # inserts the new record to the table
    result = do_query(insert_stat_sql, insert_sql_params)
    return result


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


def svc_delete_movie(movie_id):
    """
    Delete service for to delete all movie genres by given ID
    """

    sql = f"""
        DELETE FROM {SCHEMA_NAME}.{MOVIE_GENRE} WHERE movie_id = %s
        RETURNING *;
        """
    params = [movie_id]

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
