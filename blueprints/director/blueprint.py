"""Director table blueprint"""

from datetime import date, datetime
import os
from typing import Optional
from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate

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


class DirectorItems(BaseModel):
    """
    Items
    """

    first_name: str
    last_name: str
    created_at: Optional[str]


class DirectorDataModel(BaseModel):
    """
    Data Model
    """

    director_id: int
    first_name: str
    last_name: str
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
    data: list[DirectorDataModel | MessageModel]


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
    """
    Value model
    """

    value: int | str | date | float


class InModel(BaseModel):
    """
    In model
    """
    field: str
    values: list[ValueModel]


class PostModel(BaseModel):
    """Post model status"""

    status: int | str


version = os.getenv("VERSION")
director_blueprint = Blueprint("director", __name__, url_prefix=version)


@director_blueprint.route("/director/directors", methods=["GET"])
@validate()
def get_all_records():
    """
    A GET handler. Returns all records for director.
    """
    result = svc_get()

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/<director_id>", methods=["GET"])
@validate()
def get_by_id(director_id: int):
    """
    A GET handler. Returns record by a given identifier.
    """
    result = svc_get_by_id(director_id)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/create", methods=["POST"])
@validate(body=DirectorItems)
def post_director():
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

    return PostModel(status=status)


@director_blueprint.route("/director/<director_id>", methods=["PUT"])
@validate(body=DirectorItems)
def put_director(director_id: int):
    """
    A PUT handler for director table
    """

    payload = request.get_json()

    result = svc_put(payload, director_id)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/<director_id>", methods=["DELETE"])
@validate()
def delete_director(director_id: int):
    """
    A DELETE handle
    """

    result = svc_delete(director_id)
    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/exact", methods=["POST"])
@validate(body=SearchModel)
def search_by_exact():
    """
    Exact search
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/like", methods=["POST"])
@validate(body=SearchModel)
def search_by_like():
    """
    Like Search
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    In Search
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])
