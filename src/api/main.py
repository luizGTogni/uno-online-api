from flask import Flask
from flask_cors import CORS
from .v1.routes import user_router_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(user_router_bp)
## api_router.include_router(api_router, prefix="/api/v1")
