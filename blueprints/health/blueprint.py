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

    data = do_query(sql, {})

    # checks the API and database health
    if data["status"] == 200:
        return jsonify(api_health="OK", db_health="OK", status=200)
    else:
        return jsonify(db_health="NOT OK", status=500)
