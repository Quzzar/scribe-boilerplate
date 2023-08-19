from flask import request, jsonify
from functools import wraps
from app import supabase
from src.users.services import get_user_from_auth_id

def require_user(f):
    """ Decorator to check if the request has a valid token.

    Args:
        f (function): The function to be decorated.

    Returns:
        Any: The output of the decorated function, with the user_id as the first argument.
    """
    @wraps(f)
    def decorater(*args, **kwargs):
        token = None

        bearer_token = request.headers.get('Authorization')
        if bearer_token:
            if bearer_token.startswith('Bearer '):
                token = bearer_token.split(' ')[-1]
            else:
                return jsonify({'message': 'Bearer token is missing.'}), 401
        else:
            return jsonify({'message': 'Authorization header is missing.'}), 401

        if not token:
            return jsonify({'message': 'Bearer token is missing.'}), 401

        try:
            res = supabase.auth.get_user(token)
            user = get_user_from_auth_id(res.user.id)
            user_id = user.get('id')
        except AttributeError:
            return jsonify({'message': 'Authentication token is invalid.'}), 401
        except Exception as e:
            if str(e).startswith("invalid JWT:"):
                return jsonify({'message': 'Authentication token is invalid.'}), 401
            else:
              return jsonify({'message': str(e)}), 500

        return f(user_id, *args, **kwargs)
    return decorater
