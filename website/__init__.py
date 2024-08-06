import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY']='f5f58d08c51419aca1208bc5a68467fd'
    app.config["MONGO_URI"] =  os.getenv("MONGO_URI")
    mongo.init_app(app)

    app.mongo = mongo

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    return app