import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///focusing.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    notes = db.relationship("SessionNote", backref="patient", lazy=True, order_by="SessionNote.timestamp.desc()")


class SessionNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    note = db.Column(db.Text, nullable=False)
    rating_before = db.Column(db.Integer)
    rating_after = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'patient_id' in session:
        pid = session['patient_id']
        patient = Patient.query.get(pid)
        if patient:
            return render_template('session.html', patient=patient)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    if not name:
        return redirect(url_for('index'))
    patient = Patient.query.filter_by(name=name).first()
    if not patient:
        patient = Patient(name=name)
        db.session.add(patient)
        db.session.commit()
    session['patient_id'] = patient.id
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('patient_id', None)
    return redirect(url_for('index'))

@app.route('/add_note', methods=['POST'])
def add_note():
    note_text = request.form.get('note')
    rating_before = request.form.get('rating_before')
    rating_after = request.form.get('rating_after')
    pid = session.get('patient_id')
    if pid and note_text:
        entry = SessionNote(
            patient_id=pid,
            note=note_text,
            rating_before=int(rating_before) if rating_before else None,
            rating_after=int(rating_after) if rating_after else None,
        )
        db.session.add(entry)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=debug)
