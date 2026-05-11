// ── Language Pills ────────────────────────────────────────────────────────────
document.querySelectorAll(".lang-pill").forEach((pill) => {
  pill.addEventListener("click", () => {
    pill.classList.toggle("active");
  });
});

function getSelectedLanguages() {
  return Array.from(document.querySelectorAll(".lang-pill.active")).map(
    (p) => p.dataset.lang,
  );
}

// ── Generate Query ────────────────────────────────────────────────────────────
let lastGeneratedQuery = "";

async function generateQuery() {
  const keyword = document.getElementById("keyword").value.trim();
  const operator = document.getElementById("operator").value;
  const languages = getSelectedLanguages();
  const output = document.getElementById("output");
  const btn = document.getElementById("generateBtn");
  const outputContainer = document.getElementById("outputContainer");

  if (!keyword) {
    showToast("⚠️ Please enter a keyword!", "warning");
    return;
  }
  if (languages.length === 0) {
    showToast("⚠️ Please select at least one language!", "warning");
    return;
  }

  // Loading state
  btn.classList.add("loading");

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keyword, languages, operator }),
    });

    const data = await response.json();
    lastGeneratedQuery = data.raw_query;

    output.value = lastGeneratedQuery;
    outputContainer.classList.add("show");
  } catch (err) {
    console.error(err);
    output.value = "Error generating query. Please try again.";
    outputContainer.classList.add("show");
  } finally {
    btn.classList.remove("loading");
  }
}

// ── Open Opoint ───────────────────────────────────────────────────────────────
function openOpoint() {
  if (!lastGeneratedQuery) {
    showToast("⚠️ Generate a query first!", "warning");
    return;
  }
  const encoded = encodeURIComponent(lastGeneratedQuery);
  const url = `https://m360.opoint.com/search/?expression=${encoded}&filters=geo:1144`;
  window.open(url, "_blank");
}

// ── Copy Query ────────────────────────────────────────────────────────────────
function copyQuery() {
  const output = document.getElementById("output");
  if (
    !output.value ||
    output.value === "Your generated query will appear here..."
  ) {
    showToast("⚠️ Nothing to copy!", "warning");
    return;
  }

  navigator.clipboard.writeText(output.value).then(() => {
    const btn = document.getElementById("copyBtn");
    btn.classList.add("copied");
    btn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    showToast("✅ Query copied to clipboard!");

    setTimeout(() => {
      btn.classList.remove("copied");
      btn.innerHTML = '<i class="fas fa-copy"></i> Copy';
    }, 2000);
  });
}

// ── Toast Notification ────────────────────────────────────────────────────────
function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  const toastMsg = document.getElementById("toastMsg");

  toastMsg.textContent = message;
  toast.classList.add("show");

  if (type === "warning") {
    toast.style.borderColor = "var(--warning)";
    toast.querySelector("i").style.color = "var(--warning)";
  } else {
    toast.style.borderColor = "var(--success)";
    toast.querySelector("i").style.color = "var(--success)";
  }

  setTimeout(() => toast.classList.remove("show"), 3000);
}

// ── Enter Key Support ─────────────────────────────────────────────────────────
document.getElementById("keyword").addEventListener("keypress", (e) => {
  if (e.key === "Enter") generateQuery();
});
