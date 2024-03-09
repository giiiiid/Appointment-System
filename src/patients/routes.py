from flask import Blueprint, request, jsonify
from utils.utils import hash_password, check_hash_password, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.models import Patient, Appointment



patients = Blueprint("patient", __name__)



@patients.route("/patient/register", methods=["GET", "POST"])
def register():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")
    age = request.json.get("age")

    if len(password) < 8:
        return jsonify({"error":"Characters must be at least 5"})
    
    if Patient.query.filter_by(full_name=name).first():
        return jsonify({"message":"Name already exists"})
    elif Patient.query.filter_by(email=email).first():
        return jsonify({"message":"Email already exists"})
    else:
        new_patient = Patient(
            full_name=name, 
            email=email, 
            password=hash_password(password),
            age=age
            )
        db.session.add(new_patient)
        db.session.commit()

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

    user = Patient.query.filter_by(full_name=name, email=email).first()
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
    


@patients.route("/patient/<int:user_id>/set-appointment", methods=["POST"])
@jwt_required()
def create_appointment(user_id):
    current_user = get_jwt_identity()

    sickness = request.json.get("type_of_sickness")
    date_to_set = request.json.get("appointed_date")

    if not Patient.query.filter_by(id=current_user).first():
        return jsonify({"error":"You are not authorised"})
    else:
        new_appointment = Appointment(
            type_of_sickness = sickness,
            appointed_date = date_to_set
        )
        db.session.add(new_appointment)
        db.session.commit()
