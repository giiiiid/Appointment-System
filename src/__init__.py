from flask import Flask
from utils.config import Config
from utils.utils import db, bcrypt
from doctors.routes import doctors
from patients.routes import patients

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(doctors)
    app.register_blueprint(patients)


    return app
    