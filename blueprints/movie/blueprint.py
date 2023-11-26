"""
blueprint for movie table
"""
import os
from flask import Blueprint, jsonify

from blueprints.movie.service import svc_get, svc_get_by_id


version = os.getenv("VERSION")
movie_blueprint = Blueprint("movie", __name__, url_prefix=version)


@movie_blueprint.route("/movie/movies", methods={"GET"})
def get_all_records():
    """
    A GET handler. Returns all records for customer.
    """
    result = svc_get()

    return jsonify(status=result["status"], data=result["data"])


@movie_blueprint.route("/movie/<movie_id>", methods=["GET"])
def get_by_id(movie_id: int):
    """
    A GET handler. Returns record by a given identifier.
    """
    result = svc_get_by_id(movie_id)

    return jsonify(status=result["status"], data=result["data"])
