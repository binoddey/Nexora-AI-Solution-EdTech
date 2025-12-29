from flask import Flask, session
from flask_cors import CORS
import json
import uuid
from flask import render_template

# -------------------------
# Import Core Layers
# -------------------------

from models.student_model import StudentModel
from engine.adaptive_engine import AdaptiveEngine
from ml.adaptive_ml import AdaptiveML

# -------------------------
# Flask App Setup
# -------------------------

app = Flask(__name__)
app.secret_key = "hackathon_super_secret_key"
CORS(app)

# -------------------------
# Load Question Bank
# -------------------------

with open("data/question_bank.json", "r", encoding="utf-8") as f:
    QUESTION_BANK = json.load(f)

SUBJECT = "Mathematics"
TOPICS = list(QUESTION_BANK[SUBJECT].keys())

# -------------------------
# Shared AI Engines
# -------------------------

adaptive_engine = AdaptiveEngine()
adaptive_ml = AdaptiveML()

# -------------------------
# Session-Level Student Store
# -------------------------
# NOTE:
# Flask sessions cannot store Python objects.
# We store a session ID in cookies and map it to a StudentModel in memory.
# -------------------------

STUDENT_STORE = {}

def get_student():
    """
    Returns a StudentModel tied to the current browser session.
    Creates one if it does not exist.
    """

    if "student_id" not in session:
        session["student_id"] = str(uuid.uuid4())

    student_id = session["student_id"]

    if student_id not in STUDENT_STORE:
        STUDENT_STORE[student_id] = StudentModel(
            subject=SUBJECT,
            topics=TOPICS
        )

    return STUDENT_STORE[student_id]

# -------------------------
# Register API Routes
# -------------------------

from routes.subject_routes import subject_bp
from routes.practice_routes import practice_bp
from routes.submission_routes import submission_bp

app.register_blueprint(subject_bp)
app.register_blueprint(practice_bp)
app.register_blueprint(submission_bp)

# -------------------------
# Health Check (Optional)
# -------------------------

@app.route("/")
def home():
    return {
        "status": "running",
        "message": "AI-Powered Adaptive Learning Backend is live"
    }



@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route('/courses.html')
def courses():
    return render_template('courses.html')

# -------------------------
# Run Server
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)
