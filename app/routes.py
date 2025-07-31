from flask import Blueprint, request, jsonify
from app import mongo
from app.utils import token_required, admin_required

task_bp = Blueprint("tasks", __name__)

@task_bp.route('/tasks', methods=['POST'])
@token_required
def create_task(user_data):
    data = request.get_json()
    task = {
        "title": data["title"],
        "description": data.get("description", ""),
        "user": user_data["email"]
    }
    mongo.db.tasks.insert_one(task)
    return jsonify({"msg": "Task created"}), 201

@task_bp.route('/tasks', methods=['GET'])
@token_required
def get_tasks(user_data):
    tasks = mongo.db.tasks.find({"user": user_data["email"]})
    return jsonify([{"title": t["title"], "description": t.get("description", "")} for t in tasks])

@task_bp.route('/admin/tasks', methods=['GET'])
@token_required
@admin_required
def get_all_tasks(user_data):
    tasks = mongo.db.tasks.find()
    return jsonify([{"title": t["title"], "user": t["user"]} for t in tasks])