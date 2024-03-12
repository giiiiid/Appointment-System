from utils.utils import db


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(10), unique=True, nullable=False)
    doc_id = db.Column(db.Integer, unique=True, nullable=False)
    specialization = db.Column(db.String(15), unique=True, nullable=False)
    location = db.Column(db.String(50))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), primary_key=True)
    # patients = db.relationship("Patient", backref="patient", lazy=True)

    def __repr__(self):
        return f"Doctor({self.name}, {self.email})"



class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(10), unique=True, nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), primary_key=True)
    # doc_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    # type_of_sickness = db.Column(db.String(100))
    # appointed_date = db.Column(db.Date)

    def __repr__(self):
        return f"{self.full_name}"
    


class Appointment(db.Model):
    id = db.Column(db.Integer, primar_key=True)
    type_of_sickness = db.Column(db.String(100))
    appointed_date = db.Column(db.Date)
    doctor_appointed = db.relationship("Doctor", backref="doctor", lazy=True)
    patient_appointed = db.relationship("Patient", backref="patient", lazy=True)


    def __repr__(self):
        return f"{self.full_name} - {self.type_of_sickness}"