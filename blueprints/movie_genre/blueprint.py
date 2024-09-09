"""
blueprint for movie_genre
"""


import os
from datetime import date, datetime
from typing import Optional
from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate
from blueprints.movie_genre.service import (
    svc_delete,
    svc_delete_movie,
    svc_exact_search,
    svc_get,
    svc_get_by_id,
    svc_post,
    svc_put,
)


class MovieGenreDataModel(BaseModel):
    """
    Genre Data Model
    """

    movie_id: int
    genre_id: int
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

    data: list[MovieGenreDataModel | MessageModel]
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
movie_genre_blueprint = Blueprint("movie_genre", __name__, url_prefix=version)


@movie_genre_blueprint.route("/movie_genre/movie_genres", methods=["GET"])
@validate()
def get_all_records():
    """
    Get all movie_genre records

    ---
    tags:
      - Movie Genre
    summary: Retrieve all movie-genre relationships
    description: A GET handler that retrieves all movie-genre records.
    responses:
      200:
        description: Successfully retrieved all movie-genre records
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
                  description: List of movie-genre records
                  items:
                    type: object
                    properties:
                      movie_id:
                        type: integer
                        description: ID of the movie
                      genre_id:
                        type: integer
                        description: ID of the genre
                      created_at:
                        type: string
                        format: date-time
                        description: Timestamp when the record was created
      500:
        description: Internal server error
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/<movie_id>/<genre_id>", methods=["GET"])
@validate()
def get_by_id(movie_id: int, genre_id: int):
    """
    GET records by ID

    ---
    tags:
      - Movie Genre
    summary: Retrieve a movie-genre relationship by movie ID and genre ID
    description: A GET handler that retrieves a specific movie-genre record based on the provided movie ID and genre ID.
    parameters:
      - in: path
        name: movie_id
        type: integer
        required: true
        description: ID of the movie
      - in: path
        name: genre_id
        type: integer
        required: true
        description: ID of the genre
    responses:
      200:
        description: Successfully retrieved the movie-genre record
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
                  properties:
                    movie_id:
                      type: integer
                      description: ID of the movie
                    genre_id:
                      type: integer
                      description: ID of the genre
                    created_at:
                      type: string
                      format: date-time
                      description: Timestamp when the record was created
      404:
        description: Record not found
      500:
        description: Internal server error
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {genre_id}"

    result = svc_get_by_id(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/create", methods=["POST"])
@validate(body=MovieGenreDataModel)
def post_record():
    """
    POST a new record

    ---
    tags:
      - Movie Genre
    summary: Create a new movie-genre relationship
    description: A POST handler that creates a new movie-genre record.
    parameters:
      - in: body
        name: body
        description: Movie-genre relationship data to be created
        schema:
          type: object
          required:
            - movie_id
            - genre_id
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            genre_id:
              type: integer
              description: ID of the genre
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-genre record was created
    responses:
      201:
        description: Movie-genre record created successfully
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


@movie_genre_blueprint.route("/movie_genre/<movie_id>/<genre_id>", methods=["PUT"])
@validate(body=MovieGenreDataModel)
def put_record(movie_id: int, genre_id: int):
    """
    Updates a record
    ---
    tags:
      - Movie Genre
    summary: Update a movie-genre relationship by ID
    description: A PUT handler to update an existing movie-genre record.
    parameters:
      - in: path
        name: movie_id
        required: true
        schema:
          type: integer
        description: ID of the movie
      - in: path
        name: genre_id
        required: true
        schema:
          type: integer
        description: ID of the genre
      - in: body
        name: body
        description: Movie-genre relationship data to update
        schema:
          type: object
          required:
            - movie_id
            - genre_id
          properties:
            movie_id:
              type: integer
              description: ID of the movie
            genre_id:
              type: integer
              description: ID of the genre
            created_at:
              type: string
              format: date-time
              description: Timestamp when the movie-genre record was created
    responses:
      200:
        description: Successfully updated the movie-genre record
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: integer
                  description: HTTP status code
                data:
                  type: object
                  description: The updated movie-genre record
      400:
        description: Invalid input
      404:
        description: Record not found
      500:
        description: Internal server error
    """
    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {genre_id}"

    payload = request.get_json()
    result = svc_put(pkeys, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/<movie_id>/<genre_id>", methods=["DELETE"])
@validate()
def delete_movie_genre(movie_id: int, genre_id: int):
    """
    A DELETE handler
    Deletes a record by id
    ---
    tags:
      - Movie Genre
    summary: Delete a movie-genre relationship by ID
    description: A DELETE handler that deletes a movie-genre record by movie_id and genre_id.
    parameters:
      - in: path
        name: movie_id
        required: true
        schema:
          type: integer
        description: ID of the movie
      - in: path
        name: genre_id
        required: true
        schema:
          type: integer
        description: ID of the genre
    responses:
      200:
        description: Movie-genre record deleted successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: integer
                  description: HTTP status code
                data:
                  type: object
                  description: The deleted movie-genre record details
      400:
        description: Invalid input
      404:
        description: Record not found
      500:
        description: Internal server error
    """

    pkeys = f"{movie_id}"
    pkeys = f"{pkeys}, {genre_id}"

    result = svc_delete(pkeys)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/movie/<movie_id>", methods=["DELETE"])
@validate()
def delete_movie(movie_id: int):
    """
    A DELETE handler
    deletes all movie genres by movie_id
    ---
    tags:
      - Movie Genre
    summary: Delete all movie-genre relationships for a given movie ID
    description: A DELETE handler that deletes all genre associations for a specific movie by its ID.
    parameters:
      - in: path
        name: movie_id
        required: true
        schema:
          type: integer
        description: ID of the movie whose genres will be deleted
    responses:
      200:
        description: Successfully deleted all genres associated with the movie
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: integer
                  description: HTTP status code
                data:
                  type: object
                  description: Details of the deleted movie-genre records
      400:
        description: Invalid input
      404:
        description: Movie or genres not found
      500:
        description: Internal server error
    """

    result = svc_delete_movie(movie_id)
    return ResponseModel(status=result["status"], data=result["data"])


@movie_genre_blueprint.route("/movie_genre/exact", methods=["POST"])
@validate(body=SearchModel)
def search_exact():
    """
    EXACT Search
    Retrives all records from movies for exact value match
    ---
    tags:
      - Movie Genre
    summary: Search movie_genre records for an exact value match
    description: A POST handler that retrieves all movie_genre records that match the exact values provided.
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
                    description: The field to search by (e.g., movie_id, genre_id)
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
                      genre_id:
                        type: integer
                        description: ID of the genre
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
