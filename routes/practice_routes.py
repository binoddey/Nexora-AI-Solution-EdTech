# routes/practice_routes.py

from flask import Blueprint, jsonify
from services.practice_service import PracticeService
from engine.adaptive_engine import AdaptiveEngine
from ml.adaptive_ml import AdaptiveML

practice_bp = Blueprint("practice_bp", __name__)

@practice_bp.route("/api/practice/<subject>/<topic>", methods=["GET"])
def practice_topic(subject, topic):
    from app import get_student, QUESTION_BANK

    student = get_student()
    engine = AdaptiveEngine()
    ml = AdaptiveML()

    service = PracticeService(
        student_model=student,
        adaptive_engine=engine,
        adaptive_ml=ml,
        question_bank=QUESTION_BANK
    )

    response = service.get_next_question(
        subject=subject,
        forced_topic=topic
    )

    return jsonify(response)
