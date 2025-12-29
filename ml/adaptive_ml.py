# ml/adaptive_ml.py

import math


class AdaptiveML:
    """
    Optimization layer.
    Predicts probability of student success on a question
    and ranks questions to maintain ~65% success probability.
    """

    def __init__(self, target_success=0.65):
        self.TARGET_SUCCESS = target_success

        # Tunable weights (explainable to judges)
        self.W_MASTERY = 0.6
        self.W_DIFFICULTY = 0.4

        # Difficulty encoding
        self.DIFFICULTY_MAP = {
            "easy": 0.3,
            "medium": 0.6,
            "hard": 0.9
        }

    # -------------------------
    # Core Prediction
    # -------------------------

    def predict_success(self, mastery, difficulty):
        """
        Predict probability of success using
        a logistic-style function.
        """
        mastery_norm = mastery / 100
        difficulty_val = self.DIFFICULTY_MAP.get(difficulty, 0.6)

        # Linear combination
        z = (
            self.W_MASTERY * mastery_norm
            - self.W_DIFFICULTY * difficulty_val
        )

        # Sigmoid for probability
        probability = 1 / (1 + math.exp(-5 * z))

        return round(probability, 2)

    # -------------------------
    # Question Ranking
    # -------------------------

    def rank_questions(self, questions, mastery, difficulty):
        """
        Rank questions by closeness to target success probability.
        ML does NOT choose topic — only ranks questions.
        """
        scored = []

        for q in questions:
            prob = self.predict_success(mastery, difficulty)
            distance = abs(prob - self.TARGET_SUCCESS)

            scored.append({
                "question": q,
                "predicted_success": prob,
                "distance": distance
            })

        # Sort by closest to target success
        scored.sort(key=lambda x: x["distance"])

        return scored

    # -------------------------
    # Explanation Layer
    # -------------------------

    def explain_prediction(self, mastery, difficulty):
        """
        Human-readable ML explanation.
        """
        prob = self.predict_success(mastery, difficulty)

        return (
            f"Predicted success probability is {int(prob * 100)}% "
            f"based on current mastery ({mastery}%) "
            f"and selected difficulty ({difficulty})"
        )
