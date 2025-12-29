# routes/submission_routes.py

from flask import Blueprint, jsonify, request

submission_bp = Blueprint("submission_bp", __name__)

@submission_bp.route("/api/submit", methods=["POST"])
def submit_answer():
    from app import get_student
    from engine.adaptive_engine import AdaptiveEngine

    data = request.get_json()
    topic = data.get("topic")
    is_correct = data.get("correct")

    student = get_student()
    engine = AdaptiveEngine()

    # Update student model
    student.record_attempt(topic, is_correct)

    updated_mastery = student.mastery[topic]
    show_hint = engine.should_show_hint(student, topic)

    response = {
        "correct": is_correct,
        "updated_mastery": updated_mastery,
        "show_hint": show_hint,
        "learning_feedback": (
            f"Mastery in {topic} increased due to correct response"
            if is_correct
            else f"Mastery in {topic} decreased due to incorrect response"
        )
    }

    return jsonify(response)
