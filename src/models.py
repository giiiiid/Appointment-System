from utils.utils import db


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=True, nullable=False)
    last_name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(10), unique=True, nullable=False)
    doc_id = db.Column(db.Integer(8), unique=True, nullable=False)
    specialization = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String(50))
    patients = db.relationship("Patient", backref="patient", lazy=True)



class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=True, nullable=False)
    last_name = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(10), unique=True, nullable=False)
    type_of_sickness = db.Column(db.String(100))
    appointed_date = db.Column(db.Date)
    