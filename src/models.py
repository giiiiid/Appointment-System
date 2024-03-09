from utils.utils import db


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(10), unique=True, nullable=False)
    doc_id = db.Column(db.Integer(8), unique=True, nullable=False)
    specialization = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String(50))
    patients = db.relationship("Patient", backref="patient", lazy=True)

    def __repr__(self):
        return f"Doctor({self.name}, {self.email})"



class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(10), unique=True, nullable=False)
    type_of_sickness = db.Column(db.String(100))
    appointed_date = db.Column(db.Date)

    def __repr__(self):
        return f"{self.full_name}"
    