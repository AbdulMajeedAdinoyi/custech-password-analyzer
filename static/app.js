const pwInput = document.getElementById("pw");
const bar = document.getElementById("bar");
const categoryEl = document.getElementById("category");
const tipsEl = document.getElementById("tips");
const breachEl = document.getElementById("breach");

async function score(password) {
  const res = await fetch("/api/score", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ password })
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

function setMeter(score, category) {
  bar.style.width = `${Math.max(5, score)}%`; // keep visible bar
  categoryEl.textContent = `${category} (${score})`;
  bar.style.background =
    category === "Weak" ? "var(--weak)" :
    category === "Moderate" ? "var(--moderate)" :
    "var(--strong)";
}

function setTips(tips) {
  tipsEl.innerHTML = "";
  if (!tips || tips.length === 0) {
    const li = document.createElement("li");
    li.textContent = "No issues detected";
    tipsEl.appendChild(li);
    return;
  }
  tips.forEach(t => {
    const li = document.createElement("li");
    li.textContent = t;
    tipsEl.appendChild(li);
  });
}

pwInput.addEventListener("input", async (e) => {
  const val = e.target.value;
  if (!val) {
    bar.style.width = "0%";
    categoryEl.textContent = "Waiting...";
    tipsEl.innerHTML = "<li>Start typing to see feedback</li>";
    breachEl.textContent = "Not checked";
    breachEl.style.color = "var(--text)";
    return;
  }

  // Show analyzing status while waiting
  categoryEl.textContent = "Analyzing...";
  breachEl.textContent = "Checking...";
  breachEl.style.color = "var(--accent-light)";

  try {
    const result = await score(val);
    setMeter(result.score, result.category);
    setTips(result.feedback);

    // Color breach check dynamically
    breachEl.textContent = result.compromised ? "Compromised" : "Not compromised";
    breachEl.style.color = result.compromised ? "var(--weak)" : "var(--accent-green)";
  } catch (err) {
    categoryEl.textContent = "Error scoring password";
    breachEl.textContent = "Error";
    breachEl.style.color = "var(--weak)";
  }
});