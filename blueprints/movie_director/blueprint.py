from datetime import date, datetime
import os
from typing import Optional
from flask import Blueprint, jsonify, request
from pydantic import BaseModel
from flask_pydantic import validate

from blueprints.movie_director.service import (
    svc_delete,
    svc_get,
    svc_get_by_id,
    svc_post,
    svc_put,
    svc_exact_search,
)


class MovieDirectorDataModel(BaseModel):
    """
    Genre Data Model
    """

    movie_id: int
    director_id: int
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

    data: list[MovieDirectorDataModel | MessageModel]
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
movie_director_blueprint = Blueprint("movie_director", __name__, url_prefix=version)


@movie_director_blueprint.route("/movie_director/movie_directors", methods=["GET"])
@validate()
def get_all_records():
    """
    Get all movie_director records
    """

    result = svc_get()
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/<movie_id>/<director_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int, director_id: int):
    """
    GET records by ID
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    result = svc_get_by_id(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/create", methods=["POST"])
@validate(body=MovieDirectorDataModel)
def post_record():
    """
    POST a new record
    """

    payload = request.get_json()
    result = svc_post(payload)

    status = result["status"]
    if status == 200:
        status = 201

    return jsonify(status=status)


@movie_director_blueprint.route("/movie_director/<movie_id>/<director_id>", methods=["PUT"])
@validate(body=MovieDirectorDataModel)
def put_record(movie_id: int, director_id: int):
    """
    Updates a record
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/<movie_id>/<director_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int, director_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    result = svc_delete(pkeys)
    return jsonify(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/exact", methods=["POST"])
@validate(body=SearchModel)
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return jsonify(status=result["status"], data=result["data"])
