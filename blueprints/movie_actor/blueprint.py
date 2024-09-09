"""
blueprint for movie_actor
"""


import os

from datetime import date, datetime
from typing import Optional
from flask_pydantic import validate
from flask import Blueprint, request
from pydantic import BaseModel
from blueprints.movie_actor.service import (
    svc_delete,
    svc_delete_movie,
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

    ---
    tags:
      - Movie Actor
    summary: Get all movie-actor relationships
    description: A GET handler that retrieves all movie-actor records.
    responses:
      200:
        description: A list of movie-actor relationships
        schema:
          type: array
          items:
            type: object
            properties:
              movie_id:
                type: integer
                description: ID of the movie
              actor_id:
                type: integer
                description: ID of the actor
              created_at:
                type: string
                format: date-time
                description: Timestamp when the movie-actor record was created
      404:
        description: No records found
      500:
        description: Internal server error
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/<movie_id>/<actor_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int, actor_id: int):
    """
    GET records by ID

    ---
    tags:
      - Movie Actor
    summary: Get movie-actor relationship by IDs
    description: A GET handler that retrieves a movie-actor record based on movie ID and actor ID.
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie
      - in: path
        name: actor_id
        type: integer
        required: true
        description: ID of the actor
    responses:
      200:
        description: Movie-actor relationship record
        schema:
          type: object
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            actor_id:
              type: integer
              description: ID of the actor
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-actor record was created
      404:
        description: Record not found
      500:
        description: Internal server error
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

    ---
    tags:
      - Movie Actor
    summary: Create a new movie-actor relationship
    description: A POST handler that creates a new movie-actor record.
    parameters:
      - in: body
        name: body
        description: Movie-actor relationship data to be created
        schema:
          type: object
          required:
            - movie_id
            - actor_id
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            actor_id:
              type: integer
              description: ID of the actor
            created_at:
              type: string
              description: Timestamp when the movie-actor record was created
    responses:
      201:
        description: Movie-actor record created successfully
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


@movie_actor_blueprint.route("/movie_actor/<movie_id>/<actor_id>", methods=["PUT"])
@validate(body=MovieActorDataModel)
def put_record(movie_id: int, actor_id: int):
    """
    Updates a record

    ---
    tags:
      - Movie Actor
    summary: Update a movie-actor relationship
    description: A PUT handler that updates a movie-actor record based on movie ID and actor ID.
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie
      - in: path
        name: actor_id
        type: integer
        required: true
        description: ID of the actor
      - in: body
        name: body
        description: Movie-actor relationship data to be updated
        schema:
          type: object
          required:
            - movie_id
            - actor_id
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            actor_id:
              type: integer
              description: ID of the actor
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-actor record was created
    responses:
      200:
        description: Movie-actor record updated successfully
        schema:
          type: object
          properties:
            status:
              type: integer
              description: HTTP status code
            data:
              type: object
              description: Updated movie-actor record
              properties:
                movie_id:
                  type: integer
                  description: ID of the movie
                actor_id:
                  type: integer
                  description: ID of the actor
                created_at:
                  type: string
                  format: date-time
                  description: Timestamp when the movie-actor record was created
      400:
        description: Invalid input
      404:
        description: Record not found
      500:
        description: Internal server error
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {actor_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/<movie_id>/<actor_id>", methods=["DELETE"])
@validate()
def delete_movie_actor(movie_id: int, actor_id: int):
    """
    A DELETE handler. Deletes a record by movie_id and actor_id

    ---
    tags:
      - Movie Actor
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie to delete the actor from
      - in: path
        name: actor_id
        type: integer
        required: true
        description: ID of the actor to be deleted from the movie
    responses:
      200:
        description: Successfully deleted the movie-actor relationship
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
        description: Movie or actor not found
      500:
        description: Internal server error
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {actor_id}"

    result = svc_delete(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_actor_blueprint.route("/movie_actor/movie/<movie_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int):
    """
    A DELETE handler. deletes all movie actors by movie_id

    ---
    tags:
      - Movie Actor
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie for which all associated actors should be deleted
        schema:
          example: 1
    responses:
      200:
        description: Successfully deleted all actors for the specified movie
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


@movie_actor_blueprint.route("/movie_actor/exact", methods=["POST"])
@validate(body=SearchModel)
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match

    ---
    tags:
      - Movie Actor
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
                    description: The field to search by (e.g., title, director)
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
                      actor_id:
                        type: integer
                        description: ID of the actor
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
