"""
Query utility class
"""


from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from flask import current_app as app


class Query():
    """
    Query class
    """
    def __init__(self, conn_pool):
        """
        connection pool constructor
        """

        self.conn_pool = conn_pool
        # grabs a connection from the pool
        self.conn = self.conn_pool.getconn()
        # opens a cursor to execute sql statements
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute(self, query, params=None):
        """
        This method will execute a sql query with or without parameters

        parameter query = sql
        parameter params = query parameters (optional)
        """

        # try and except block
        try:
            self.cursor.execute(query, params)  # execute the query
        except OperationalError as err:
            # log and raise the thrown error
            app.logger.error("Query execution failed => " + str(err))
            raise OperationalError(str(err)) from err

    def row(self):
        """
        return integer row count of a given query
        """
        return self.cursor.rowcount()

    def fetch(self):
        """
        Returns: dictionary of rows
        returns the data from the executed query
        """
        return self.cursor.fetchall()

    def close(self):
        """
        Puts the connection back in the pool
        """

        self.conn_pool.putconn(self.conn)
