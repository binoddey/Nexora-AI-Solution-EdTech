# adaptive_math_tutor/adaptive_engine.py

import pandas as pd
import random

class AdaptiveEngine:
    """
    The core logic for selecting the next question based on the student's model.
    """
    
    DIFFICULTY_MAP = {'easy': 1, 'medium': 2, 'hard': 3}
    REV_DIFFICULTY_MAP = {1: 'easy', 2: 'medium', 3: 'hard'}
    
    def __init__(self, question_data_path):
        # Load the question bank
        self.qb = pd.read_csv(question_data_path)
        self.qb['difficulty_val'] = self.qb['difficulty'].map(self.DIFFICULTY_MAP)
        self.history = [] # Tracks the last two answers for hint logic
        
    def _get_target_difficulty(self, mastery_score):
        """
        Maps a student's mastery score to a target difficulty level.
        """
        if mastery_score > 80:
            return 'hard'
        elif mastery_score > 50:
            return 'medium'
        else:
            return 'easy'

    def _select_topic(self, student_model):
        """
        Selects the next topic based on a mixed strategy:
        - 70% chance to select the topic with the lowest mastery score (needs work).
        - 30% chance to select a topic randomly (to maintain engagement).
        """
        
        # Get topics student has attempted
        attempted_topics = [t for t, a in student_model.attempts.items() if a > 0]
        
        if random.random() < 0.7 and attempted_topics:
            # Select topic with lowest mastery among attempted topics
            topic_to_focus = min(student_model.mastery.items(), key=lambda item: item[1])[0]
        else:
            # Randomly select any topic
            topic_to_focus = random.choice(student_model.get_topics())
            
        return topic_to_focus

    def get_next_question(self, student_model):
        """
        Determines the next question's topic and difficulty and retrieves it.
        """
        
        # 1. Select the next topic to test
        topic = self._select_topic(student_model)
        mastery = student_model.mastery[topic]
        
        # 2. Determine the target difficulty based on mastery
        target_difficulty = self._get_target_difficulty(mastery)
        
        # 3. Filter question bank
        available_q = self.qb[
            (self.qb['topic'] == topic) & 
            (self.qb['difficulty'] == target_difficulty)
        ]
        
        # Fallback: If no question exists at the exact difficulty, try medium, then easy.
        if available_q.empty:
             available_q = self.qb[
                (self.qb['topic'] == topic) & 
                (self.qb['difficulty'] == 'medium')
            ]
        if available_q.empty:
             available_q = self.qb[
                (self.qb['topic'] == topic)
            ]
        
        # 4. Select a random question from the filtered list
        if available_q.empty:
            return None # Should not happen with a good question bank
        
        return available_q.sample(1).iloc[0].to_dict()

    def update_session_history(self, is_correct):
        """Updates history for the hint/solution logic."""
        self.history.append(is_correct)
        if len(self.history) > 2:
            self.history.pop(0)

    def should_show_help(self):
        """
        Rule: Show help (hint/solution) if the student has 2 consecutive wrong answers.
        """
        if len(self.history) == 2 and self.history == [False, False]:
            return True
        return False