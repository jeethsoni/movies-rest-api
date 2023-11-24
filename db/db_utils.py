"""
database utility class
"""


import logging
import emoji
from flask import current_app as app
from psycopg2 import DatabaseError
from constants.constants import STATUS_OK, STATUS_ERR
from db.Query import Query


def do_query(sql, payload):
    """
    Service function to execute query
    """

    try:
        # creating an instance and passing database connection
        query = Query(app.conn)
        # executing the sql query
        query.execute(sql, payload)
        # stores the fetched result in 'data' variable
        data = query.fetch()
        query.close()
        # deletes the query
        del query

        return {"status": STATUS_OK, "data": data}
    except DatabaseError as err:
        # logs the database error
        logging.error(emoji.emojize("Error retrieving data :cross_mark:"))
        return {"status": STATUS_ERR, "error": err}
