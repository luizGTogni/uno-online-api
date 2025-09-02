from flask import Blueprint, Response, jsonify

user_router_bp = Blueprint("users_routers", __name__, url_prefix="/api/v1")

@user_router_bp.route("/", methods=["POST"])
def create_user() -> Response:
    return jsonify()
