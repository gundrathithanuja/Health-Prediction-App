from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.String(20))
    email = db.Column(db.String(100))
    glucose = db.Column(db.Float)
    haemoglobin = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    remarks = db.Column(db.String(200))


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        fullname = request.form['fullname']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        glucose_value = float(glucose)
        cholesterol_value = float(cholesterol)

        if glucose_value > 140:
            remarks = "High Diabetes Risk"
        elif cholesterol_value > 200:
            remarks = "High Cholesterol Risk"
        else:
            remarks = "Normal"

        patient = Patient(
            fullname=fullname,
            dob=dob,
            email=email,
            glucose=glucose_value,
            haemoglobin=float(haemoglobin),
            cholesterol=cholesterol_value,
            remarks=remarks
        )

        db.session.add(patient)
        db.session.commit()

        return redirect('/')

    patients = Patient.query.all()

    return render_template(
        'index.html',
        message="Patient Saved Successfully",
        patients=patients
    )


@app.route('/delete/<int:id>')
def delete_patient(id):

    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':

        patient.fullname = request.form['fullname']
        patient.dob = request.form['dob']
        patient.email = request.form['email']
        patient.glucose = float(request.form['glucose'])
        patient.haemoglobin = float(request.form['haemoglobin'])
        patient.cholesterol = float(request.form['cholesterol'])

        if patient.glucose > 140:
            patient.remarks = "High Diabetes Risk"
        elif patient.cholesterol > 200:
            patient.remarks = "High Cholesterol Risk"
        else:
            patient.remarks = "Normal"

        db.session.commit()

        return redirect('/')

    return render_template('edit.html', patient=patient)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)