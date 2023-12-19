from db.db_utils import do_query
from constants.constants import MOVIE_REVIEW, SCHEMA_NAME, MOVIE


def svc_get():
    """
    A GET service to get all records
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE};"
    result = do_query(sql, {})

    return result


def svc_get_by_id(id):
    """
    A GET service to get by ID
    """
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE} WHERE movie_id = %s;"
    params = [id]
    result = do_query(sql, params)

    return result


def svc_post(payload):
    """
    A POST service
    """

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


def svc_put(payload, id):
    """
    A PUT Service
    """
    title = payload["title"]
    description = payload["description"]
    year = payload["movie_year"]
    rating = payload["rating"]
    runtime = payload["runtime"]
    votes = payload["votes"]
    revenue = payload["revenue"]
    metascore = payload["metascore"]
    created_at = payload["created_at"]

    # SQL statement
    sql = f"""
        UPDATE {SCHEMA_NAME}.{MOVIE} SET title = %(title)s, description = %(description)s,
        movie_year = %(movie_year)s, rating = %(rating)s, runtime = %(runtime)s,
        votes = %(votes)s, revenue = %(revenue)s, metascore = %(metascore)s, 
        created_at = %(created_at)s
        WHERE movie_id = %(id)s
        RETURNING *;"""

    # parameters for SQL
    params = {
        "title": title,
        "description": description,
        "movie_year": year,
        "rating": rating,
        "runtime": runtime,
        "votes": votes,
        "revenue": revenue,
        "metascore": metascore,
        "created_at": created_at,
        "id": id,
    }

    result = do_query(sql, params)

    return result


def svc_delete(movie_id):
    """
    A DELETE service
    """

    # deletes from the child table first and then deletes from parent table
    child_table_sql = (
        # child table
        f"""
        DELETE FROM {SCHEMA_NAME}.{MOVIE_REVIEW} WHERE movie_id = %(movie_id)s;
        """
    )

    # # parent table
    parent_table_sql = f"""DELETE FROM {SCHEMA_NAME}.{MOVIE} WHERE movie_id = %(movie_id)s
        RETURNING *;
        """

    # parameters for SQL
    params = {"movie_id": movie_id}

    # execute child table query
    do_query(child_table_sql, params)

    # execute parent table query
    result = do_query(parent_table_sql, params)
    return result


def svc_exact_search(payload):
    """
    EXACT search service
    """
    field = payload["field"]
    value = payload["value"]

    search_condition = f"{field} = '{value}'"
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE} WHERE {search_condition}"

    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result


def svc_like_search(payload):
    """
    LIKE search service
    """

    field = payload["field"]
    value = payload["value"]

    search_condition = f"{field} LIKE '%%{value}%%'"
    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE} WHERE {search_condition};"

    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result


def svc_in_search(payload):
    """
    IN search service
    """

    field = payload["field"]
    value = payload["value"]

    in_search = f"{field} IN ('{value}')"

    sql = f"SELECT * FROM {SCHEMA_NAME}.{MOVIE} WHERE {in_search};"

    params = {"field": field, "value": value}

    result = do_query(sql, params)
    return result
