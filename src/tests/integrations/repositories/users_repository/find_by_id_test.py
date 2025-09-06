from uuid import  uuid4
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.models.entities import User
from src.models.repositories.users_repository import UsersRepository

user_id = uuid4()

class DBConnectionHandlerMock:
    def __init__(self) -> None:
        self.__engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(bind=self.__engine)
        self.__session_maker = sessionmaker(bind=self.__engine)
        self.session = None

    def __enter__(self) -> "DBConnectionHandlerMock":
        self.session = self.__session_maker()

        user = User(
            id=user_id,
            name="John Doe",
            username="johndoe",
            email="johndoe@example.com",
            password="123456",
        )

        self.session.add(user)
        self.session.commit()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()
        Base.metadata.drop_all(bind=self.__engine)
        self.__engine.dispose()

@pytest.mark.integration
def test_find_by_id_integration():
    db_connection = DBConnectionHandlerMock()

    repository = UsersRepository(db_connection)
    response = repository.find_by_id(user_id)

    assert isinstance(response, User)
    assert response.id == user_id
    assert response.username == "johndoe"
    assert response.password == "123456"
    assert response.role == "player"
    assert response.level == 1
    assert response.rating == 0

@pytest.mark.integration
def test_find_by_id_exception_not_result_found_integration():
    db_connection = DBConnectionHandlerMock()

    repository = UsersRepository(db_connection)
    response = repository.find_by_id(uuid4())

    assert response is None
