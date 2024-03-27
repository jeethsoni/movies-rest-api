"""
blueprint for actor table
"""
from datetime import date, datetime
import os
from flask import Blueprint, jsonify, request
from pydantic import BaseModel
from typing import Optional
from flask_pydantic import validate

from blueprints.actor.service import (
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_post,
    svc_put,
    svc_delete,
    svc_exact_search,
    svc_like_search,
)


class ActorItems(BaseModel):
    """
    Actor Items
    """

    first_name: str
    last_name: str
    age: int
    gender: str
    created_at: Optional[str]


class ActorDataModel(BaseModel):
    """
    Actor Data Model
    """

    actor_id: int
    first_name: str
    last_name: str
    age: int
    gender: str
    created_at: Optional[str | datetime | date]


class MessageModel(BaseModel):
    """
    Message model
    """

    message: str


class ResponseModel(BaseModel):
    """
    Response model
    """

    status: int
    data: list[ActorDataModel | MessageModel]


class FieldValueModel(BaseModel):
    """
    Field and value model
    """

    field: str
    value: int | str | date | float


class SearchModel(BaseModel):
    """
    Search model
    """

    fields: list[FieldValueModel]


class ValueModel(BaseModel):
    value: int | str | date | float


class InModel(BaseModel):
    field: str
    value: list[ValueModel]


class PostModel(BaseModel):
    """Post model status"""

    status: int | str


version = os.getenv("VERSION")
actor_blueprint = Blueprint("actor", __name__, url_prefix=version)


@actor_blueprint.route("/actor/actors", methods=["GET"])
@validate()
def get_all_records():
    """
    A GET handler. Returns all records for actor.
    """
    result = svc_get()

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/<actor_id>", methods=["GET"])
@validate()
def get_by_id(actor_id: int):
    """
    A GET handler. Returns record by a given identifier.
    """
    result = svc_get_by_id(actor_id)

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/create", methods=["POST"])
@validate(body=ActorItems)
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
@validate(body=ActorItems)
def put_actor(actor_id: int):
    """
    A PUT handler for actor table
    """

    payload = request.get_json()

    result = svc_put(payload, actor_id)

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/<actor_id>", methods=["DELETE"])
@validate()
def delete_actor(actor_id: int):
    """
    A DELETE handle
    """

    result = svc_delete(actor_id)
    return jsonify(status=result["status"])


@actor_blueprint.route("/actor/exact", methods=["POST"])
@validate(body=SearchModel)
def search_by_exact():
    """
    Exact search
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/like", methods=["POST"])
@validate(body=SearchModel)
def search_by_like():
    """
    Like Search
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return jsonify(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    In Search
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return jsonify(status=result["status"], data=result["data"])
