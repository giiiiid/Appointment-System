from flask import Flask
from utils.config import Config
from utils.utils import db, bcrypt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)


    return app
    