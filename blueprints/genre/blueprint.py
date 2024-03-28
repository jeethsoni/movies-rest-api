"""
Genre table blueprint
"""
import os

from flask import Blueprint, jsonify, request
from blueprints.genre.service import (
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
genre_blueprint = Blueprint("genre", __name__, url_prefix=version)


@genre_blueprint.route("/genre/genres", methods=["GET"])
def get_all_records():
    """
    GET all records
    """
    result = svc_get()
    return jsonify(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/<genre_id>", methods=["GET"])
def get_by_id(genre_id: int):
    """
    GET all by id
    """

    result = svc_get_by_id(genre_id)
    print(result)
    return jsonify(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/create", methods=["POST"])
def post_record():
    """
    Creates new record
    """

    payload = request.get_json()

    result = svc_post(payload)
    status = result["status"]

    if result["status"] == 200:
        status = 201
    else:
        status = result["status"]

    return jsonify(status=status)


@genre_blueprint.route("/genre/<genre_id>", methods=["PUT"])
def put_record(genre_id: int):
    """
    Updates a record
    """

    payload = request.get_json()

    result = svc_put(genre_id, payload)
    return jsonify(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/<genre_id>", methods=["DELETE"])
def delete_record(genre_id: int):
    """
    deletes a record
    """

    result = svc_delete(genre_id)
    return jsonify(status=result["status"])


@genre_blueprint.route("/genre/in", methods=["POST"])
def search_by_in():
    """
    Searches records by in
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/like", methods=["POST"])
def search_by_like():
    """
    Searchhes record by Like
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/exact", methods=["POST"])
def search_by_exact():
    """
    Searchhes record by Like
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return jsonify(status=result["status"], data=result["data"])