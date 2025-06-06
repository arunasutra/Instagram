import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")

# In-memory storage for simplicity
patients = {}

@app.route('/')
def index():
    if 'patient_id' in session:
        pid = session['patient_id']
        patient = patients.get(pid)
        return render_template('session.html', patient=patient)
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    if not name:
        return redirect(url_for('index'))
    pid = len(patients) + 1
    patients[pid] = {"id": pid, "name": name, "notes": []}
    session['patient_id'] = pid
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('patient_id', None)
    return redirect(url_for('index'))

@app.route('/add_note', methods=['POST'])
def add_note():
    note = request.form.get('note')
    pid = session.get('patient_id')
    if pid and note:
        patients[pid]['notes'].append(note)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
