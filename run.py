from src.api import app
from src.core.config import settings
from src.db.db_connection import db_connection_handler

if __name__ == "__main__":
    db_connection_handler.connect()
    app.run(
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        debug=settings.APP_DEBUG,
        load_dotenv=True
    )
