"""
Service file for actor
"""
from db.db_utils import do_query
from constants.constants import ACTOR, SCHEMA_NAME


def svc_get():
    """
    A GET service to get all records
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{ACTOR};"
    result = do_query(sql, {})

    return result


def svc_get_by_id(actor_id):
    """
    A GET service to get by ID
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{ACTOR} WHERE actor_id = %s;"
    params = [actor_id]
    result = do_query(sql, params)

    return result


def svc_post(payload):
    """
    A POST service
    """

    # parameters for the query
    first_name = payload["first_name"]
    last_name = payload["last_name"]
    gender = payload["gender"]
    age = payload["age"]

    # SQL statement
    sql = f"INSERT INTO {SCHEMA_NAME}.{ACTOR}(first_name, last_name, gender, age) VALUES (%s, %s, %s, %s) RETURNING *;"
    params = [first_name, last_name, gender, age]

    result = do_query(sql, params)

    return result


def svc_put(payload, id):
    """
    A PUT service
    """

    first_name = payload["first_name"]
    last_name = payload["last_name"]
    gender = payload["gender"]
    age = payload["age"]
    created_at = payload["created_at"]

    # SQL Statement
    sql = f"""
            UPDATE {SCHEMA_NAME}.{ACTOR} SET first_name = %(first_name)s, last_name = %(last_name)s,
            gender = %(gender)s, age = %(age)s, created_at = %(created_at)s
            WHERE actor_id = %(id)s
            RETURNING *;"""

    params = {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "age": age,
        "created_at": created_at,
        "id": id,
    }

    result = do_query(sql, params)
    return result


def svc_delete(id):
    """
    A DELETE service
    """

    sql = f"DELETE FROM {SCHEMA_NAME}.{ACTOR} WHERE actor_id = %(id)s RETURNING *;"
    params = {
        "id": id,
    }

    result = do_query(sql, params)
    return result


def svc_exact_search(payload):
    """
    An Exact search service
    """

    field = payload["field"]
    value = payload["value"]

    exact_clause = f"{field} = '{value}';"
    sql = f"SELECT * FROM {SCHEMA_NAME}.{ACTOR} WHERE {exact_clause}"

    params = {"field": field, "value": value}

    result = do_query(sql, params)

    return result


def svc_like_search(payload):
    """
    LIKE Search service
    """

    field = payload["field"]
    value = payload["value"]
    like_clause = ""

    for idx, value in enumerate():
        