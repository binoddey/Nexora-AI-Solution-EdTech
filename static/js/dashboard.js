document.addEventListener("DOMContentLoaded", loadDashboard);

function loadDashboard() {
  fetch("/api/subject_report/Mathematics")
    .then(res => res.json())
    .then(data => {
      renderMastery(data.mastery_overview);
      renderList("strengths", data.strengths);
      renderList("weaknesses", data.weak_areas);
      renderAI(data.focus_topic, data.ai_reasoning);
    })
    .catch(err => console.error(err));
}

function renderMastery(mastery) {
  const container = document.getElementById("masteryContainer");
  container.innerHTML = "";

  Object.entries(mastery).forEach(([topic, value]) => {
    container.innerHTML += `
      <div style="margin-bottom:8px">
        <strong>${topic} (${value}%)</strong>
        <div style="background:#e5e7eb;height:6px;border-radius:4px">
          <div style="width:${value}%;height:6px;background:#2563eb;border-radius:4px"></div>
        </div>
      </div>
    `;
  });
}

function renderList(id, items) {
  const ul = document.getElementById(id);
  ul.innerHTML = items.length
    ? items.map(i => `<li>${i}</li>`).join("")
    : "<li>—</li>";
}

function renderAI(topic, reason) {
  document.getElementById("focusTopic").innerText =
    `Focus on ${topic}`;
  document.getElementById("aiReason").innerText = reason;
}
