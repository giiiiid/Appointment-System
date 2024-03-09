from flask import Blueprint
from utils.utils import hash_password



patients = Blueprint("patient", __name__)