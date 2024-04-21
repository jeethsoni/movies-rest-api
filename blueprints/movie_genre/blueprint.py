import os

from flask import Blueprint, jsonify, request
from blueprints.movie_genre.service import svc_delete, svc_exact_search, svc_get, svc_get_by_id, svc_post


version = os.getenv("VERSION")
movie_genre_blueprint = Blueprint("movie_genre", __name__, url_prefix=version)


@movie_genre_blueprint.route("/movie_genre/movie_genres", methods=["GET"])
def get_all_records():
    """
    Get all movie_genre records
    """

    result = svc_get()
    return jsonify(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/<movie_id>/<genre_id>", methods=["GET"])
def get_by_id(movie_id: int, genre_id: int):
    """
    GET records by ID
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {genre_id}"

    result = svc_get_by_id(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/create", methods=["POST"])
def post_record():
    """
    POST a new record
    """

    payload = request.get_json()
    result = svc_post(payload)

    status = result["status"]
    if status == 200:
        return jsonify(status=201)


#### PUT Route


@movie_genre_blueprint.route("/movie_genre/<movie_id>/<genre_id>", methods=["DELETE"])
def delete_movie(movie_id: int, genre_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {genre_id}"

    result = svc_delete(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/exact", methods=["POST"])
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return jsonify(status=result["status"], data=result["data"])
