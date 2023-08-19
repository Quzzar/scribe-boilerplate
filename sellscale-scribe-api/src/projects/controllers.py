from flask import Blueprint, request, jsonify
from src.authentication.request_helpers import get_request_parameter
from src.authentication.decorators import require_user
from src.projects.services import (
    get_projects,
    get_project,
    create_project,
    update_project,
    delete_project,
    create_message,
    get_message,
    get_messages,
    update_message
)
from app import limiter

PROJECTS_BLUEPRINT = Blueprint("project", __name__)


@PROJECTS_BLUEPRINT.route("/", methods=["GET"])
@require_user
def get_projects_endpoint(user_id: str):
    
    projects = get_projects(user_id)

    return jsonify({
        "status": "success",
        "data": projects
    }), 200


@PROJECTS_BLUEPRINT.route("/", methods=["POST"])
@require_user
def create_project_endpoint(user_id: str):
    
    name = get_request_parameter("name", request, json=True, required=True, parameter_type=str, default_value='')
    description = get_request_parameter("description", request, json=True, required=True, parameter_type=str, default_value='')
    template_id = get_request_parameter("template_id", request, json=True, required=False, parameter_type=int, default_value=None)

    project = create_project(user_id, name, description, template_id)

    return jsonify({
        "status": "success",
        "data": project
    }), 200


@PROJECTS_BLUEPRINT.route("/<project_id>/", methods=["GET"])
@require_user
def get_project_endpoint(user_id: str, project_id: str):
    
    project = get_project(user_id, project_id)

    return jsonify({
        "status": "success",
        "data": project,
    }), 200


@PROJECTS_BLUEPRINT.route("/<project_id>/", methods=["PATCH"])
@require_user
def update_project_endpoint(user_id: str, project_id: str):
    
    name = get_request_parameter("name", request, json=True, required=False, parameter_type=str, default_value='')
    description = get_request_parameter("description", request, json=True, required=False, parameter_type=str, default_value='')
    
    project = update_project(user_id, project_id, name, description)

    return jsonify({
        "status": "success",
        "data": project,
    }), 200


@PROJECTS_BLUEPRINT.route("/<project_id>/", methods=["DELETE"])
@require_user
def delete_project_endpoint(user_id: str, project_id: str):
    
    project = delete_project(user_id, project_id)

    return jsonify({
        "status": "success",
        "data": project,
    }), 200


# Message generation
@PROJECTS_BLUEPRINT.route("/<project_id>/message/", methods=["POST"])
@limiter.limit("15/hour")
@require_user
def create_message_endpoint(user_id: str, project_id: str):
    
    li_url = get_request_parameter("li_url", request, json=True, required=True, parameter_type=str, default_value='')
    blocks = get_request_parameter("blocks", request, json=True, required=True, parameter_type=list, default_value=[])
    
    success, status, message = create_message(user_id, project_id, li_url, blocks)

    if success:
        return jsonify({
            "status": "success",
            "data": message,
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": status,
        }), 500


@PROJECTS_BLUEPRINT.route("/<project_id>/message/", methods=["GET"])
@require_user
def get_messages_endpoint(user_id: str, project_id: str):
    
    messages = get_messages(user_id, project_id)

    return jsonify({
        "status": "success",
        "data": messages,
    }), 200


@PROJECTS_BLUEPRINT.route("/<project_id>/message/<message_id>/", methods=["GET"])
@require_user
def get_message_endpoint(user_id: str, project_id: str, message_id: str):
    
    message = get_message(user_id, message_id)

    return jsonify({
        "status": "success",
        "data": message,
    }), 200


@PROJECTS_BLUEPRINT.route("/<project_id>/message/<message_id>/", methods=["PATCH"])
@require_user
def update_message_endpoint(user_id: str, project_id: str, message_id: str):
    
    subject = get_request_parameter("subject", request, json=True, required=False, parameter_type=str, default_value='')
    msg = get_request_parameter("message", request, json=True, required=False, parameter_type=str, default_value='')
    
    message = update_message(user_id, message_id, subject, msg)

    return jsonify({
        "status": "success",
        "data": message,
    }), 200
