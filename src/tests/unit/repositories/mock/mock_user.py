from src.models.entities import User


class MockUser:
    @staticmethod
    def create(user_id: str) -> User:
        return User(
            id=user_id,
            name="John Doe",
            username="johndoe",
            email="johndoe@example.com",
            level=10,
            rating=52,
        )
