from flask import Blueprint, jsonify, request, abort
from utils.utils import hash_password, db, check_hash_password
from src.models import Doctor, Appointment
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity



doctors = Blueprint("doc", __name__)



@doctors.route("/doctor/register", methods=["GET", "POST"])
def register():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    age = request.json.get("age")
    doc_id = request.json.get("doc_id")
    specialization = request.json.get("specialization")
    address = request.json.get("address")

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
            address=address
            )
        db.session.add(new_doctor)
        db.session.commit()

        return jsonify({
            "message":"Your account has been created",
            "Name":name,
            "email":email
        }), 201



@doctors.route("/doctor/login", methods=["GET", "POST"])
def login():
    name = request.json.get("full_name")
    email = request.json.get("email")
    password = request.json.get("password")

    user = Doctor.query.filter_by(full_name=name, email=email).first()
    hashed_pwd = check_hash_password(user.password, password)

    if user and hashed_pwd:
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return jsonify({
            "message":"You have been successfully logged in",
            "access-token":access_token,
            "refresh-token":refresh_token,
            "user":{
                "Name":user.full_name,
                "email":user.email,
            }
        })
    else:
        return jsonify({"error":"Invalid credentials"}), 404
    


@doctors.route("/doctor/view-appointment/<int:id>", methods=["GET"])
@jwt_required()
def view_appointments(id):
    current_user = get_jwt_identity()
    
    meeting = Appointment.query.get_or_404(id)
    if meeting.doctor != current_user:
        abort(403)
    else:
        return jsonify({
            "Name of Patient":meeting.patient.full_name,
            "Email":meeting.patient.email,
            "age":meeting.patient.age,
            "Type of Sickness":meeting.type_of_sickness,
            "Date":meeting.date
        }), 200



@doctors.route("/doctor/<int:id>/view-appointments", methods=["GET"])
@jwt_required()
def viewlist_appointment():
    current_user = get_jwt_identity()
    doctor = Doctor.query.get_or_404(id)
    if doctor.id != current_user:
        abort(403)

    meeting = doctor.appointment.all()
    if not doctor:
        return jsonify({"message":"You are not authorised"})
    elif len(meeting) == 0:
        return jsonify({"message":"You have no appointments"})
    else:
        return meeting



@doctors.route("/doctor/delete-appointment/<int:id>", methods=["GET", "DELETE"])
@jwt_required()
def delete_appointments(id):
    current_user = get_jwt_identity()

    meeting = Appointment.query.get_or_404(id)
    if meeting.doc_id != current_user:
        abort(403)

    if not meeting:
        return jsonify({"message":"Appointment cannot be found"}), 404
    else:
        db.session.delete(meeting)
        db.session.commit()
        return jsonify({
            "message":"You have successfully deleted the appointment"
        }), 200
