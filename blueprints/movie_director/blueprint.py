import os
from flask import Blueprint, jsonify, request
from blueprints.movie_director.service import (
    svc_delete,
    svc_get,
    svc_get_by_id,
    svc_post,
    svc_put,
    svc_exact_search,
)

version = os.getenv("VERSION")
movie_director_blueprint = Blueprint("movie_director", __name__, url_prefix=version)


@movie_director_blueprint.route("/movie_director/movie_directors", methods=["GET"])
def get_all_records():
    """
    Get all movie_director records
    """

    result = svc_get()
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route(
    "/movie_director/<movie_id>/<director_id>", methods=["GET"]
)
def get_by_id(movie_id: int, director_id: int):
    """
    GET records by ID
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    result = svc_get_by_id(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/create", methods=["POST"])
def post_record():
    """
    POST a new record
    """

    payload = request.get_json()
    result = svc_post(payload)

    status = result["status"]
    if status == 200:
        status = 201

    return jsonify(status=status)


@movie_director_blueprint.route(
    "/movie_director/<movie_id>/<director_id>", methods=["PUT"]
)
def put_record(movie_id: int, director_id: int):
    """
    Updates a record
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route(
    "/movie_director/<movie_id>/<director_id>", methods=["DELETE"]
)
def delete_movie(movie_id: int, director_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    result = svc_delete(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/exact", methods=["POST"])
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return jsonify(status=result["status"], data=result["data"])
