"""
Database connection class
"""

import os
import logging

from dotenv import load_dotenv
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import DatabaseError
import emoji


class Connection:
    """
    Database connection class
    """

    def __init__(self):
        """
        constructor
        """
        self.setpool()

    def getconn(self):
        """
        gets connection from the pool
        """
        return self.pool.getconn()

    def putconn(self, conn):
        """
        places connection back in the pool
        """
        self.pool.putconn(conn)

    def setpool(self):
        """
        sets connection pool
        """
        try:
            load_dotenv()
            self.config = {}
            self.config["user"] = os.getenv("DB_USER")
            self.config["password"] = os.getenv("DB_PASSWORD")
            self.config["host"] = os.getenv("DB_HOST")
            self.config["port"] = os.getenv("DB_PORT")
            self.config["database"] = os.getenv("DATABASE")
            # configure threaded connection pool
            self.pool = ThreadedConnectionPool(
                minconn=os.getenv("MIN_CONNECTIONS"),
                maxconn=os.getenv("MAX_CONNECTIONS"),
                **self.config
            )
            logging.info(emoji.emojize("Connected to database...:party_popper:"))
            print("Connected to database")
        except DatabaseError:
            logging.error(
                emoji.emojize("Error in setting up database connection :cross_mark:")
            )
