import os
from flask import Blueprint, jsonify, request

from blueprints.director.service import (
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_post,
    svc_put,
    svc_delete,
    svc_exact_search,
    svc_like_search,
)


version = os.getenv("VERSION")
director_blueprint = Blueprint("director", __name__, url_prefix=version)


@director_blueprint.route("/director/directors", methods=["GET"])
def get_all_records():
    """
    A GET handler. Returns all records for director.
    """
    result = svc_get()

    return jsonify(status=result["status"], data=result["data"])


@director_blueprint.route("/director/<director_id>", methods=["GET"])
def get_by_id(director_id: int):
    """
    A GET handler. Returns record by a given identifier.
    """
    result = svc_get_by_id(director_id)

    return jsonify(status=result["status"], data=result["data"])


@director_blueprint.route("/director/create", methods=["POST"])
def post_director():
    """
    A POST handler. Creates a new movie record
    """
    # request object
    payload = request.get_json()

    result = svc_post(payload)

    status = result["status"]
    if status == 200:
        return jsonify(status=201)

    return jsonify(status=status)


@director_blueprint.route("/director/<director_id>", methods=["PUT"])
def put_director(director_id: int):
    """
    A PUT handler for director table
    """

    payload = request.get_json()

    result = svc_put(payload, director_id)

    return jsonify(status=result["status"], data=result["data"])


@director_blueprint.route("/director/<director_id>", methods=["DELETE"])
def delete_director(director_id: int):
    """
    A DELETE handle
    """

    result = svc_delete(director_id)
    return jsonify(status=result["status"])


@director_blueprint.route("/director/exact", methods=["POST"])
def search_by_exact():
    """
    Exact search
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@director_blueprint.route("/director/like", methods=["POST"])
def search_by_like():
    """
    Like Search
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@director_blueprint.route("/director/in", methods=["POST"])
def search_by_in():
    """
    In Search
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return jsonify(status=result["status"], data=result["data"])
