const params = new URLSearchParams(window.location.search);
const currentTopic = params.get("topic");

if (!currentTopic) {
  document.getElementById("questionText").innerText =
    "No topic selected. Go back and choose a topic.";
  throw new Error("Topic missing in URL");
}

let currentQuestion = null;

document.addEventListener("DOMContentLoaded", loadQuestion);

function loadQuestion() {
  document.getElementById("feedback").innerText = "";
  document.getElementById("answerInput").value = "";

  fetch(`/api/practice/Mathematics/${currentTopic}`)
    .then(res => res.json())
    .then(data => {
      currentQuestion = data;

      document.getElementById("questionText").innerText = data.question;
      document.getElementById("difficulty").innerText =
        `Difficulty: ${data.difficulty}`;
      document.getElementById("prediction").innerText =
        `Predicted Success: ${Math.round(data.predicted_success * 100)}%`;
    });
}

function submitAnswer() {
  const answer = document.getElementById("answerInput").value;
  if (!answer) return;

  // For demo: assume non-empty = correct
  fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      topic: currentTopic,
      correct: true
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("feedback").innerText =
      data.learning_feedback;

    document.getElementById("masteryBadge").innerText =
      `Mastery: ${data.updated_mastery}%`;

    document.getElementById("progressFill").style.width =
      `${data.updated_mastery}%`;
  });
}

function nextQuestion() {
  loadQuestion();
}

function showHint() {
  document.getElementById("feedback").innerText =
    "Hint: Break the problem into smaller steps.";
}
