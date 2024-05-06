import pytest
from faker import Faker
from blueprints.movie import service
from constants.constants import STATUS_OK


@pytest.fixture
def fields_payload():
    """
    creates fake field value data
    """
    faker_data = {}

    faker_data["fields"] = [{"field": "id", "value": 1}]

    return faker_data


@pytest.fixture
def in_payload():
    """
    fake in clause payload
    """
    faker_data = {}
    faker_data["field"] = "id"
    faker_data["values"] = [{"value": 1}, {"value": 2}]

    return faker_data


@pytest.fixture
def fake_data():
    """
    Returns fake data for movie table
    """

    fake = Faker()
    faker_data = {}
    faker_data["movie_id"] = fake.pyint()
    faker_data["title"] = fake.pystr(min_chars=0, max_chars=100)
    faker_data["description"] = fake.pystr(min_chars=0, max_chars=1000)
    faker_data["movie_year"] = fake.date()
    faker_data["rating"] = fake.pyfloat()
    faker_data["runtime"] = fake.pyfloat()
    faker_data["votes"] = fake.pyint()
    faker_data["revenue"] = fake.pyfloat()
    faker_data["metascore"] = fake.pyint()
    faker_data["created_at"] = fake.pystr()

    return faker_data


@pytest.fixture()
def fake_id():
    """returns fake id"""

    return "1"


def test_svc_get(mocker, fake_data):
    """
    GET service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores value in result variable
    result = service.svc_get()
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK  # asserts status code

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_get_by_id(mocker, fake_data, fake_id):
    """
    GET BY ID service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_get_by_id(fake_id)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_put(mocker, fake_data, fake_id):
    """
    PUT service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_put(fake_data, fake_id)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_post(mocker, fake_data):
    """
    POST service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_post(fake_data)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_delete(mocker, fake_data, fake_id):
    """
    DELETE service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_delete(fake_id)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_by_in(mocker, fake_data, in_payload):
    """
    IN Search service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_in_search(in_payload)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_by_like(mocker, fake_data, fields_payload):
    """
    LIKE search service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_like_search(fields_payload)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]


def test_svc_by_exact(mocker, fake_data, fields_payload):
    """
    EXACT search service test function
    """

    # mocks the "do_query" function in service.py file
    mocker_sql = mocker.patch.object(service, "do_query")
    # returns status and data from the mocked "do_query" function
    mocker_sql.return_value = {"status": STATUS_OK, "data": [fake_data]}

    # executes the function and stores data and status in result variable
    result = service.svc_exact_search(fields_payload)
    data = result["data"]
    status = result["status"]

    # asserts if the data returned is in form of a list
    assert isinstance(data, list)
    assert status == STATUS_OK

    # asserts data returned is matched with fake data
    assert data[0]["movie_id"] == fake_data["movie_id"]
    assert data[0]["title"] == fake_data["title"]
    assert data[0]["description"] == fake_data["description"]
    assert data[0]["movie_year"] == fake_data["movie_year"]
    assert data[0]["runtime"] == fake_data["runtime"]
    assert data[0]["rating"] == fake_data["rating"]
    assert data[0]["votes"] == fake_data["votes"]
    assert data[0]["revenue"] == fake_data["revenue"]
    assert data[0]["metascore"] == fake_data["metascore"]
    assert data[0]["created_at"] == fake_data["created_at"]
