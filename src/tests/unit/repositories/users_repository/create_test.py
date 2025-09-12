from uuid import uuid4

import pytest
from src.models.repositories import UsersRepository
from src.schemas.user import UserCreate
from src.tests.unit.repositories.mock import DBMocker

user_id = uuid4()

class DBConnectionHandlerMock(DBMocker):
    def __init__(self, mocker) -> None:
        self.session = mocker.Mock()

@pytest.mark.unit
def test_create(mocker):
    db_connection = DBConnectionHandlerMock(mocker)
    repository = UsersRepository(db_connection)

    user = UserCreate(
        name="John Doe",
        username="johndoe",
        email="johndoe@example.com",
        password="123456"
    )

    repository.create(user)

    db_connection.session.add.assert_called_once()
    db_connection.session.commit.assert_called_once()
