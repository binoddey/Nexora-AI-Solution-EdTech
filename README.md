# Nexora - AI-Powered Adaptive Learning System

An **AI-driven student learning platform** that personalizes practice, identifies strengths and weaknesses, and explains *why* a student should focus on a particular topic — not just *what* to study.

This project demonstrates **adaptive learning + explainable AI**, built for clarity, not gimmicks.

---

## What This Project Does

The system continuously tracks a student’s learning state and adapts in real time by:

- Measuring **topic-wise mastery (0–100)**
- Identifying **strengths and weak areas**
- Recommending a **focus topic with reasoning**
- Serving **ML-optimized questions** at the right difficulty
- Updating mastery dynamically after every answer

All decisions are **transparent and explainable**.

---

## Core Features

### Student-Centric Dashboard
- Topic mastery overview
- Strengths & weaknesses
- AI recommendation with plain-English reasoning
- Clear next-step guidance

### Adaptive Quiz Experience
- Single quiz interface for all topics
- Topic-focused practice
- Difficulty adapts automatically
- ML selects questions near optimal challenge (~65% success)

### Explainable AI (Not a Black Box)
- Every recommendation includes:
- mastery analysis
- recent error patterns
- practice sufficiency
- Designed for judge evaluation & trust

---

## AI & ML Architecture

### StudentModel (State Layer)
Responsible for:
- Tracking mastery per topic
- Tracking attempts
- Maintaining recent answer history

> This layer **stores learning state only**.

---

### AdaptiveEngine (Pedagogical Layer)
Responsible for:
- Choosing difficulty level
- Deciding hint visibility
- Ensuring learning progression

> This layer models **how humans should be taught**.

---

### AdaptiveML (Optimization Layer)
Responsible for:
- Ranking questions by predicted success probability
- Keeping learning in the optimal challenge zone

> ML **optimizes**, but does not override pedagogy.

---

### AIExplanationEngine (Explainability Layer)
Responsible for:
- Deriving strengths & weaknesses
- Selecting focus topic
- Generating natural-language explanations

> This makes AI decisions **understandable and defensible**.

---


