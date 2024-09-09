"""
blueprint for movie_genre
"""


import os

from datetime import date, datetime
from typing import Optional
from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate
from blueprints.movie_review.service import (
    svc_delete,
    svc_delete_movie,
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
    ---
    tags:
      - Movie Review
    summary: Retrieve all movie reviews
    description: A GET handler that retrieves all movie review records.
    responses:
      200:
        description: Successfully retrieved all movie review records
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: array
                  description: List of all movie review records
                  items:
                    type: object
                    properties:
                      movie_id:
                        type: integer
                        description: ID of the movie
                      review_id:
                        type: integer
                        description: ID of the review
                      review:
                        type: string
                        description: The review content
                      created_at:
                        type: string
                        description: Timestamp when the review was created
      500:
        description: Internal server error
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/<movie_id>/<review_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int, review_id: int):
    """
    GET records by ID
    ---
    tags:
      - Movie Review
    summary: Retrieve a movie review by movie_id and review_id
    description: A GET handler that retrieves a specific movie review by the provided movie_id and review_id.
    parameters:
      - in: path
        name: movie_id
        required: true
        schema:
          type: integer
        description: ID of the movie
      - in: path
        name: review_id
        required: true
        schema:
          type: integer
        description: ID of the review
    responses:
      200:
        description: Successfully retrieved the movie review record
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: object
                  description: The movie review data
                  properties:
                    movie_id:
                      type: integer
                      description: ID of the movie
                    review_id:
                      type: integer
                      description: ID of the review
                    review:
                      type: int
                      description: The review content
                    created_at:
                      type: string
                      format: date-time
                      description: Timestamp when the review was created
      400:
        description: Invalid input
      404:
        description: Review not found
      500:
        description: Internal server error
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
    ---
    tags:
      - Movie Review
    summary: Create a new movie review
    description: A POST handler that creates a new movie review record.
    parameters:
      - in: body
        name: body
        description: Movie review data to be created
        schema:
          type: object
          required:
            - movie_id
            - review
            - created_at
          properties:
            movie_id:
              type: integer
              description: ID of the movie being reviewed
            review:
              type: string
              description: Text of the movie review
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie review was created
    responses:
      201:
        description: Movie review record created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: integer
                  description: HTTP status code
      400:
        description: Invalid input
      500:
        description: Internal server error
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
    ---
    tags:
      - Movie Review
    summary: Update an existing movie review
    description: A PUT handler that updates a movie review record by review_id.
    parameters:
      - in: path
        name: review_id
        required: true
        schema:
          type: integer
        description: ID of the review to be updated
      - in: body
        name: body
        description: Updated movie review data
        schema:
          type: object
          required:
            - movie_id
            - review
            - created_at
          properties:
            movie_id:
              type: integer
              description: ID of movie
            review:
              type: string
              description: Updated text of the movie review
            created_at:
              type: string
              format: date-time
              description: Timestamp when the review was last updated
    responses:
      200:
        description: Movie review record updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: object
                  description: Updated movie review data
                  properties:
                    review_id:
                      type: integer
                      description: ID of the review
                    movie_id:
                      type: integer
                      description: ID of movie
                    review:
                      type: string
                      description: Updated review content
                    created_at:
                      type: string
                      description: Timestamp when the review was last updated
      400:
        description: Invalid input
      404:
        description: Review not found
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_put(review_id, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route(
    "/movie_review/<movie_id>/<review_id>", methods=["DELETE"]
)
@validate()
def delete_movie_review(movie_id: int, review_id: int):
    """
    A DELETE handler
    Deletes a record by id.

    ---
    tags:
      - Movie Review
    summary: Delete a movie review by its ID
    description: A DELETE handler that deletes a movie review record by movie_id and review_id.
    parameters:
      - in: path
        name: movie_id
        required: true
        schema:
          type: integer
        description: ID of the movie associated with the review
      - in: path
        name: review_id
        required: true
        schema:
          type: integer
        description: ID of the review to be deleted
    responses:
      200:
        description: Movie review record deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: object
                  description: Details of the deleted record
      404:
        description: Review or movie not found
      500:
        description: Internal server error
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {review_id}"

    result = svc_delete(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/movie/<movie_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int):
    """
    A DELETE handler
    deletes all movie reviews by movie_id.

    ---
    tags:
      - Movie Review
    summary: Delete all reviews associated with a movie
    description: A DELETE handler that deletes all movie reviews associated with the given movie_id.
    parameters:
      - in: path
        name: movie_id
        required: true
        schema:
          type: integer
        description: ID of the movie whose reviews are to be deleted
    responses:
      200:
        description: All reviews for the specified movie have been deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: object
                  description: Details of the operation
      404:
        description: Movie not found or no reviews associated with the movie
      500:
        description: Internal server error
    """

    result = svc_delete_movie(movie_id)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_review_blueprint.route("/movie_review/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    Searches records by in.

    ---
    tags:
      - Movie Review
    summary: Search movie reviews using an 'in' clause
    description: Retrieves movie review records that match any value in a provided list of values for a specified field.
    parameters:
      - in: body
        name: body
        description: Search criteria including the field and values to match
        schema:
          type: object
          required:
            - field
            - values
          properties:
            field:
              type: string
              description: The field to search by (e.g., review_id, movie_id)
            values:
              type: array
              description: List of values to match
              items:
                type: object
                required:
                  - value
                properties:
                  value:
                    type: string
                    description: The value to match in the specified field
    responses:
      200:
        description: Successfully retrieved records matching any of the specified values
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: array
                  description: List of records matching the specified values
                  items:
                    type: object
                    properties:
                      movie_id:
                        type: integer
                        description: ID of the movie
                      review_id:
                        type: integer
                        description: ID of the review
                      review:
                        type: string
                        description: Text of the review
                      created_at:
                        type: string
                        format: date-time
                        description: Timestamp when the review was created
      400:
        description: Invalid input
      404:
        description: No records found matching the specified values
      500:
        description: Internal server error
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

    ---
    tags:
      - Movie Review
    summary: Exact search for movie reviews
    description: Retrieves all movie review records matching the exact value for specified fields.
    parameters:
      - in: body
        name: body
        description: JSON object containing search criteria for exact value match
        schema:
          type: object
          required:
            - fields
          properties:
            fields:
              type: array
              description: List of search criteria
              items:
                type: object
                required:
                  - field
                  - value
                properties:
                  field:
                    type: string
                    description: The field to search by (e.g., review_id, movie_id)
                  value:
                    type: string
                    description: The exact value to search for
    responses:
      200:
        description: Successfully retrieved records matching the exact value
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: Status of the operation
                data:
                  type: array
                  description: List of records matching the exact value
                  items:
                    type: object
                    properties:
                      movie_id:
                        type: integer
                        description: ID of the movie
                      review_id:
                        type: integer
                        description: ID of the review
                      review:
                        type: string
                        description: Text of the review
                      created_at:
                        type: string
                        format: date-time
                        description: Timestamp when the review was created
      400:
        description: Invalid input
      404:
        description: No records found matching the exact value
      500:
        description: Internal server error
    """

    # request object
    payload = request.get_json()

    result = svc_exact_search(payload)
    return ResponseModel(status=result["status"], data=result["data"])
