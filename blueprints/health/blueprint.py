"""
blueprint for health check
"""

import os
from flask import Blueprint, jsonify
from db.db_utils import do_query


version = os.getenv("VERSION")
health_blueprint = Blueprint("health", __name__, url_prefix=version)


@health_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    a GET handler for api health check
    """

    # executes the sql and returns timestamp
    sql = "SELECT CURRENT_TIMESTAMP;"
    data = do_query(sql, [])

    # checks if current timestamp returns timestamp or none
    row = data["data"][0]
    data_check = row.get("current_timestamp")

    # checks the API and database health
    if data_check is None or data["status"] == 500:
        return jsonify(db_health="NOT OK", status=500)

    return jsonify(message="OK", database_health="OK", status=200)
