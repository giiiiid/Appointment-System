from flask import Blueprint, jsonify, request
from utils.utils import hash_password, db, check_hash_password
from src.models import Doctor
from flask_jwt_extended import create_access_token, create_refresh_token


doctors = Blueprint("doc", __name__)


@doctors.route("/doctor/register", methods=["GET", "POST"])
def register():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")
    age = request.json.get("age")
    doc_id = request.json.get("doc_id")
    specialization = request.json.get("specialization")
    location = request.json.get("location")

    if len(password) < 8:
        return jsonify({"error":"Characters must be at least 5"})
    
    if Doctor.query.filter_by(full_name=name).first():
        return jsonify({"message":"Name already exists"})
    elif Doctor.query.filter_by(email=email).first():
        return jsonify({"message":"Email already exists"})
    elif Doctor.query.filter_by(doc_id=doc_id).first():
        return jsonify({"message":"Doc ID already exists"})
    else:
        new_doctor = Doctor(
            full_name=name, 
            email=email, 
            password=hash_password(password),
            age=age,
            doc_id=doc_id,
            specialization=specialization,
            location=location
            )
        db.session.add(new_doctor)
        db.commit()

        return jsonify({
            "message":"Your account has been created",
            "Name":name,
            "email":email
        }), 201



@doctors.route("/docttor/login", methods=["GET", "POST"])
def login():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")
    

    user = Doctor.query.filter_by(full_name=name).first()
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
    

