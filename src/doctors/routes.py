from flask import Blueprint, jsonify, request
from utils.utils import hash_password, db
from src.models import Doctor


doctors = Blueprint("doc", __name__)


@doctors.route("/doctor/register", methods=["GET", "POST"])
def register():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")

    if len(password) < 8:
        return jsonify({"error":"Characters must be at least 5"})
    
    if Doctor.query.filter_by(full_name=name).first():
        return jsonify({"message":"Name already exists"})
    elif Doctor.query.filter_by(email=email).first():
        return jsonify({"message":"Email already exists"})
    else:
        new_doctor = Doctor(full_name=name, email=email, password=hash_password(password))
        db.session.add(new_doctor)
        db.commit()

        return jsonify({
            "message":"Your account has been created",
            "Full name":name,
            "email":email
        }), 201