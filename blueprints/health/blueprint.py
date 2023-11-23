"""
blueprint for health check
"""
import os
from flask import Blueprint, jsonify


version = os.getenv("VERSION")
health_blueprint = Blueprint("health", __name__, url_prefix=version)


@health_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    a GET handler for api health check
    """
    return jsonify(message="OK", status=200)
