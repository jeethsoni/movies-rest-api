"""
blueprint for actor table
"""

import os
from datetime import date, datetime
from flask import Blueprint, request
from pydantic import BaseModel
from typing import Optional
from flask_pydantic import validate

from blueprints.actor.service import (
    svc_get,
    svc_get_by_id,
    svc_in_search,
    svc_post,
    svc_put,
    svc_delete,
    svc_exact_search,
    svc_like_search,
)


class ActorItems(BaseModel):
    """
    Actor Items
    """

    first_name: str
    last_name: str
    age: int
    gender: str
    created_at: Optional[str]


class ActorDataModel(BaseModel):
    """
    Actor Data Model
    """

    actor_id: int
    first_name: str
    last_name: str
    age: int
    gender: str
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
    data: list[ActorDataModel | MessageModel]


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
    Value Model
    """

    value: int | str | date | float


class InModel(BaseModel):
    """
    In Model
    """

    field: str
    values: list[ValueModel]


class PostModel(BaseModel):
    """Post model status"""

    status: int | str


version = os.getenv("VERSION")
actor_blueprint = Blueprint("actor", __name__, url_prefix=version)


@actor_blueprint.route("/actor/actors", methods=["GET"])
@validate()
def get_all_records():
    """
    A GET handler. Returns all records for actor.
    ---
    tags:
    - Actor
    summary: Retrieve a list of all actors
    responses:
      200:
        description: A list of all actors
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
                      actor_id:
                        type: integer
                        description: The actor's ID
                        example: 1
                      first_name:
                        type: string
                        description: The actor's first name
                        example: "John"
                      last_name:
                        type: string
                        description: The actor's last name
                        example: "Doe"
                      age:
                        type: integer
                        description: The actor's age
                        example: 35
                      gender:
                        type: string
                        description: The actor's gender
                        example: "Male"
                      created_at:
                        type: string
                        description: When the actor was created
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
                  example: "An error occurred while retrieving actors"
    """

    result = svc_get()
    return ResponseModel(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/<actor_id>", methods=["GET"])
@validate()
def get_by_id(actor_id: int):
    """
    A GET handler. Returns record by a given identifier.
    ---
    tags:
      - Actor
    summary: Retrieve an actor by their ID
    parameters:
      - in: path
        name: actor_id
        required: true
        schema:
          type: integer
          example: 1
        description: The ID of the actor to retrieve
    responses:
      200:
        description: A specific actor's data by ID
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
                    actor_id:
                      type: integer
                      description: The actor's ID
                      example: 1
                    first_name:
                      type: string
                      description: The actor's first name
                      example: "John"
                    last_name:
                      type: string
                      description: The actor's last name
                      example: "Doe"
                    age:
                      type: integer
                      description: The actor's age
                      example: 35
                    gender:
                      type: string
                      description: The actor's gender
                      example: "Male"
                    created_at:
                      type: string
                      description: When the actor was created
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
                  example: "An error occurred while retrieving the actor"
    """

    result = svc_get_by_id(actor_id)
    return ResponseModel(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/create", methods=["POST"])
@validate(body=ActorItems)
def post_actor():
    """
    A POST handler. Creates a new actor record
    ---
    tags:
      - Actor
    parameters:
      - in: body
        name: body
        description: Actor object that needs to be added
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
              description: First name of the actor
            last_name:
              type: string
              description: Last name of the actor
            age:
              type: integer
              description: Age of the actor
            gender:
              type: string
              description: Gender of the actor
            created_at:
              type: string
              description: actor created timestamp
    responses:
      201:
        description: Actor created successfully
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


@actor_blueprint.route("/actor/<actor_id>", methods=["PUT"])
@validate(body=ActorItems)
def put_actor(actor_id: int):
    """
    A PUT handler for actor table
    ---
    tags:
      - Actor
    parameters:
      - in: path
        name: actor_id
        type: integer
        required: true
        description: ID of the actor to update
        schema:
          example: 1
      - in: body
        name: body
        description: Actor object with updated details
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
              description: First name of the actor
            last_name:
              type: string
              description: Last name of the actor
            age:
              type: integer
              description: Age of the actor
            gender:
              type: string
              description: Gender of the actor
            created_at:
              type: string
              description: Actor created timestamp
    responses:
      200:
        description: Actor updated successfully
      400:
        description: Invalid input
      404:
        description: Actor not found
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_put(payload, actor_id)

    return ResponseModel(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/<actor_id>", methods=["DELETE"])
@validate()
def delete_actor(actor_id: int):
    """
    A DELETE handle
    ---
    tags:
      - Actor
    parameters:
      - in: path
        name: actor_id
        schema:
          type: integer
          example: 1
        required: true
        description: ID of the actor to delete
    responses:
      200:
        description: Actor successfully deleted
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

    result = svc_delete(actor_id)
    return ResponseModel(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/exact", methods=["POST"])
@validate(body=SearchModel)
def search_by_exact():
    """
    Exact search
    ---
    tags:
      - Actor
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
                  description: List of actors matching the search criteria
                  items:
                    type: object
                    properties:
                      actor_id:
                        type: integer
                        description: ID of the actor
                      first_name:
                        type: string
                        description: First name of the actor
                      last_name:
                        type: string
                        description: Last name of the actor
                      age:
                        type: integer
                        description: Age of the actor
                      gender:
                        type: string
                        description: Gender of the actor
                      created_at:
                        type: string
                        description: Actor creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_exact_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/like", methods=["POST"])
@validate(body=SearchModel)
def search_by_like():
    """
    Like Search
    ---
    tags:
      - Actor
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
                  description: List of actors matching the search criteria
                  items:
                    type: object
                    properties:
                      actor_id:
                        type: integer
                        description: ID of the actor
                      first_name:
                        type: string
                        description: First name of the actor
                      last_name:
                        type: string
                        description: Last name of the actor
                      age:
                        type: integer
                        description: Age of the actor
                      gender:
                        type: string
                        description: Gender of the actor
                      created_at:
                        type: string
                        description: Actor creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_like_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])


@actor_blueprint.route("/actor/in", methods=["POST"])
@validate(body=InModel)
def search_by_in():
    """
    In Search
    ---
    tags:
      - Actor
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
                  description: List of actors matching the search criteria
                  items:
                    type: object
                    properties:
                      actor_id:
                        type: integer
                        description: ID of the actor
                      first_name:
                        type: string
                        description: First name of the actor
                      last_name:
                        type: string
                        description: Last name of the actor
                      age:
                        type: integer
                        description: Age of the actor
                      gender:
                        type: string
                        description: Gender of the actor
                      created_at:
                        type: string
                        description: Actor creation timestamp
      500:
        description: Internal server error
    """

    payload = request.get_json()
    result = svc_in_search(payload)

    return ResponseModel(status=result["status"], data=result["data"])
