"""
ai_explanation.py

Responsible for generating human-readable AI explanations
based on student mastery and performance trends.

This module does NOT change state.
It only EXPLAINS decisions made by the system.
"""


class AIExplanationEngine:
    def __init__(self, mastery_data, attempt_data, history_data):
        """
        mastery_data: dict -> {topic: mastery_percentage}
        attempt_data: dict -> {topic: total_attempts}
        history_data: dict -> {topic: [True, False, ...]}  # recent answers
        """
        self.mastery = mastery_data
        self.attempts = attempt_data
        self.history = history_data

    # -------------------------------
    # Strengths & Weaknesses
    # -------------------------------

    def get_strengths(self, threshold=75):
        strengths = []
        for topic, value in self.mastery.items():
            if value >= threshold:
                strengths.append(f"{topic} ({value}%)")
        return strengths

    def get_weak_areas(self, threshold=50):
        weak = []
        for topic, value in self.mastery.items():
            if value <= threshold:
                weak.append(f"{topic} ({value}%)")
        return weak

    # -------------------------------
    # Focus Topic Selection
    # -------------------------------

    def get_focus_topic(self):
        """
        Choose the topic that needs attention most.
        Priority:
        1. Lowest mastery
        2. Highest recent error rate
        """
        scored = []

        for topic in self.mastery:
            mastery_score = self.mastery[topic]

            recent = self.history.get(topic, [])
            if recent:
                error_rate = recent.count(False) / len(recent)
            else:
                error_rate = 0

            scored.append((topic, mastery_score, error_rate))

        # Sort: lowest mastery, highest error rate
        scored.sort(key=lambda x: (x[1], -x[2]))

        return scored[0][0]

    # -------------------------------
    # Natural Language Explanation
    # -------------------------------

    def explain_focus(self, topic):
        mastery = self.mastery.get(topic, 0)
        recent = self.history.get(topic, [])

        incorrect = recent.count(False)
        total = len(recent)

        reasons = []

        if mastery < 50:
            reasons.append("low overall mastery")

        if total > 0 and incorrect / total > 0.4:
            reasons.append("frequent recent errors")

        if self.attempts.get(topic, 0) < 5:
            reasons.append("limited practice so far")

        if not reasons:
            reasons.append("balanced difficulty with room for improvement")

        return f"{topic} was selected because of " + " and ".join(reasons) + "."

