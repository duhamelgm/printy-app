from functools import wraps
from flask import jsonify, request
from models import Token
from datetime import datetime
from printing_queue import queue_size

def throttle():
    def _throttle(f):
        @wraps(f)
        def __throttle(*args, **kwargs):
            if queue_size() >= 5:
                return jsonify({"status": "error", "message": "Printy is busy right now. Please try again later."}), 429

            return f(*args, **kwargs)
        return __throttle
    return _throttle