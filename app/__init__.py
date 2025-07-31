from flask import Flask
from flask_pymongo import PyMongo
from flasgger import Swagger
from dotenv import load_dotenv
import os

load_dotenv()

mongo = PyMongo()

def create_app():
    app = Flask(__name__)

    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/taskmanager")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecret")

    mongo.init_app(app)
    Swagger(app)

    from app.auth import auth_bp
    from app.routes import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app