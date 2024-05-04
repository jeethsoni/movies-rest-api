from datetime import date, datetime
import os
from typing import Optional

from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate
from blueprints.movie_review.service import (
    svc_delete,
    svc_exact_search,
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_post,
    svc_put,
)


class MovieReviewItems(BaseModel):
    """
    MovieReview items
    """

    movie_id: int
    review: int
    created_at: Optional[str]


class MovieReviewDataModel(BaseModel):
    """
    MovieReview Data Model
    """

    movie_id: int
    review_id: int
    review: int
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

    data: list[MovieReviewDataModel | MessageModel]
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
    Post model class
    """

    status: int | str


version = os.getenv("VERSION")
movie_review_blueprint = Blueprint("movie_review", __name__, url_prefix=version)


@movie_review_blueprint.route("/movie_review/movie_reviews", methods=["GET"])
@validate()
def get_all_records():
    """
    Get all movie_review records
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/<movie_id>/<review_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int, review_id: int):
    """
    GET records by ID
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {review_id}"

    result = svc_get_by_id(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/create", methods=["POST"])
@validate(body=MovieReviewItems)
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


@movie_review_blueprint.route("/movie_review/<review_id>", methods=["PUT"])
@validate(body=MovieReviewItems)
def put_record(review_id: int):
    """
    Updates a record
    """

    payload = request.get_json()
    result = svc_put(review_id, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route(
    "/movie_review/<movie_id>/<review_id>", methods=["DELETE"]
)
@validate()
def delete_movie(movie_id: int, review_id: int):
    """
    A DELETE handler
    Deletes a record by id
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {review_id}"

    result = svc_delete(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    Searches records by in
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/exact", methods=["POST"])
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
