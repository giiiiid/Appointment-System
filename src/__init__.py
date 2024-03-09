from flask import Flask
from utils.config import Config
from utils.utils import db, bcrypt
from src.doctors.routes import doctors
from src.patients.routes import patients
from flask_jwt_extended import JWTManager



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(doctors)
    app.register_blueprint(patients)
    
    JWTManager(app)

    return app
    