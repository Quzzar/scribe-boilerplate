from flask import Blueprint, request, jsonify
from src.authentication.request_helpers import get_request_parameter
from src.authentication.decorators import require_user
from src.templates.services import get_templates, create_template
import os


TEMPLATES_BLUEPRINT = Blueprint("template", __name__)


@TEMPLATES_BLUEPRINT.route("/", methods=["GET"])
@require_user
def get_templates_endpoint(user_id: str):
    
    templates = get_templates()

    return jsonify({
        "status": "success",
        "data": templates
    }), 200


@TEMPLATES_BLUEPRINT.route("/", methods=["POST"])
def create_template_endpoint():
    
    token = None
    bearer_token = request.headers.get('Authorization')
    if bearer_token:
        if bearer_token.startswith('Bearer '):
            token = bearer_token.split(' ')[-1]
        else:
            return jsonify({'message': 'Bearer token is missing.'}), 401
    else:
        return jsonify({'message': 'Authorization header is missing.'}), 401
    
    if not token or os.environ.get("ADMIN_AUTH_TOKEN") != token:
        return jsonify({'message': 'Admin authorization token is invalid.'}), 401

    name = get_request_parameter("name", request, json=True, required=True, parameter_type=str, default_value='')
    description = get_request_parameter("description", request, json=True, required=True, parameter_type=str, default_value='')
    blocks = get_request_parameter("blocks", request, json=True, required=True, parameter_type=list, default_value=[])

    template = create_template(name, description, blocks)

    return jsonify({
        "status": "success",
        "data": template
    }), 200
