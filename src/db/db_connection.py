from typing import Union
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings

class DBConnectionHandler:
    def __init__(self) -> None:
        self.__conn_string = settings.DATABASE_URL
        self.__engine = None
        self.session = None

    def connect(self) -> None:
        self.__engine = create_engine(self.__conn_string)

    def get_engine(self) -> Union[Engine, None]:
        return self.__engine

    def __enter__(self) -> "DBConnectionHandler":
        session_maker = sessionmaker()
        self.session = session_maker(bind=self.__engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if isinstance(self.session, Session):
            self.session.close()

db_connection_handler = DBConnectionHandler()
