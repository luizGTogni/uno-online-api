from typing import Union
from sqlalchemy.exc import NoResultFound
from src.db.db_connection import DBConnectionHandler
from src.schemas.user import UserCreate
from src.models.entities import User
from .interfaces import IUsersRepository

class UsersRepository(IUsersRepository):
    def __init__(self, db_connection: DBConnectionHandler) -> None:
        self.__db_connection = db_connection

    def find_by_id(self, user_id: str) -> Union[User, None]:
        with self.__db_connection as db:
            try:
                user = db.session.get(User, user_id)
                return user
            except NoResultFound:
                return None
            except Exception as e:
                raise e

    def create(self, user_data: UserCreate) -> dict:
        with self.__db_connection as db:
            try:
                user = User(**user_data.model_dump())
                db.session.add(user)
                db.session.commit()
                return user.to_dict()
            except Exception as e:
                print("erro")
                db.session.rollback()
                raise e
