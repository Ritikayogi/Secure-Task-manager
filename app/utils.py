from flask import request, jsonify, current_app
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            return jsonify({"msg": "Token missing"}), 403
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "Token expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"msg": "Invalid token"}), 403

        return f(data, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(user_data, *args, **kwargs):
        if user_data.get("role") != "admin":
            return jsonify({"msg": "Admin only"}), 403
        return f(user_data, *args, **kwargs)
    return decorated