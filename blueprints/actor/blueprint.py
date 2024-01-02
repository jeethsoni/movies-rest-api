"""
blueprint for actor table
"""
import os
from flask import Blueprint, jsonify, request

from blueprints.actor.service import svc_get, svc_get_by_id, svc_post


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
def post_movie():
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
