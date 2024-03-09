from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt =  Bcrypt()



def hash_password(pwd:str):
    hash_pwd = bcrypt.generate_password_hash(pwd).decode("utf-8")
    return hash_pwd


def check_hash_password(user_pwd, pwd):
    return bcrypt.check_password_hash(user_pwd, pwd)