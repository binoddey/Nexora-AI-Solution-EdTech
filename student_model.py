# adaptive_math_tutor/student_model.py

class StudentModel:
    """
    Tracks the student's mastery score (0-100) and attempts per topic.
    """
    def __init__(self, topics):
        # Initialize mastery and attempt counters for all available topics
        self.mastery = {topic: 50 for topic in topics} # Start all students at 50/100 mastery
        self.attempts = {topic: 0 for topic in topics}
        self.history = [] # To log session activity

    def get_topics(self):
        """Returns the list of all topics."""
        return list(self.mastery.keys())

    def update_mastery(self, topic, is_correct):
        """
        Updates the mastery score based on performance.
        - Correct answer: +5 points
        - Incorrect answer: -10 points
        """
        self.attempts[topic] += 1
        current_mastery = self.mastery[topic]

        if is_correct:
            new_mastery = min(100, current_mastery + 5)
        else:
            new_mastery = max(0, current_mastery - 10)
        
        self.mastery[topic] = new_mastery
        
        self.history.append({
            'topic': topic,
            'correct': is_correct,
            'mastery_after': new_mastery
        })

    def get_mastery_report(self):
        """
        Generates a summary report of the student's performance.
        """
        report = {
            'strengths': [],
            'weak_areas': [],
            'focus_topic': None
        }
        
        sorted_mastery = sorted(self.mastery.items(), key=lambda item: item[1], reverse=True)
        
        # Determine strengths (mastery > 75) and weaknesses (mastery < 50)
        for topic, score in sorted_mastery:
            if score > 75:
                report['strengths'].append(f"{topic} ({score}%)")
            elif score < 50:
                report['weak_areas'].append(f"{topic} ({score}%)")
        
        # Recommended focus topic: Lowest mastery and attempted at least once
        lowest_mastery_topic = min(
            (score, topic) 
            for topic, score in self.mastery.items() 
            if self.attempts[topic] > 0
        )
        report['focus_topic'] = lowest_mastery_topic[1] if lowest_mastery_topic else sorted_mastery[-1][0]
        
        return report