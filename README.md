# Focusing Therapy Interface

This simple Flask application provides a basic interface for patients to take notes during focusing sessions.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set a `SECRET_KEY` environment variable used by Flask for session security:
   ```bash
   export SECRET_KEY="your-secret-value"
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Visit `http://localhost:5000` in your browser.

Patients can log in by entering their name. Notes from their focusing sessions are stored in a local SQLite database (`notes.db`) so data persists across restarts.
