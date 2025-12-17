from flask import Flask, render_template, jsonify, request, session
import json
from ml_engine import AdaptiveML

app = Flask(__name__)
app.secret_key = "hackathon_super_secret_key" # Fixes session issues
ai = AdaptiveML()

# Load Data
try:
    with open('data.json', 'r') as f:
        db = json.load(f)
except Exception as e:
    print(f"Error loading data.json: {e}")

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/api/next_question', methods=['GET'])
def get_next_adaptive_question():
    mastery = db['student']['mastery']
    
    # NEW: If mastery is 100, tell the frontend to graduate
    if mastery >= 100:
        return jsonify({"status": "graduated"})

    if 'seen_ids' not in session:
        session['seen_ids'] = []

    available_questions = [q for q in db['questions'] if q['id'] not in session['seen_ids']]
    
    # If bank exhausted, reset history
    if not available_questions:
        available_questions = db['questions']
        session['seen_ids'] = []

    question = ai.get_best_question(mastery, available_questions)
    
    history = session['seen_ids']
    history.append(question['id'])
    session['seen_ids'] = history
    
    # Add a normal status so JS knows to continue
    question_data = question.copy()
    question_data["status"] = "continue"
    return jsonify(question_data)

@app.route('/api/submit', methods=['POST'])
def handle_submission(): # Unique name
    data = request.json
    is_correct = data['is_correct']
    
    # Update Mastery in memory (for the demo)
    if is_correct:
        db['student']['mastery'] = min(100, db['student']['mastery'] + 8)
    else:
        db['student']['mastery'] = max(0, db['student']['mastery'] - 5)
    
    return jsonify({"new_mastery": db['student']['mastery']})

if __name__ == '__main__':
    app.run(debug=True)