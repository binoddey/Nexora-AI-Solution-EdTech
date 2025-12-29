let currentTopic = null;

document.addEventListener("DOMContentLoaded", loadDashboard);

function loadDashboard() {
  fetch("/api/subject_report/Mathematics")
    .then(res => res.json())
    .then(renderDashboard);
}

function renderDashboard(data) {
  const mastery = document.getElementById("masteryContainer");
  mastery.innerHTML = "";

  Object.entries(data.mastery_overview).forEach(([topic, value]) => {
    mastery.innerHTML += `
      <div class="progress">
        <strong>${topic} (${value}%)</strong>
        <div class="bar">
          <div class="fill" style="width:${value}%"></div>
        </div>
      </div>
    `;
  });

  document.getElementById("strengths").innerHTML =
    data.strengths.map(t => `<li>${t}</li>`).join("");

  document.getElementById("weaknesses").innerHTML =
    data.weak_areas.map(t => `<li>${t}</li>`).join("");

  document.getElementById("focusTopic").innerText =
    `Focus on ${data.focus_topic}`;

  document.getElementById("aiReason").innerText =
    data.ai_reasoning;

  const buttons = document.getElementById("practiceButtons");
  buttons.innerHTML = "";

  Object.keys(data.mastery_overview).forEach(topic => {
    buttons.innerHTML += `
      <button onclick="startPractice('${topic}')">
        Practice ${topic}
      </button>
    `;
  });
}

function startPractice(topic) {
  currentTopic = topic;

  fetch(`/api/practice/Mathematics/${topic}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("practiceArea").classList.remove("hidden");
      document.getElementById("questionTopic").innerText = data.topic;
      document.getElementById("questionText").innerText = data.question;
      document.getElementById("difficulty").innerText =
        `Difficulty: ${data.difficulty}`;
      document.getElementById("predicted").innerText =
        `Predicted Success: ${Math.round(data.predicted_success * 100)}%`;
    });
}

function submitAnswer(correct) {
  fetch("/api/submit", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      topic: currentTopic,
      correct: correct
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("feedback").innerText =
      data.learning_feedback;
    loadDashboard();
  });
}
