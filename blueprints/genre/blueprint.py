"""
Genre table blueprint
"""
from datetime import date, datetime
import os
from typing import Optional
from flask_pydantic import validate
from flask import Blueprint, request
from pydantic import BaseModel
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


class GenreItems(BaseModel):
    """
    Genre items
    """

    name: str
    created_at: Optional[str]


class GenreDataModel(BaseModel):
    """
    Genre Data Model
    """

    genre_id: int
    name: str
    created_at: Optional[str | date | datetime]


class MessageModel(BaseModel):
    """
    Message model
    """

    message: str


class ResponseModel(BaseModel):
    """
    Response Model
    """

    data: list[GenreDataModel | GenreItems]
    status: int


class FieldValueModel(BaseModel):
    """
    Field and Value model
    """

    field: str
    value: str


class SearchModel(BaseModel):
    """
    Search model
    """

    fields: list[FieldValueModel]


class ValueModel(BaseModel):
    """
    Value Model
    """

    value: str | date | datetime


class InModel(BaseModel):
    """
    In search model
    """

    field: str
    values: list[ValueModel]


class PostModel(BaseModel):
    """
    Post Model class
    """

    status: int | str


version = os.getenv("VERSION")
genre_blueprint = Blueprint("genre", __name__, url_prefix=version)


@genre_blueprint.route("/genre/genres", methods=["GET"])
@validate()
def get_all_records():
    """
    GET all records
    """
    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/<genre_id>", methods=["GET"])
@validate()
def get_by_id(genre_id: int):
    """
    GET all by id
    """

    result = svc_get_by_id(genre_id)
    print(result)
    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/create", methods=["POST"])
@validate(body=GenreItems)
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

    return PostModel(status=status)


@genre_blueprint.route("/genre/<genre_id>", methods=["PUT"])
@validate(body=GenreItems)
def put_record(genre_id: int):
    """
    Updates a record
    """

    payload = request.get_json()

    result = svc_put(genre_id, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/<genre_id>", methods=["DELETE"])
@validate()
def delete_record(genre_id: int):
    """
    deletes a record
    """

    result = svc_delete(genre_id)
    return ResponseModel(status=result["status"])


@genre_blueprint.route("/genre/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    Searches records by in
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/like", methods=["POST"])
@validate(SearchModel)
def search_by_like():
    """
    Searchhes record by Like
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/exact", methods=["POST"])
@validate(SearchModel)
def search_by_exact():
    """
    Searchhes record by Like
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])
