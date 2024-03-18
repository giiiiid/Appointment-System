from flask import Blueprint, request, jsonify, abort
from utils.utils import hash_password, check_hash_password, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from src.models import Patient, Appointment



patients = Blueprint("patient", __name__)



@patients.route("/patient/register", methods=["GET", "POST"])
def register():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")
    age = request.json.get("age")

    if len(password) < 8:
        return jsonify({"error":"Password characters must be at least 5"})
    elif age < 18:
        return jsonify({"message":"Contact a guardian to book an appointment"})
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
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    user = Patient.query.filter_by(full_name=name, email=email).first()
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
    


@patients.route("/patient/set-appointment", methods=["POST"])
@jwt_required()
def create_appointment():
    current_user = get_jwt_identity()

    sickness = request.json.get("Sickness")
    set_date = request.json.get("Date")
    doctor_to_appoint = request.json.get("Doctor")

    if doctor_to_appoint is None:
        return jsonify({"message":"Doctor does not exist"})
    else:
        new_appointment = Appointment(
            type_of_sickness = sickness,
            appointed_date = set_date,
            doc_id = doctor_to_appoint,
            patient_id = current_user
        )
        db.session.add(new_appointment)
        db.session.commit()

    return jsonify({
        "Name of Doctor":new_appointment.doc_appointment.full_name,
        "Email":new_appointment.doctordoc_appointment.email,
        "Type of Sickness":new_appointment.type_of_sickness,
        "Date":new_appointment.date
    }), 201



@patients.route("/patient/view-appointments/<int:id>", methods=["GET", "POST"])
@jwt_required()
def view_appointment(id):
    current_user = get_jwt_identity()

    meeting = Appointment.query.get_or_404(id)
    if meeting.patient_id != current_user:
        abort(403)
    else:
        return jsonify({
            "Name of Doctor":meeting.doc_appointment.full_name,
            "Email":meeting.doctor_appointment.email,
            "Type of Sickness":meeting.type_of_sickness,
            "Date":meeting.date
        }), 200

    

@patients.route("/patient/view-appointments", methods=["GET"])
@jwt_required()
def viewlist_appointment():
    current_user = get_jwt_identity()
    meeting = Appointment.query.filter_by(patient_id == current_user).all()
    if not meeting:
        return jsonify({"message":"You are not authorised"})
    elif len(meeting) == 0:
        return jsonify({"message":"You have no appointments"})
    else:
        return meeting



@patients.route("/patient/update-appointment/<int:id>", methods=["GET", "POST"])
@jwt_required()
def update_appointment(id):
    current_user = get_jwt_identity()
    meeting = Appointment.query.get_or_404(id)
    if meeting.patient_id != current_user:
        abort(403)
    
    if request.method == "GET":
        return jsonify({
            "Name of Doctor": meeting.doc_appointment.full_name,
            "Email": meeting.doc_appointment.email,
            "Type of Sickness": meeting.type_of_sickness,
            "Date": meeting.date
        })
    
    elif request.method == "PUT":
        meeting.type_of_sickness = request.json.get("Sickness")
        meeting.doc_appointment.full_name = request.json.get("Doctor")
        meeting.date = request.json.get("Date")

        db.session.commit()
        return jsonify({
            "Name of Doctor": meeting.doc_appointment.full_name,
            "Email": meeting.doc_appointment.email,
            "Type of Sickness": meeting.type_of_sickness,
            "Date": meeting.date
        }), 200



@patients.route("/patient/delete-appointment/<int:id>", methods=["GET", "DELETE"])
@jwt_required()
def delete_appointment(id):
    current_user = get_jwt_identity()

    meeting = Appointment.query.get_or_404(id)
    if meeting.patient_id != current_user:
        abort(403)
    else:
        db.session.delete(meeting)
        db.session.commit()
        return jsonify({"message":"Your appointment has successfully been deleted"}), 200