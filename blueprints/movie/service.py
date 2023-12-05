from db.db_utils import do_query
from constants.constants import SCHEMA_NAME, MOVIE


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
    sql = (
        f"""
        UPDATE {SCHEMA_NAME}.{MOVIE} SET title = %(title)s, description = %(description)s,
        movie_year = %(movie_year)s, rating = %(rating)s, runtime = %(runtime)s,
        votes = %(votes)s, revenue = %(revenue)s, metascore = %(metascore)s, 
        created_at = %(created_at)s
        WHERE movie_id = %(id)s
        RETURNING *;"""
        )

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
                "id": id
            }

    result = do_query(sql, params)

    return result


def svc_delete(movie_id):
    """
    A DELETE service
    """

    # deletes from the child table first and then deletes from parent table
    sql = (
        # child table
        """
        DELETE FROM movies.movie_review WHERE movie_id = %(movie_id)s;
        """

        # parent table
        f"""DELETE FROM {SCHEMA_NAME}.{MOVIE} WHERE movie_id = %(movie_id)s
        RETURNING *;
        """
        )

    params = {
            "movie_id": movie_id
            }

    result = do_query(sql, params)
    print(result)

    return result
