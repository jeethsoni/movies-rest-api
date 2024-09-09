"""Director table blueprint"""

from datetime import date, datetime
import os
from typing import Optional
from flask import Blueprint, request
from pydantic import BaseModel
from flask_pydantic import validate

from blueprints.director.service import (
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_post,
    svc_put,
    svc_delete,
    svc_exact_search,
    svc_like_search,
)


class DirectorItems(BaseModel):
    """
    Items
    """

    first_name: str
    last_name: str
    created_at: Optional[str]


class DirectorDataModel(BaseModel):
    """
    Data Model
    """

    director_id: int
    first_name: str
    last_name: str
    created_at: Optional[str | datetime | date]


class MessageModel(BaseModel):
    """
    Message model
    """

    message: str


class ResponseModel(BaseModel):
    """
    Response model
    """

    status: int
    data: list[DirectorDataModel | MessageModel]


class FieldValueModel(BaseModel):
    """
    Field and value model
    """

    field: str
    value: int | str | date | float


class SearchModel(BaseModel):
    """
    Search model
    """

    fields: list[FieldValueModel]


class ValueModel(BaseModel):
    """
    Value model
    """

    value: int | str | date | float


class InModel(BaseModel):
    """
    In model
    """

    field: str
    values: list[ValueModel]


class PostModel(BaseModel):
    """Post model status"""

    status: int | str


version = os.getenv("VERSION")
director_blueprint = Blueprint("director", __name__, url_prefix=version)


@director_blueprint.route("/director/directors", methods=["GET"])
@validate()
def get_all_records():
    """
    A GET handler. Returns all records for director.
    ---
    tags:
    - Director
    summary: Retrieve a list of all directors
    responses:
      200:
        description: A list of all directors
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
                      director_id:
                        type: integer
                        description: The director's ID
                        example: 1
                      first_name:
                        type: string
                        description: The director's first name
                        example: "John"
                      last_name:
                        type: string
                        description: The director's last name
                        example: "Doe"
                      created_at:
                        type: string
                        description: When the director was created
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
                  example: "An error occurred while retrieving directors"
    """
    result = svc_get()

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/<director_id>", methods=["GET"])
@validate()
def get_by_id(director_id: int):
    """
    A GET handler. Returns record by a given identifier.
    ---
    tags:
      - Director
    summary: Retrieve an director by their ID
    parameters:
      - in: path
        name: director_id
        required: true
        schema:
          type: integer
          example: 1
        description: The ID of the director to retrieve
    responses:
      200:
        description: A specific director's data by ID
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
                    director_id:
                      type: integer
                      description: The director's ID
                      example: 1
                    first_name:
                      type: string
                      description: The director's first name
                      example: "John"
                    last_name:
                      type: string
                      description: The director's last name
                      example: "Doe"
                    age:
                      type: integer
                      description: The director's age
                      example: 35
                    gender:
                      type: string
                      description: The director's gender
                      example: "Male"
                    created_at:
                      type: string
                      description: When the director was created
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
                  example: "An error occurred while retrieving the director"
    """

    result = svc_get_by_id(director_id)
    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/create", methods=["POST"])
@validate(body=DirectorItems)
def post_director():
    """
    A POST handler. Creates a new movie record
    ---
    tags:
      - Director
    parameters:
      - in: body
        name: body
        description: director object that needs to be added
        schema:
          type: object
          required:
            - first_name
            - last_name
            - age
            - gender
            - created_at
          properties:
            first_name:
              type: string
              description: First name of the director
            last_name:
              type: string
              description: Last name of the director
            created_at:
              type: string
              description: director created timestamp
    responses:
      201:
        description: director created successfully
      400:
        description: Invalid input
      500:
        description: Internal server error
    """
    # request object
    payload = request.get_json()

    result = svc_post(payload)

    if result["status"] == 200:
        status = 201
    else:
        status = result["status"]

    return PostModel(status=status)


@director_blueprint.route("/director/<director_id>", methods=["PUT"])
@validate(body=DirectorItems)
def put_director(director_id: int):
    """
    A PUT handler for director table
    ---
    tags:
      - Director
    parameters:
      - in: path
        name: director_id
        type: integer
        required: true
        description: ID of the director to update
        schema:
          example: 1
      - in: body
        name: body
        description: director object with updated details
        schema:
          type: object
          required:
            - first_name
            - last_name
            - age
            - gender
            - created_at
          properties:
            first_name:
              type: string
              description: First name of the director
            last_name:
              type: string
              description: Last name of the director
            created_at:
              type: string
              description: director created timestamp
    responses:
      200:
        description: director updated successfully
      400:
        description: Invalid input
      404:
        description: director not found
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_put(payload, director_id)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/<director_id>", methods=["DELETE"])
@validate()
def delete_director(director_id: int):
    """
    A DELETE handle
    ---
    tags:
      - Director
    parameters:
      - in: path
        name: director_id
        schema:
          type: integer
          example: 1
        required: true
        description: ID of the director to delete
    responses:
      200:
        description: director successfully deleted
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

    result = svc_delete(director_id)
    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/exact", methods=["POST"])
@validate(body=SearchModel)
def search_by_exact():
    """
    Exact search
    ---
    tags:
      - Director
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
                  description: List of directors matching the search criteria
                  items:
                    type: object
                    properties:
                      director_id:
                        type: integer
                        description: ID of the director
                      first_name:
                        type: string
                        description: First name of the director
                      last_name:
                        type: string
                        description: Last name of the director
                      created_at:
                        type: string
                        description: director creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/like", methods=["POST"])
@validate(body=SearchModel)
def search_by_like():
    """
    Like Search
    ---
    tags:
      - Director
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
                  description: List of directors matching the search criteria
                  items:
                    type: object
                    properties:
                      director_id:
                        type: integer
                        description: ID of the director
                      first_name:
                        type: string
                        description: First name of the director
                      last_name:
                        type: string
                        description: Last name of the director
                      created_at:
                        type: string
                        description: director creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@director_blueprint.route("/director/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    In Search
    ---
    tags:
      - Director
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
                  description: List of directors matching the search criteria
                  items:
                    type: object
                    properties:
                      director_id:
                        type: integer
                        description: ID of the director
                      first_name:
                        type: string
                        description: First name of the director
                      last_name:
                        type: string
                        description: Last name of the director
                      created_at:
                        type: string
                        description: director creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])
