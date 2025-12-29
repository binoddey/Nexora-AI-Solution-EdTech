# services/practice_service.py

class PracticeService:
    """
    Orchestrates topic-focused adaptive practice.
    Connects:
    - StudentModel (state)
    - AdaptiveEngine (pedagogy)
    - AdaptiveML (optimization)
    """

    def __init__(self, student_model, adaptive_engine, adaptive_ml, question_bank):
        """
        question_bank format:
        {
          "Mathematics": {
              "Fractions": [ {question_obj}, ... ],
              "Decimals":  [ ... ],
              "Arithmetic": [ ... ]
          }
        }
        """
        self.student = student_model
        self.engine = adaptive_engine
        self.ml = adaptive_ml
        self.question_bank = question_bank

    # -------------------------
    # Core Practice Flow
    # -------------------------

    def get_next_question(self, subject, forced_topic=None):
        """
        Return a single adaptive question.
        """

        # 1️⃣ Select topic (AI or forced)
        topic = self.engine.select_topic(
            self.student, forced_topic=forced_topic
        )

        # 2️⃣ Determine difficulty
        mastery = self.student.mastery[topic]
        difficulty = self.engine.select_difficulty(mastery)

        # 3️⃣ Fetch topic questions
        topic_questions = self._filter_questions(
            subject, topic, difficulty
        )

        if not topic_questions:
            return {
                "error": "No questions available for this topic and difficulty"
            }

        # 4️⃣ Rank questions using ML
        ranked = self.ml.rank_questions(
            topic_questions, mastery, difficulty
        )

        selected = ranked[0]

        # 5️⃣ Hint decision
        show_hint = self.engine.should_show_hint(
            self.student, topic
        )

        # 6️⃣ Assemble explainable response
        return {
            "question": selected["question"]["text"],
            "topic": topic,
            "difficulty": difficulty,
            "predicted_success": selected["predicted_success"],
            "show_hint": show_hint,
            "ai_reasoning": {
                "topic_reasoning": (
                    "User-selected topic"
                    if forced_topic
                    else self.student.get_ai_reasoning_for_focus()
                ),
                "difficulty_reasoning": self.engine.get_difficulty_reasoning(mastery),
                "ml_reasoning": self.ml.explain_prediction(mastery, difficulty),
                "hint_reasoning": (
                    self.engine.get_hint_reasoning(self.student, topic)
                    if show_hint else "No hint needed at this stage"
                )
            }
        }

    # -------------------------
    # Helpers
    # -------------------------

    def _filter_questions(self, subject, topic, difficulty):
        """
        Filter questions by subject, topic, and difficulty.
        Assumes each question has a 'difficulty' field.
        """
        all_questions = self.question_bank.get(subject, {}).get(topic, [])

        return [
            q for q in all_questions
            if q.get("difficulty") == difficulty
        ]
