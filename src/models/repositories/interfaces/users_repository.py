from abc import ABC, abstractmethod
from typing import Union
from src.models.entities.user import User
from src.schemas.user import UserCreate

class IUsersRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: str) -> Union[User, None]:
        pass

    @abstractmethod
    def create(self, user_data: UserCreate) -> None:
        pass
