"""
blueprint for actor table
"""
import os
from flask import Blueprint, jsonify, request

from blueprints.actor.service import (
    svc_get,
    svc_get_by_id,
    svc_post,
    svc_put,
    svc_delete,
    svc_exact_search,
)


version = os.getenv("VERSION")
actor_blueprint = Blueprint("actor", __name__, url_prefix=version)


@actor_blueprint.route("/actor/actors", methods=["GET"])
def get_all_records():
    """
    A GET handler. Returns all records for actor.
    """
    result = svc_get()

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/<actor_id>", methods=["GET"])
def get_by_id(actor_id: int):
    """
    A GET handler. Returns record by a given identifier.
    """
    result = svc_get_by_id(actor_id)

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/create", methods=["POST"])
def post_actor():
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


@actor_blueprint.route("/actor/<actor_id>", methods=["PUT"])
def put_actor(actor_id: int):
    """
    A PUT handler for actor table
    """

    payload = request.get_json()

    result = svc_put(payload, actor_id)

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/<actor_id>", methods=["DELETE"])
def delete_actor(actor_id: int):
    """
    A DELETE handle
    """

    result = svc_delete(actor_id)
    return jsonify(status=result["status"])


@actor_blueprint.route("/actor/exact", methods=["POST"])
def search_by_exact():
    """
    Exact search
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return jsonify(status=result["status"], data=result["data"])
