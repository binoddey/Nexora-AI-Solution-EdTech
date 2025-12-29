# services/subject_service.py

class SubjectService:
    """
    Builds subject-level learning reports.
    This is the visibility layer for AI reasoning.
    """

    def __init__(self, student_model):
        self.student = student_model

    # -------------------------
    # Public API
    # -------------------------

    def generate_subject_report(self):
        """
        Generate a complete subject dashboard report.
        """

        mastery_overview = self.student.get_mastery_overview()
        strengths = self.student.get_strengths()
        weak_areas = self.student.get_weak_areas()
        focus_topic = self.student.get_focus_topic()
        ai_reasoning = self.student.get_ai_reasoning_for_focus()

        return {
            "subject": self.student.subject,
            "mastery_overview": mastery_overview,
            "strengths": strengths,
            "weak_areas": weak_areas,
            "focus_topic": focus_topic,
            "ai_reasoning": ai_reasoning
        }

    # -------------------------
    # Debug / Transparency
    # -------------------------

    def explain(self):
        """
        Full explanation payload for demos or debugging.
        """
        return {
            "student_snapshot": self.student.snapshot(),
            "focus_topic": self.student.get_focus_topic(),
            "focus_reasoning": self.student.get_ai_reasoning_for_focus()
        }
