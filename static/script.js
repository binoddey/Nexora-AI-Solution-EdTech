let currentQuestion = null;

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadNext();
});

async function loadNext() {
    document.getElementById('feedback-area').classList.add('hidden');
    document.getElementById('question-area').classList.remove('hidden');
    document.getElementById('answer-input').value = '';

    try {
        const response = await fetch('/api/next_question');
        const data = await response.json();

        // CHECK FOR GRADUATION
        if (data.status === "graduated") {
            showGraduationScreen();
            return;
        }

        currentQuestion = data;
        document.getElementById('topic-label').innerText = currentQuestion.topic;
        document.getElementById('question-text').innerText = currentQuestion.question;
        document.getElementById('answer-input').focus();
    } catch (err) {
        console.error("Failed to load:", err);
    }
}

function showGraduationScreen() {
    // 1. Fire Confetti!
    confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 }
    });

    // 2. Transform the UI
    const card = document.getElementById('quiz-card');
    card.innerHTML = `
        <div style="text-align: center; padding: 40px 20px;">
            <div style="font-size: 80px; margin-bottom: 20px;">🎓</div>
            <h1 style="color: #4f46e5; margin-bottom: 10px;">Module Mastered!</h1>
            <p style="color: #6b7280; margin-bottom: 30px;">
                You've demonstrated 100% proficiency in Fractions and Decimals.
            </p>
            <button onclick="window.location.reload()" style="max-width: 200px;">
                Restart Journey
            </button>
        </div>
    `;
}

async function checkAnswer() {
    const userAnswer = document.getElementById('answer-input').value.trim();
    if (!userAnswer) return;

    // Check correctness (case insensitive)
    const isCorrect = userAnswer.toLowerCase() === currentQuestion.answer.toLowerCase();

    // Send result to backend to update ML Student Model
    const response = await fetch('/api/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            topic: currentQuestion.topic,
            is_correct: isCorrect
        })
    });

    const data = await response.json();

    // Update UI state
    updateUI(isCorrect, data.new_mastery);
}

function updateUI(isCorrect, newMastery) {
    // 1. Hide question, show feedback
    document.getElementById('question-area').classList.add('hidden');
    const feedbackArea = document.getElementById('feedback-area');
    feedbackArea.classList.remove('hidden');

    const msg = document.getElementById('feedback-msg');
    if (isCorrect) {
        msg.innerText = "Fantastic! You nailed it.";
        msg.className = "correct-msg";
        document.getElementById('solution-text').innerText = "";
    } else {
        msg.innerText = "Not quite right...";
        msg.className = "error-msg";
        document.getElementById('solution-text').innerText = `Correct Answer: ${currentQuestion.answer}`;
    }

    // 2. Update Mastery progress
    document.getElementById('mastery-val').innerText = newMastery;
    document.getElementById('progress-bar').style.width = newMastery + "%";
}