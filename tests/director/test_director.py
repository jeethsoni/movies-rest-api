import pytest
from faker import Faker
from blueprints.director import service
from constants.constants import STATUS_OK


@pytest.fixture()
def fake_id():
    """
    returns fake id
    """

    return "1"


@pytest.fixture()
def fake_data():
    """
    creates fake data
    """

    fake = Faker()
    faker_data = {}
    faker_data["director_id"] = fake.pyint()
    faker_data["first_name"] = fake.pystr(min_chars=0, max_chars=100)
    faker_data["last_name"] = fake.pystr(min_chars=0, max_chars=100)
    faker_data["created_at"] = fake.pystr()

    return faker_data


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

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_get_by_id(mocker, fake_data, fake_id):
    """
    GET service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_get_by_id(fake_id)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
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

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_put(mocker, fake_data, fake_id):
    """
    POST service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_put(fake_data, fake_id)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_delete(mocker, fake_data, fake_id):
    """
    POST service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_delete(fake_id)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_by_in(mocker, fake_data, in_payload):
    """
    POST service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_in_search(in_payload)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_by_like(mocker, fake_data, fields_payload):
    """
    POST service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_like_search(fields_payload)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_by_exact(mocker, fake_data, fields_payload):
    """
    POST service test function
    """

    mocker_sql = mocker.patch.object(service, "do_query")
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    result = service.svc_exact_search(fields_payload)
    data = result["data"]
    status = result["status"]

    assert isinstance(data, list)
    assert status == STATUS_OK

    assert data[0]["director_id"] == fake_data["director_id"]
    assert data[0]["first_name"] == fake_data["first_name"]
    assert data[0]["last_name"] == fake_data["last_name"]
    assert data[0]["created_at"] == fake_data["created_at"]
