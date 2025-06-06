import os
import sqlite3
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    g,
)

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY environment variable not set")

app = Flask(__name__)
app.secret_key = secret_key

DATABASE = os.path.join(os.path.dirname(__file__), "notes.db")


def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            note TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        );
        """
    )
    db.commit()


@app.route('/')
def index():
    if 'patient_id' in session:
        pid = session['patient_id']
        db = get_db()
        patient = db.execute(
            'SELECT id, name FROM patients WHERE id=?',
            (pid,),
        ).fetchone()
        if patient:
            notes = db.execute(
                'SELECT note FROM notes WHERE patient_id=?',
                (pid,),
            ).fetchall()
            patient_data = {
                "id": patient["id"],
                "name": patient["name"],
                "notes": [n["note"] for n in notes]
            }
            return render_template('session.html', patient=patient_data)
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name')
    if not name:
        return redirect(url_for('index'))
    db = get_db()
    cur = db.execute('INSERT INTO patients (name) VALUES (?)', (name,))
    db.commit()
    pid = cur.lastrowid
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
        db = get_db()
        db.execute(
            'INSERT INTO notes (patient_id, note) VALUES (?, ?)',
            (pid, note),
        )
        db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)
