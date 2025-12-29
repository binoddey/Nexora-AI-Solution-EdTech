# engine/adaptive_engine.py

class AdaptiveEngine:
    """
    Pedagogical decision layer.
    Decides:
    - which topic to practice
    - difficulty level
    - when to show hints
    """

    def __init__(self):
        # Tunable pedagogy parameters (easy to justify)
        self.DIFFICULTY_BANDS = {
            "easy": (0, 40),
            "medium": (41, 75),
            "hard": (76, 100)
        }

        self.HINT_TRIGGER_ATTEMPTS = 2
        self.HINT_TRIGGER_ERROR_RATE = 0.5

    # -------------------------
    # Topic Selection
    # -------------------------

    def select_topic(self, student_model, forced_topic=None):
        """
        Select topic for practice.
        - If forced_topic is provided → respect user choice
        - Else → let AI decide
        """
        if forced_topic:
            return forced_topic

        return student_model.get_focus_topic()

    # -------------------------
    # Difficulty Selection
    # -------------------------

    def select_difficulty(self, mastery):
        """
        Decide difficulty band based on mastery.
        """
        for difficulty, (low, high) in self.DIFFICULTY_BANDS.items():
            if low <= mastery <= high:
                return difficulty

        # Fallback (should never happen)
        return "medium"

    def get_difficulty_reasoning(self, mastery):
        """
        Human-readable explanation for difficulty choice.
        """
        difficulty = self.select_difficulty(mastery)

        if difficulty == "easy":
            return "Low mastery detected, easier questions selected to build confidence"
        elif difficulty == "medium":
            return "Moderate mastery detected, maintaining optimal learning challenge"
        else:
            return "High mastery detected, harder questions selected to stretch ability"

    # -------------------------
    # Hint Logic
    # -------------------------

    def should_show_hint(self, student_model, topic):
        """
        Decide whether to show a hint.
        Based on:
        - Recent error rate
        - Number of attempts
        """
        attempts = student_model.attempts[topic]
        error_rate = student_model.get_recent_error_rate(topic)

        if attempts < self.HINT_TRIGGER_ATTEMPTS:
            return False

        if error_rate >= self.HINT_TRIGGER_ERROR_RATE:
            return True

        return False

    def get_hint_reasoning(self, student_model, topic):
        """
        Explain why a hint was shown.
        """
        error_rate = round(student_model.get_recent_error_rate(topic) * 100)

        return (
            f"Hint shown due to repeated difficulty in {topic} "
            f"(recent error rate {error_rate}%)"
        )

    # -------------------------
    # Debug / Transparency
    # -------------------------

    def explain_decision(self, student_model, topic):
        """
        Full pedagogical explanation for judges/debugging.
        """
        mastery = student_model.mastery[topic]

        return {
            "topic": topic,
            "mastery": mastery,
            "difficulty": self.select_difficulty(mastery),
            "difficulty_reasoning": self.get_difficulty_reasoning(mastery),
            "show_hint": self.should_show_hint(student_model, topic)
        }
