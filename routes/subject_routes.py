# routes/subject_routes.py

from flask import Blueprint, jsonify
from services.subject_service import SubjectService

subject_bp = Blueprint("subject_bp", __name__)

@subject_bp.route("/api/subject_report/<subject>", methods=["GET"])
def subject_report(subject):
    from app import get_student  # lazy import to avoid circular deps

    student = get_student()
    service = SubjectService(student)

    report = service.generate_subject_report()
    return jsonify(report)
