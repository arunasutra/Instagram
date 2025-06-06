# Focusing Therapy Interface

This simple Flask application provides a basic interface for patients to take notes during focusing sessions.  Notes are now stored in a local SQLite database.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Visit `http://localhost:5000` in your browser. To allow remote access, run the server with the host set to `0.0.0.0` (already configured in `app.py`).

Patients can log in by entering their name. They can then add notes for their focusing sessions, provide optional ratings before and after the session, and review their full history. Data is stored in a SQLite database (`focusing.db`) so it persists across restarts.
