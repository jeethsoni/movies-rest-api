import os

from flask import Blueprint, request, jsonify
from blueprints.movie_review.service import (
    svc_delete,
    svc_exact_search,
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_like_search,
    svc_post,
    svc_put,
)


version = os.getenv("VERSION")
movie_review_blueprint = Blueprint("movie_review", __name__, url_prefix=version)


@movie_review_blueprint.route("/movie_review/movie_reviews", methods=["GET"])
def get_all_records():
    """
    Get all movie_review records
    """

    result = svc_get()
    return jsonify(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/<movie_id>/<review_id>", methods=["GET"])
def get_by_id(movie_id: int, review_id: int):
    """
    GET records by ID
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {review_id}"

    result = svc_get_by_id(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/create", methods=["POST"])
def post_record():
    """
    POST a new record
    """

    payload = request.get_json()
    result = svc_post(payload)

    status = result["status"]
    if status == 200:
        return jsonify(status=201)


@movie_review_blueprint.route("/movie_review/<movie_id>/<review_id>", methods=["PUT"])
def put_record(movie_id: int, review_id: int):
    """
    Updates a record
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {review_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return jsonify(status=result["status"], data=result["data"])


@movie_review_blueprint.route(
    "/movie_review/<movie_id>/<review_id>", methods=["DELETE"]
)
def delete_movie(movie_id: int, review_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {review_id}"

    result = svc_delete(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/in", methods=["POST"])
def search_by_in():
    """
    Searches records by in
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/like", methods=["POST"])
def search_by_like():
    """
    Searchhes record by Like
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/exact", methods=["POST"])
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return jsonify(status=result["status"], data=result["data"])
