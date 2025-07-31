from flask import Blueprint, request, jsonify, current_app
import bcrypt
import jwt
from datetime import datetime, timedelta
from app import mongo

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if mongo.db.users.find_one({"email": data["email"]}):
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    user = {
        "email": data["email"],
        "password": hashed_pw,
        "role": data.get("role", "user")
    }
    mongo.db.users.insert_one(user)
    return jsonify({"msg": "User registered"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({"email": data["email"]})

    if user and bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        token = jwt.encode({
            "user_id": str(user["_id"]),
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, current_app.config["SECRET_KEY"], algorithm="HS256")

        return jsonify({"token": token})
    return jsonify({"msg": "Invalid credentials"}), 401