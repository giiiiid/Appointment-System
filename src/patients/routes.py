from flask import Blueprint, request, jsonify
from utils.utils import hash_password, check_hash_password, db
from flask_jwt_extended import create_access_token, create_refresh_token
from src.models import Patient



patients = Blueprint("patient", __name__)



@patients.route("/patient/register", methods=["GET", "POST"])
def register():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")

    if len(password) < 8:
        return jsonify({"error":"Characters must be at least 5"})
    
    if Patient.query.filter_by(full_name=name).first():
        return jsonify({"message":"Name already exists"})
    elif Patient.query.filter_by(email=email).first():
        return jsonify({"message":"Email already exists"})
    else:
        new_doctor = Patient(full_name=name, email=email, password=hash_password(password))
        db.session.add(new_doctor)
        db.commit()

        return jsonify({
            "message":"Your account has been created",
            "Name":name,
            "email":email
        }), 201



@patients.route("/patient/login", methods=["GET", "POST"])
def login():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")

    user = Patient.query.filter_by(full_name=name).first()
    hashed_pwd = check_hash_password(user.password, password)

    if user and hashed_pwd:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return jsonify({
            "message":"You have successfully logged in",
            "access-token":access_token,
            "refresh-token":refresh_token,
            "user":{
                "Name":user.full_name,
                "email":user.email,
            }
        })
    else:
        return jsonify({"error":"Invalid credentials"}), 404