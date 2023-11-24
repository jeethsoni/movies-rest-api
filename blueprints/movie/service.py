from db.db_utils import do_query


def svc_get():
    sql = "SELECT * FROM movies.movie;"
    result = do_query(sql, {})

    return result


def svc_get_by_id(id):

    sql = "SELECT * FROM movies.movie WHERE movie_id = %s;"
    params = [id]
    result = do_query(sql, params)

    return result
