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

    data: list[GenreDataModel | MessageModel]
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
    ---
    tags:
    - Genre
    summary: Retrieve a list of all genres
    responses:
      200:
        description: A list of all genres
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: The status of the request
                  example: "200"
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      genre_id:
                        type: integer
                        description: The genre ID
                        example: 1
                      name:
                        type: string
                        description: name of the genre
                        example: "comedy"
                      created_at:
                        type: string
                        description: When the genre was created
                        example: "2023-08-19T12:34:56Z"
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: The status of the request
                  example: "500"
                message:
                  type: string
                  description: Error message
                  example: "An error occurred while retrieving genres"
    """
    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/<genre_id>", methods=["GET"])
@validate()
def get_by_id(genre_id: int):
    """
    GET all by id
    ---
    tags:
      - Genre
    summary: Retrieve an genre by their ID
    parameters:
      - in: path
        name: genre_id
        required: true
        schema:
          type: integer
          example: 1
        description: The ID of the genre to retrieve
    responses:
      200:
        description: A specific genre's data by ID
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: The status of the request
                  example: "200"
                data:
                  type: object
                  properties:
                    genre_id:
                      type: integer
                      description: The genre's ID
                      example: 1
                    name:
                        type: string
                        description: name of the genre
                        example: "comedy"
                    created_at:
                      type: string
                      description: When the genre was created
                      example: "2023-08-19T12:34:56Z"
      500:
        description: Internal server error
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  description: The status of the request
                  example: "500"
                message:
                  type: string
                  description: Error message
                  example: "An error occurred while retrieving the genre"
    """

    result = svc_get_by_id(genre_id)
    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/create", methods=["POST"])
@validate(body=GenreItems)
def post_record():
    """
    Creates new record
    ---
    tags:
      - Genre
    parameters:
      - in: body
        name: body
        description: genre object that needs to be added
        schema:
          type: object
          required:
            - name
            - created_at
          properties:
            name:
              type: string
              description: genre name
            created_at:
              type: string
              description: genre created timestamp
    responses:
      201:
        description: genre created successfully
      400:
        description: Invalid input
      500:
        description: Internal server error
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
    ---
    tags:
      - Genre
    parameters:
      - in: path
        name: genre_id
        type: integer
        required: true
        description: ID of the genre to update
        schema:
          example: 1
      - in: body
        name: body
        description: genre object with updated details
        schema:
          type: object
          required:
            - name
            - created_at
          properties:
            name:
              type: string
              description: genre name
            created_at:
              type: string
              description: genre created timestamp
    responses:
      200:
        description: genre updated successfully
      400:
        description: Invalid input
      404:
        description: genre not found
      500:
        description: Internal server error
    """

    payload = request.get_json()

    result = svc_put(genre_id, payload)
    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/<genre_id>", methods=["DELETE"])
@validate()
def delete_record(genre_id: int):
    """
    deletes a record
    ---
    tags:
      - Genre
    parameters:
      - in: path
        name: genre_id
        schema:
          type: integer
          example: 1
        required: true
        description: ID of the genre to delete
    responses:
      200:
        description: genre successfully deleted
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "success"
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "error"
    """

    result = svc_delete(genre_id)
    return ResponseModel(status=result["status"])


@genre_blueprint.route("/genre/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    Searches records by in
    ---
    tags:
      - Genre
    parameters:
      - in: body
        name: body
        description: JSON object containing search criteria
        schema:
          type: object
          required:
            - field
            - values
          properties:
            field:
              type: string
              description: The field to search by (e.g., last_name)
            values:
              type: array
              description: List of values to search for
              items:
                type: object
                required:
                  - value
                properties:
                  value:
                    type: string
                    description: The exact value to search for
    responses:
      200:
        description: Exact search results returned successfully
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
                  description: List of genres matching the search criteria
                  items:
                    type: object
                    properties:
                      genre_id:
                        type: integer
                        description: ID of the genre
                      name:
                        type: string
                        description: genre name
                      created_at:
                        type: string
                        description: genre creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/like", methods=["POST"])
@validate(SearchModel)
def search_by_like():
    """
    Searches record by Like
    ---
    tags:
      - Genre
    parameters:
      - in: body
        name: body
        description: JSON object containing search criteria
        schema:
          type: object
          required:
            - fields
          properties:
            fields:
              type: array
              description: List of search criteria objects
              items:
                type: object
                required:
                  - field
                  - value
                properties:
                  field:
                    type: string
                    description: The field to search by (e.g., title, first_name, last_name)
                  value:
                    type: string
                    description: The exact value to search for
    responses:
      200:
        description: Exact search results returned successfully
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
                  description: List of genres matching the search criteria
                  items:
                    type: object
                    properties:
                      genre_id:
                        type: integer
                        description: ID of the genre
                      name:
                        type: string
                        description: genre name
                      created_at:
                        type: string
                        description: genre creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@genre_blueprint.route("/genre/exact", methods=["POST"])
@validate(SearchModel)
def search_by_exact():
    """
    Searches record by Like
    ---
    tags:
      - Genre
    parameters:
      - in: body
        name: body
        description: JSON object containing search criteria
        schema:
          type: object
          required:
            - fields
          properties:
            fields:
              type: array
              description: List of search criteria objects
              items:
                type: object
                required:
                  - field
                  - value
                properties:
                  field:
                    type: string
                    description: The field to search by (e.g., title, first_name, last_name)
                  value:
                    type: string
                    description: The exact value to search for
    responses:
      200:
        description: Exact search results returned successfully
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
                  description: List of genres matching the search criteria
                  items:
                    type: object
                    properties:
                      genre_id:
                        type: integer
                        description: ID of the genre
                      name:
                        type: string
                        description: genre name
                      created_at:
                        type: string
                        description: genre creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])
