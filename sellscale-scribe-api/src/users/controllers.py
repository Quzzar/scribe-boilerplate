from flask import Blueprint, request, jsonify
from src.authentication.request_helpers import get_request_parameter
from src.authentication.decorators import require_user
from src.users.services import sign_in_user, auth_user, update_user, get_user, refresh_user_token
from app import limiter

USERS_BLUEPRINT = Blueprint("user", __name__)


@USERS_BLUEPRINT.route("/", methods=["GET"])
@require_user
def get_user_endpoint(user_id: str):
    
    user = get_user(user_id)

    return jsonify({
        "status": "success",
        "data": user
    }), 200


@USERS_BLUEPRINT.route("/", methods=["PATCH"])
@require_user
def update_user_endpoint(user_id: str):
    
    name = get_request_parameter("name", request, json=True, required=False, parameter_type=str, default_value='')
    role = get_request_parameter("role", request, json=True, required=False, parameter_type=str, default_value='')
    company_name = get_request_parameter("company_name", request, json=True, required=False, parameter_type=str, default_value='')
    what_you_do = get_request_parameter("what_you_do", request, json=True, required=False, parameter_type=str, default_value='')
    buys_your_product = get_request_parameter("buys_your_product", request, json=True, required=False, parameter_type=str, default_value='')
    why_buy = get_request_parameter("why_buy", request, json=True, required=False, parameter_type=str, default_value='')
    fun_facts = get_request_parameter("fun_facts", request, json=True, required=False, parameter_type=str, default_value='')
    
    user = update_user(user_id, name, role, company_name, what_you_do, buys_your_product, why_buy, fun_facts)

    return jsonify({
        "status": "success",
        "data": user
    }), 200


@USERS_BLUEPRINT.route("/signin", methods=["POST"])
def sign_in_user_endpoint():
    
    email = get_request_parameter("email", request, json=True, required=True, parameter_type=str)
    
    success = sign_in_user(email)

    if success:
        return jsonify({
            "status": "success",
            "data": {}
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Failed to send OTP."
        }), 400


@USERS_BLUEPRINT.route("/auth", methods=["POST"])
#@limiter.limit("5/hour")
def auth_user_endpoint():
    
    access_token = get_request_parameter("access_token", request, json=True, required=True, parameter_type=str)
    refresh_token = get_request_parameter("refresh_token", request, json=True, required=True, parameter_type=str)
    expires_in = get_request_parameter("expires_in", request, json=True, required=True, parameter_type=int)
    
    user_id, access_token, refresh_token, created_user = auth_user(access_token, refresh_token)

    return jsonify({
        "status": "success",
        "data": {
            "user_id": user_id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "created_user": created_user
        }
    }), 200


@USERS_BLUEPRINT.route("/refresh_token", methods=["POST"])
def refresh_token_endpoint():
    
    refresh_token = get_request_parameter("refresh_token", request, json=True, required=True, parameter_type=str)
    
    access_token, refresh_token = refresh_user_token(refresh_token)

    return jsonify({
        "status": "success",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    }), 200

