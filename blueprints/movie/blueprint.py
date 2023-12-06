"""
blueprint for movie table
"""
import os
from flask import Blueprint, jsonify, request

from blueprints.movie.service import svc_delete, svc_exact_search, svc_get, svc_get_by_id, svc_post, svc_put


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


@movie_blueprint.route("/movie/create", methods=["POST"])
def post_movie():
    """
    A POST handler. Creates a new movie record
    """
    # request object
    payload = request.get_json()

    result = svc_post(payload)

    if result["status"] == 200:
        status = 201
    else:
        status = result["status"]

    return jsonify(status=status)


@movie_blueprint.route("/movie/<movie_id>", methods=["PUT"])
def put_movie(movie_id: int):
    """
    A PUT handler.
    Updates a record by id
    """

    # request object
    payload = request.get_json()

    result = svc_put(payload, movie_id)

    return jsonify(status=result["status"])


@movie_blueprint.route("/movie/<movie_id>", methods=["DELETE"])
def delete_movie(movie_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    result = svc_delete(movie_id)

    return jsonify(status=result["status"])


@movie_blueprint.route("/movie/exact", methods=["POST"])
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return jsonify(status=result["status"], data=result["data"])
