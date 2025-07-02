from flask import Flask
from app.webhook.routes import webhook
from app.extensions import mongo
from flask_cors import CORS
import os


def create_app():
    template_dir = os.path.abspath("templates")
    app = Flask(__name__, template_folder=template_dir)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/webhookDB"
    app.config["MONGO_URI"] = "mongodb+srv://parag477:Parag9144@cluster0.l3nik0y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    mongo.init_app(app)
    CORS(app)

    app.register_blueprint(webhook)
    return app
