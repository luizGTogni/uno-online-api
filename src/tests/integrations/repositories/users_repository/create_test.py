from uuid import  uuid4
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.models.entities.user import UserRoleEnum
from src.models.repositories.users_repository import UsersRepository
from src.schemas.user import UserCreate

user_id = uuid4()

class DBConnectionHandlerMock:
    def __init__(self) -> None:
        self.__engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(bind=self.__engine)
        self.__session_maker = sessionmaker(bind=self.__engine)
        self.session = None

    def __enter__(self) -> "DBConnectionHandlerMock":
        self.session = self.__session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()
        Base.metadata.drop_all(bind=self.__engine)
        self.__engine.dispose()

@pytest.mark.integration
def test_create_integration():
    db_connection = DBConnectionHandlerMock()
    repository = UsersRepository(db_connection)

    user = UserCreate(
        name="John Doe",
        username="johndoe",
        email="johndoe@example.com",
        password="123456"
    )

    response = repository.create(user)

    assert response["username"] == "johndoe"
    assert response["role"] == UserRoleEnum.PLAYER
    assert response["level"] == 1
    assert response["rating"] == 0
