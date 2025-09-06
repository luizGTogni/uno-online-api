from uuid import uuid4

import pytest
from src.models.entities.user import User
from src.models.repositories import UsersRepository
from src.tests.unit.repositories.mock import DBMocker, MockUser

user_id = uuid4()

class DBConnectionHandlerMock(DBMocker):
    def __init__(self, mocker) -> None:
        self.session = mocker.Mock()
        self.session.get.return_value = MockUser.create(user_id)

class DBConnectionHandlerNotFoundMock(DBMocker):
    def __init__(self, mocker) -> None:
        self.session = mocker.Mock()
        self.session.get.return_value = None

@pytest.mark.unit
def test_find_by_id(mocker):
    db_connection = DBConnectionHandlerMock(mocker)
    repository = UsersRepository(db_connection)
    response = repository.find_by_id(user_id)

    db_connection.session.get.assert_called_once_with(User, user_id)

    assert isinstance(response, User)
    assert response.id == user_id
    assert response.name == "John Doe"
    assert response.username == "johndoe"
    assert response.email == "johndoe@example.com"
    assert response.level == 10
    assert response.rating == 52

@pytest.mark.unit
def test_find_by_id_exception_not_result_found(mocker):
    db_connection = DBConnectionHandlerNotFoundMock(mocker)
    repository = UsersRepository(db_connection)
    response = repository.find_by_id("999")

    assert response is None
