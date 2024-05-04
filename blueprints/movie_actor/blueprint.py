import os

from datetime import date, datetime
from typing import Optional
from flask_pydantic import validate
from flask import Blueprint, request
from pydantic import BaseModel
from blueprints.movie_actor.service import (
    svc_delete,
    svc_get,
    svc_get_by_id,
    svc_post,
    svc_put,
    svc_exact_search,
)


class MovieActorDataModel(BaseModel):
    """
    Genre Data Model
    """

    movie_id: int
    actor_id: int
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

    data: list[MovieActorDataModel | MessageModel]
    status: int


class FieldValueModel(BaseModel):
    """
    Field and Value model
    """

    field: str
    value: str | int


class SearchModel(BaseModel):
    """
    Search model
    """

    fields: list[FieldValueModel]


class PostModel(BaseModel):
    """
    Post Model
    """

    status: int


version = os.getenv("VERSION")
movie_actor_blueprint = Blueprint("movie_actor", __name__, url_prefix=version)


@movie_actor_blueprint.route("/movie_actor/movie_actors", methods=["GET"])
@validate()
def get_all_records():
    """
    Get all movie_actor records
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/<movie_id>/<actor_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int, actor_id: int):
    """
    GET records by ID
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {actor_id}"

    result = svc_get_by_id(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/create", methods=["POST"])
@validate(body=MovieActorDataModel)
def post_record():
    """
    POST a new record
    """

    payload = request.get_json()
    result = svc_post(payload)

    if result["status"] == 200:
        status = 201
    else:
        status = result["status"]

    return PostModel(status=status)


@movie_actor_blueprint.route("/movie_actor/<movie_id>/<actor_id>", methods=["PUT"])
@validate(body=MovieActorDataModel)
def put_record(movie_id: int, actor_id: int):
    """
    Updates a record
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {actor_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/<movie_id>/<actor_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int, actor_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {actor_id}"

    result = svc_delete(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/exact", methods=["POST"])
@validate(body=SearchModel)
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return ResponseModel(status=result["status"], data=result["data"])
