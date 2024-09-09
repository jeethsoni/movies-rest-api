"""
blueprint for movie_director
"""


from datetime import date, datetime
import os
from typing import Optional
from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate

from blueprints.movie_director.service import (
    svc_delete,
    svc_delete_movie,
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

    ---
    tags:
      - Movie Director
    summary: Get all movie-director relationships
    description: A GET handler that retrieves all movie-director records.
    responses:
      200:
        description: A list of movie-director relationships
        schema:
          type: array
          items:
            type: object
            properties:
              movie_id:
                type: integer
                description: ID of the movie
              director_id:
                type: integer
                description: ID of the director
              created_at:
                type: string
                format: date-time
                description: Timestamp when the movie-director record was created
      404:
        description: No records found
      500:
        description: Internal server error
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@movie_director_blueprint.route(
    "/movie_director/<movie_id>/<director_id>", methods=["GET"]
)
@validate()
def get_by_id(movie_id: int, director_id: int):
    """
    GET records by ID

    ---
    tags:
      - Movie Director
    summary: Get movie-director relationship by IDs
    description: A GET handler that retrieves a movie-director record based on movie ID and director ID.
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie
      - in: path
        name: director_id
        type: integer
        required: true
        description: ID of the director
    responses:
      200:
        description: Movie-director relationship record
        schema:
          type: object
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            director_id:
              type: integer
              description: ID of the director
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-director record was created
      404:
        description: Record not found
      500:
        description: Internal server error
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    result = svc_get_by_id(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/create", methods=["POST"])
@validate(body=MovieDirectorDataModel)
def post_record():
    """
    POST a new record
    ---
    tags:
      - Movie Director
    summary: Create a new movie-director relationship
    description: A POST handler that creates a new movie-director record.
    parameters:
      - in: body
        name: body
        description: Movie-director relationship data to be created
        schema:
          type: object
          required:
            - movie_id
            - director_id
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            director_id:
              type: integer
              description: ID of the director
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-director record was created
    responses:
      201:
        description: Movie-director record created successfully
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


@movie_director_blueprint.route(
    "/movie_director/<movie_id>/<director_id>", methods=["PUT"]
)
@validate(body=MovieDirectorDataModel)
def put_record(movie_id: int, director_id: int):
    """
    Updates a record by ID.

    ---
    tags:
      - Movie Director
    summary: Update a movie-director relationship
    description: A PUT handler that updates a movie-director record based on movie ID and director ID.
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie
      - in: path
        name: director_id
        type: integer
        required: true
        description: ID of the director
      - in: body
        name: body
        description: Movie-director relationship data to be updated
        schema:
          type: object
          required:
            - movie_id
            - director_id
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            director_id:
              type: integer
              description: ID of the director
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-director record was created
    responses:
      200:
        description: Movie-director record updated successfully
        schema:
          type: object
          properties:
            status:
              type: integer
              description: HTTP status code
            data:
              type: object
              description: Updated movie-director record
              properties:
                movie_id:
                  type: integer
                  description: ID of the movie
                director_id:
                  type: integer
                  description: ID of the director
                created_at:
                  type: string
                  format: date-time
                  description: Timestamp when the movie-director record was created
      400:
        description: Invalid input
      404:
        description: Record not found
      500:
        description: Internal server error
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_director_blueprint.route(
    "/movie_director/<movie_id>/<director_id>", methods=["DELETE"]
)
@validate()
def delete_movie_director(movie_id: int, director_id: int):
    """
    A DELETE handler
    Deletes a record by id.

    ---
    tags:
      - Movie Director
    summary: Delete a movie-director relationship by IDs
    description: A DELETE handler that deletes a movie-director record based on movie ID and director ID.
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie
      - in: path
        name: director_id
        type: integer
        required: true
        description: ID of the director
    responses:
      200:
        description: Movie-director record deleted successfully
        schema:
          type: object
          properties:
            status:
              type: integer
              description: HTTP status code
            data:
              type: object
              description: Confirmation of deletion
      404:
        description: Record not found
      500:
        description: Internal server error
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {director_id}"

    result = svc_delete(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/movie/<movie_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int):
    """
    A DELETE handler
    deletes all movie director by movie_id

    ---
    tags:
      - Movie Director
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie for which all associated directors should be deleted
        schema:
          example: 1
    responses:
      200:
        description: Successfully deleted all directors for the specified movie
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
                  description: Additional data related to the deletion
      404:
        description: Movie not found
      500:
        description: Internal server error
    """

    result = svc_delete_movie(movie_id)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_director_blueprint.route("/movie_director/exact", methods=["POST"])
@validate(body=SearchModel)
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match

    ---
    tags:
      - Movie Director
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
                    description: The field to search by (e.g., movie_id, director_id)
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
                      director_id:
                        type: integer
                        description: ID of the director
                      created_at:
                        type: string
                        format: date-time
                        description: Timestamp when the record was created
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
