import json
import random

def generate_questions(count=100):
    questions = []
    for i in range(1, count + 1):
        # Rotate through topics and difficulties
        topic = random.choice(["Fractions", "Decimals", "Arithmetic"])
        diff = random.choice(["easy", "medium", "hard"])
        
        if topic == "Fractions":
            a, b = random.randint(1, 5), random.randint(1, 5)
            questions.append({
                "id": i,
                "topic": topic,
                "difficulty": diff,
                "question": f"What is {a}/10 + {b}/10?",
                "answer": f"{a+b}/10",
                "hint": "Add the numerators.",
                "solution": f"({a}+{b})/10 = {a+b}/10"
            })
        elif topic == "Decimals":
            val = round(random.uniform(0.1, 9.9), 1)
            questions.append({
                "id": i,
                "topic": topic,
                "difficulty": diff,
                "question": f"What is {val} + 1.0?",
                "answer": str(round(val + 1.0, 1)),
                "hint": "Add 1 to the whole number part.",
                "solution": f"{val} + 1.0 = {val+1.0}"
            })
        else: # Arithmetic
            num = random.randint(10, 100)
            questions.append({
                "id": i,
                "topic": topic,
                "difficulty": diff,
                "question": f"What is {num} - 5?",
                "answer": str(num - 5),
                "hint": "Subtract 5.",
                "solution": f"{num} - 5 = {num-5}"
            })
            
    data = {"questions": questions, "student": {"mastery": 50}}
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Successfully generated {count} questions in data.json!")

generate_questions(100)