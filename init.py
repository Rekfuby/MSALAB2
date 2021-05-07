from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    patron_name = db.Column(db.String(50))
    room = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, last_name, first_name, patron_name, room):
        self.last_name = last_name
        self.first_name = first_name
        self.patron_name = patron_name
        self.room = room

    def __repr__(self):
        return '' % self.id

class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    patron_name = db.Column(db.String(50))
    history = db.Column(db.String(255))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, last_name, first_name, patron_name, history):
        self.last_name = last_name
        self.first_name = first_name
        self.patron_name = patron_name
        self.history = history

    def __repr__(self):
        return '' % self.id

db.create_all()

class DoctorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Doctor
        sqla_session = db.session
    id = fields.Number(dump_only = True)
    last_name = fields.String(required = True)
    first_name = fields.String(required = True)
    patron_name = fields.String(required = False)
    room = fields.Number(required = True)

class PatientSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Patient
        sqla_session = db.session
    id = fields.Number(dump_only = True)
    last_name = fields.String(required = True)
    first_name = fields.String(required = True)
    patron_name = fields.String(required = False)
    history = fields.String(required = False)

@app.route('/doctors', methods = ['GET'])
def get_doctors():
    get_doctors = Doctor.query.all()
    doctor_schema = DoctorSchema(many = True)
    doctors = doctor_schema.dump(get_doctors)
    return make_response(jsonify({"doctor": doctors}))

@app.route('/doctors/<id>', methods = ['GET'])
def get_doctor_by_id(id):
    get_doctor = Doctor.query.get(id)
    doctor_schema = DoctorSchema()
    doctor = doctor_schema.dump(get_doctor)
    return make_response(jsonify({"doctor": doctor}))

@app.route('/doctors/<id>', methods = ['PUT'])
def update_doctor_by_id(id):
    data = request.get_json()
    get_doctor = Doctor.query.get(id)
    if data.get('last_name'):
        get_doctor.last_name = data['last_name']
    if data.get('first_name'):
        get_doctor.first_name = data['first_name']
    if data.get('patron_name'):
        get_doctor.patron_name = data['patron_name']
    if data.get('room'):
        get_doctor.room= data['room']    
    db.session.add(get_doctor)
    db.session.commit()
    doctor_schema = DoctorSchema(only=['id', 'last_name', 'first_name','patron_name','room'])
    doctor = doctor_schema.dump(get_doctor)
    return make_response(jsonify({"doctor": doctor}))

@app.route('/doctors/<id>', methods = ['DELETE'])
def delete_doctor_by_id(id):
    get_doctor = Doctor.query.get(id)
    db.session.delete(get_doctor)
    db.session.commit()
    return make_response("",204)

@app.route('/doctors', methods = ['POST'])
def create_doctor():
    data = request.get_json()
    doctor_schema = DoctorSchema()
    doctor = doctor_schema.load(data)
    result = doctor_schema.dump(doctor.create())
    return make_response(jsonify({"doctor": result}),200)




@app.route('/patients', methods = ['GET'])
def get_patients():
    get_patients = Patient.query.all()
    patient_schema = PatientSchema(many = True)
    patients = patient_schema.dump(get_patients)
    return make_response(jsonify({"patient": patients}))

@app.route('/patients/<id>', methods = ['GET'])
def get_patient_by_id(id):
    get_patient = Patient.query.get(id)
    patient_schema = PatientSchema()
    patient = patient_schema.dump(get_patient)
    return make_response(jsonify({"patient": patient}))

@app.route('/patients/<id>', methods = ['PUT'])
def update_patient_by_id(id):
    data = request.get_json()
    get_patient = Patient.query.get(id)
    if data.get('last_name'):
        get_patient.last_name = data['last_name']
    if data.get('first_name'):
        get_patient.first_name = data['first_name']
    if data.get('patron_name'):
        get_patient.patron_name = data['patron_name']
    if data.get('history'):
        get_patient.history= data['history']    
    db.session.add(get_patient)
    db.session.commit()
    patient_schema = PatientSchema(only=['id', 'last_name', 'first_name','patron_name','history'])
    patient = patient_schema.dump(get_patient)
    return make_response(jsonify({"patient": patient}))

@app.route('/patients/<id>', methods = ['DELETE'])
def delete_patient_by_id(id):
    get_patient = Patient.query.get(id)
    db.session.delete(get_patient)
    db.session.commit()
    return make_response("",204)

@app.route('/patients', methods = ['POST'])
def create_patient():
    data = request.get_json()
    patient_schema = PatientSchema()
    patient = patient_schema.load(data)
    result = patient_schema.dump(patient.create())
    return make_response(jsonify({"patient": result}),200)

if __name__ == '__main__':
    app.run(debug=True)