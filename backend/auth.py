from functools import wraps
from flask import jsonify, request
from models import Token
from datetime import datetime

def authorized():
    def _authorized(f):
        @wraps(f)
        def __authorized(*args, **kwargs):
            # Check if the password is correct
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"status": "error", "message": "Unauthorized"}), 401

            # Check if the token is valid
            token_object = Token.query.filter_by(value=token).first()
            if not token_object:
                return jsonify({"status": "error", "message": "Unauthorized"}), 401

            # Check if the token is expired
            if token_object.expires_at < datetime.now():
                return jsonify({"status": "error", "message": "Token expired"}), 401

            return f(*args, **kwargs)
        return __authorized
    return _authorized