"""
blueprint for health check
"""
from flask import Blueprint, jsonify

health_blueprint = Blueprint("health", __name__)


@health_blueprint.route("/health", methods=["GET"])
def health_check():
    """
    a GET handler for api health check
    """
    return jsonify(message="OK", status=200)
