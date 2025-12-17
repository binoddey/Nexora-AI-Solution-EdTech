import numpy as np
from sklearn.linear_model import LogisticRegression

class AdaptiveML:
    def __init__(self):
        # Features: [Student_Mastery, Question_Difficulty_Weight]
        # 1=Easy, 2=Medium, 3=Hard
        self.model = LogisticRegression()
        
        # Synthetic training data to give the AI an initial "brain"
        # X: [[Mastery, Diff_Weight]] | y: [0=Incorrect, 1=Correct]
        X_train = np.array([
            [10, 3], [20, 3], [30, 2], [50, 2], 
            [70, 2], [85, 1], [95, 1], [40, 3]
        ])
        y_train = np.array([0, 0, 0, 1, 1, 1, 1, 0])
        
        self.model.fit(X_train, y_train)

    def predict_success(self, mastery, difficulty_str):
        diff_map = {"easy": 1, "medium": 2, "hard": 3}
        weight = diff_map.get(difficulty_str, 2)
        # Predicts probability of success (0.0 to 1.0)
        prob = self.model.predict_proba([[mastery, weight]])[0][1]
        return prob

    def get_best_question(self, mastery, questions):
        """
        AI Strategy: Select questions where success probability is 
        around 0.65 (The 'Sweet Spot' for learning).
        """
        scored_questions = []
        for q in questions:
            prob = self.predict_success(mastery, q['difficulty'])
            # We want the question closest to 0.65 probability
            diff_from_target = abs(prob - 0.65)
            scored_questions.append((diff_from_target, q))
        
        # Sort by smallest difference from target
        scored_questions.sort(key=lambda x: x[0])
        return scored_questions[0][1]