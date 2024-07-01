"""movie_review Tests"""

import pytest
from faker import Faker
from blueprints.movie_review import service
from constants.constants import STATUS_OK


@pytest.fixture()
def in_payload():
    """
    fake in clause payload
    """
    faker_data = {}
    faker_data["field"] = "id"
    faker_data["values"] = [{"value": 1}, {"value": 2}]

    return faker_data


@pytest.fixture()
def fields_payload():
    """
    creates fake field value data
    """
    faker_data = {}

    faker_data["fields"] = [{"field": "id", "value": 1}]

    return faker_data


@pytest.fixture()
def fake_data():
    """
    Creates fake data
    """

    fake = Faker()
    faker_data = {}
    faker_data["movie_id"] = fake.pyint()
    faker_data["review_id"] = fake.pyint()
    faker_data["review"] = fake.pyint()
    faker_data["created_at"] = fake.pystr()

    return faker_data


@pytest.fixture()
def fake_id():
    """
    returns fake id
    """

    return "1"


@pytest.fixture()
def fake_ids():
    """
    returns fake ids
    """

    return "1, 2"


def test_svc_get(mocker, fake_data):
    """
    GET service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_get()
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_get_by_id(mocker, fake_data, fake_ids):
    """
    GET by ID service test function
    """
    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_get_by_id(fake_ids)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_post(mocker, fake_data):
    """
    POST service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_post(fake_data)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_put(mocker, fake_data, fake_id):
    """
    PUT service test function
    """
    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_put(fake_id, fake_data)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_delete(mocker, fake_data, fake_ids):
    """
    DELETE service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_delete(fake_ids)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_in_search(mocker, in_payload, fake_data):
    """
    IN search test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_in_search(in_payload)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_exact_search(mocker, fields_payload, fake_data):
    """
    EXACT search test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_exact_search(fields_payload)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["review_id"] == fake_data["review_id"]
    assert data[0]["review"] == fake_data["review"]
    assert data[0]["created_at"] == fake_data["created_at"]
