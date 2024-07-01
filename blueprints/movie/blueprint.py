"""
blueprint for movie table
"""
from datetime import date, datetime
import os
from typing import Optional
from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate

from blueprints.movie.service import (
    svc_delete,
    svc_exact_search,
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_like_search,
    svc_post,
    svc_put,
)


class MovieItem(BaseModel):
    """Movie item model"""

    title: str
    description: str
    movie_year: str
    rating: float
    runtime: float
    votes: int
    revenue: float
    metascore: int
    created_at: Optional[str]


class MovieDataModel(BaseModel):
    """Movie data model"""

    movie_id: int
    title: str
    description: str
    movie_year: date
    rating: float
    runtime: float
    votes: int
    revenue: float
    metascore: int
    created_at: Optional[str | datetime | date]


class MessageModel(BaseModel):
    """Message model"""

    message: str


class ResponseModel(BaseModel):
    """Movie response model"""

    status: int
    data: list[MovieDataModel | MessageModel]


class FieldValueModel(BaseModel):
    """Movie Field and Value mmodel"""

    field: str
    value: str | int | date | float


class SearchModel(BaseModel):
    """Movie search model"""

    fields: list[FieldValueModel]


class ValueModel(BaseModel):
    """Value model"""

    value: str | float | int | date


class InModel(BaseModel):
    """In Search model"""

    field: str
    values: list[ValueModel]


class PostModel(BaseModel):
    """Movie Post model status"""

    status: int | str


version = os.getenv("VERSION")
movie_blueprint = Blueprint("movie", __name__, url_prefix=version)


@movie_blueprint.route("/movie/movies", methods=["GET"])
@validate()
def get_all_records():
    """
    A GET handler. Returns all records for customer.
    """
    result = svc_get()

    return ResponseModel(status=result["status"], data=result["data"])


@movie_blueprint.route("/movie/<movie_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int):
    """
    A GET handler. Returns record by a given identifier.
    """
    result = svc_get_by_id(movie_id)

    return ResponseModel(status=result["status"], data=result["data"])


@movie_blueprint.route("/movie/create", methods=["POST"])
@validate(body=MovieItem)
def post_movie():
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


@movie_blueprint.route("/movie/<movie_id>", methods=["PUT"])
@validate(body=MovieItem)
def put_movie(movie_id: int):
    """
    A PUT handler.
    Updates a record by id
    """

    # request object
    payload = request.get_json()
    result = svc_put(payload, movie_id)

    return ResponseModel(status=result["status"], data=result["data"])


@movie_blueprint.route("/movie/<movie_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    result = svc_delete(movie_id)

    return ResponseModel(status=result["status"], data=result["data"])


@movie_blueprint.route("/movie/exact", methods=["POST"])
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


@movie_blueprint.route("/movie/like", methods=["POST"])
@validate(body=SearchModel)
def like_search():
    """
    LIKE SEARCH
    Retrives all records from movies for like value search
    """

    payload = request.get_json()

    result = svc_like_search(payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_blueprint.route("/movie/in", methods=["POST"])
@validate(body=InModel)
def in_search():
    """
    IN SEARCH
    Retrives all records from movies for in value search
    """

    payload = request.get_json()

    result = svc_in_search(payload)
    return ResponseModel(status=result["status"], data=result["data"])
