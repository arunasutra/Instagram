# Focusing Therapy Interface

This simple Flask application provides a basic interface for patients to take notes during focusing sessions.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Visit `http://localhost:5000` in your browser.

Patients can log in by entering their name. They can then add notes for their focusing sessions, which appear on the page. The data is stored in memory and will reset when the server restarts.
