from flask import jsonify, request
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


def svc_post():
    """
    POST service
    """

    # request object
    payload = request.get_json()

    # parameters for the query
    title = payload["title"]
    description = payload["description"]
    year = payload["movie_year"]
    rating = payload["rating"]
    runtime = payload["runtime"]
    votes = payload["votes"]
    revenue = payload["revenue"]
    metascore = payload["metascore"]

    # SQL statement
    sql = f"INSERT INTO {SCHEMA_NAME}.{MOVIE}(title, description, movie_year, rating, runtime, votes, revenue, metascore) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *;"
    params = [title, description, year, rating, runtime, votes, revenue, metascore]

    result = do_query(sql, params)

    return result
