from src.api import app
from src.core.config import settings

if __name__ == "__main__":
    app.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.APP_DEBUG,
        load_dotenv=True
    )
