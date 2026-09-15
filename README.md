<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Dugg is an answer-first search engine: one plain factual answer, or an honest 'I don't know' — never a page of guesses.">
<title>Dugg</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23171A1D'/%3E%3Ccircle cx='22' cy='23' r='4.2' fill='%232F5233'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --paper: #FAF8F3;
    --ink: #171A1D;
    --muted: #6E6A61;
    --line: #DEDACD;
    --confirmed: #2F5233;
    --confirmed-bg: #EEF2EA;
    --unresolved: #A8571C;
    --unresolved-bg: #FBF0E6;
  }

  * { box-sizing: border-box; }

  body {
    margin: 0;
    background: var(--paper);
    color: var(--ink);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
  }

  :focus-visible {
    outline: 2px solid var(--ink);
    outline-offset: 2px;
  }

  @media (prefers-reduced-motion: reduce) {
    * { animation-duration: 0.001ms !important; transition-duration: 0.001ms !important; }
  }

  /* ---------- top bar (hidden until a search has been made) ---------- */

  header {
    display: none;
    align-items: center;
    gap: 20px;
    padding: 16px 20px;
    border-bottom: 1px solid var(--line);
    position: sticky;
    top: 0;
    background: var(--paper);
    z-index: 5;
  }

  header.visible { display: flex; }

  .logo-small {
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: var(--ink);
    text-decoration: none;
    flex-shrink: 0;
    cursor: pointer;
  }

  .logo-small span { color: var(--confirmed); }

  .search-pill {
    flex: 1;
    max-width: 620px;
    display: flex;
    align-items: center;
    gap: 10px;
    background: #fff;
    border: 1.5px solid var(--line);
    border-radius: 999px;
    padding: 9px 16px;
    transition: border-color 0.15s, box-shadow 0.15s;
  }

  .search-pill:focus-within {
    border-color: var(--ink);
    box-shadow: 0 2px 10px rgba(23,26,29,0.08);
  }

  .search-pill svg { flex-shrink: 0; opacity: 0.5; }

  .search-pill input {
    border: none;
    outline: none;
    flex: 1;
    width: 100%;
    min-width: 0;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    background: transparent;
    color: var(--ink);
  }

  /* ---------- centered homepage state ---------- */

  .home {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: clamp(8vh, 14vh, 20vh) 20px 40px;
  }

  .home.hidden { display: none; }

  .wordmark {
    font-family: 'Fraunces', serif;
    font-size: clamp(2.6rem, 9vw, 4.2rem);
    font-weight: 600;
    letter-spacing: -0.02em;
    margin: 0;
  }

  .wordmark span { color: var(--confirmed); }

  .tagline {
    color: var(--muted);
    font-size: 1.02rem;
    margin: 12px 0 40px;
    max-width: 36ch;
    text-align: center;
    line-height: 1.55;
  }

  .home-search-pill {
    width: 100%;
    max-width: 600px;
    display: flex;
    align-items: center;
    gap: 12px;
    background: #fff;
    border: 1.5px solid var(--line);
    border-radius: 999px;
    padding: 15px 20px;
    box-shadow: 0 1px 6px rgba(23,26,29,0.05);
    transition: border-color 0.15s, box-shadow 0.15s;
  }

  .home-search-pill:focus-within {
    border-color: var(--ink);
    box-shadow: 0 4px 16px rgba(23,26,29,0.1);
  }

  .home-search-pill svg { flex-shrink: 0; opacity: 0.45; }

  .home-search-pill input {
    border: none;
    outline: none;
    flex: 1;
    min-width: 0;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    background: transparent;
    color: var(--ink);
  }

  .home-buttons {
    display: flex;
    gap: 10px;
    margin-top: 24px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .btn {
    border: none;
    background: #F0EDE3;
    color: var(--ink);
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    padding: 10px 18px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.12s;
  }

  .btn:hover { background: #E6E2D4; }

  .btn.primary { background: var(--ink); color: var(--paper); }
  .btn.primary:hover { opacity: 0.88; background: var(--ink); }

  .chip-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 28px;
    max-width: 480px;
  }

  .chip {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
    color: var(--muted);
    background: #F0EDE3;
    border: none;
    padding: 5px 11px;
    border-radius: 999px;
    cursor: pointer;
    transition: background 0.12s, color 0.12s;
  }

  .chip:hover { background: #E6E2D4; color: var(--ink); }

  .shortcut-hint {
    margin-top: 18px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    opacity: 0.7;
  }

  .shortcut-hint kbd {
    font-family: inherit;
    background: #F0EDE3;
    border-radius: 3px;
    padding: 1px 5px;
  }

  /* ---------- results state ---------- */

  main.results {
    display: none;
    max-width: 640px;
    margin: 0 auto;
    padding: 28px 20px 60px;
  }

  main.results.visible { display: block; }

  .results-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    margin-bottom: 16px;
    word-break: break-word;
  }

  .result {
    padding: 24px 22px;
    border-left: 3px solid var(--line);
    border-radius: 4px;
    transition: background 0.2s, border-color 0.2s;
  }

  .result.confirmed { border-left-color: var(--confirmed); background: var(--confirmed-bg); }
  .result.unresolved { border-left-color: var(--unresolved); background: var(--unresolved-bg); }

  .result-text {
    font-family: 'Fraunces', serif;
    font-size: clamp(1.2rem, 4.2vw, 1.5rem);
    line-height: 1.45;
    margin: 0 0 16px;
  }

  .result-text.loading::after {
    content: '';
    display: inline-block;
    width: 1.2em;
    text-align: left;
    animation: dots 1.2s steps(4, end) infinite;
  }

  @keyframes dots {
    0%   { content: ''; }
    25%  { content: '.'; }
    50%  { content: '..'; }
    75%  { content: '...'; }
    100% { content: ''; }
  }

  .result-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  .result-meta .badge {
    padding: 2px 8px;
    border-radius: 999px;
    background: rgba(0,0,0,0.05);
  }

  footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.78rem;
    padding: 40px 24px 24px;
  }

  @media (max-width: 460px) {
    header { gap: 14px; padding: 14px 16px; }
    .logo-small { font-size: 1.2rem; }
    .home-buttons { width: 100%; }
    .btn { flex: 1; text-align: center; }
    .result { padding: 20px 18px; }
  }
</style>
</head>
<body>

  <header id="top-header">
    <a class="logo-small" id="logo-small" href="#">dugg<span>.</span></a>
    <form id="top-search-form" style="flex:1; display:flex; min-width:0;">
      <div class="search-pill">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="text" id="top-query" placeholder="capital of india" autocomplete="off" aria-label="Search Dugg">
      </div>
    </form>
  </header>

  <div class="home" id="home">
    <h1 class="wordmark">dugg<span>.</span></h1>
    <p class="tagline">One answer, stated plainly — or an honest "I don't know" instead of ten pages of guesses.</p>

    <form id="home-search-form" style="width:100%; display:flex; justify-content:center;">
      <div class="home-search-pill">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input type="text" id="home-query" placeholder="Ask Dugg anything factual…" autocomplete="off" autofocus aria-label="Ask Dugg a factual question">
      </div>
    </form>

    <div class="home-buttons">
      <button class="btn primary" id="ask-btn">Ask Dugg</button>
      <button class="btn" id="lucky-btn">Surprise Me</button>
    </div>

    <div class="chip-row">
      <button class="chip" data-q="capital of india">capital of india</button>
      <button class="chip" data-q="population of japan">population of japan</button>
      <button class="chip" data-q="15% of 200">15% of 200</button>
      <button class="chip" data-q="10 km to miles">10 km to miles</button>
      <button class="chip" data-q="25 celsius to fahrenheit">25 celsius to fahrenheit</button>
    </div>

    <p class="shortcut-hint">Press <kbd>/</kbd> to search from anywhere</p>
  </div>

  <main class="results" id="results-view">
    <div class="results-label" id="results-label"></div>
    <div class="result" id="result">
      <p class="result-text" id="result-text" aria-live="polite"></p>
      <div class="result-meta">
        <span class="badge" id="result-confidence"></span>
        <span id="result-source"></span>
        <span id="result-type"></span>
      </div>
    </div>
  </main>

  <footer id="page-footer">Dugg — answer-first search, built to be precise before it's exhaustive.</footer>

<script>
  // 👇 PASTE YOUR DEPLOYED BACKEND URL HERE (from Render/Railway/etc.), no trailing slash
  const API_BASE = "http://localhost:8000";

  const SAMPLE_QUERIES = ["capital of india", "population of japan", "15% of 200", "10 km to miles", "25 celsius to fahrenheit", "currency of france"];

  const homeView = document.getElementById("home");
  const resultsView = document.getElementById("results-view");
  const topHeader = document.getElementById("top-header");
  const homeForm = document.getElementById("home-search-form");
  const topForm = document.getElementById("top-search-form");
  const homeInput = document.getElementById("home-query");
  const topInput = document.getElementById("top-query");
  const resultBox = document.getElementById("result");
  const resultText = document.getElementById("result-text");
  const resultConfidence = document.getElementById("result-confidence");
  const resultSource = document.getElementById("result-source");
  const resultType = document.getElementById("result-type");
  const resultsLabel = document.getElementById("results-label");

  async function runSearch(q) {
    if (!q || !q.trim()) return;

    // switch to results layout
    homeView.classList.add("hidden");
    topHeader.classList.add("visible");
    resultsView.classList.add("visible");
    topInput.value = q;

    resultsLabel.textContent = `results for "${q}"`;
    resultText.textContent = "Thinking";
    resultText.classList.add("loading");
    resultConfidence.textContent = "";
    resultSource.textContent = "";
    resultType.textContent = "";
    resultBox.className = "result";

    try {
      const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(q)}`);
      if (!res.ok) throw new Error(`Backend returned ${res.status}`);
      const data = await res.json();

      resultText.classList.remove("loading");
      resultText.textContent = data.answer ?? "No answer returned.";
      const confidence = typeof data.confidence === "number" ? data.confidence : 0;
      resultConfidence.textContent = `confidence: ${(confidence * 100).toFixed(0)}%`;
      resultSource.textContent = `source: ${data.source ?? "unknown"}`;
      resultType.textContent = `type: ${data.query_type ?? "unknown"}`;
      resultBox.className = "result " + (confidence >= 0.5 ? "confirmed" : "unresolved");
    } catch (err) {
      resultText.classList.remove("loading");
      resultText.textContent = "Couldn't reach the Dugg backend. Is it running at " + API_BASE + "?";
      resultBox.className = "result unresolved";
    }
  }

  homeForm.addEventListener("submit", (e) => { e.preventDefault(); runSearch(homeInput.value); });
  topForm.addEventListener("submit", (e) => { e.preventDefault(); runSearch(topInput.value); });

  document.getElementById("ask-btn").addEventListener("click", () => runSearch(homeInput.value));
  document.getElementById("lucky-btn").addEventListener("click", () => {
    const q = SAMPLE_QUERIES[Math.floor(Math.random() * SAMPLE_QUERIES.length)];
    homeInput.value = q;
    runSearch(q);
  });

  document.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => runSearch(chip.dataset.q));
  });

  document.getElementById("logo-small").addEventListener("click", (e) => {
    e.preventDefault();
    resultsView.classList.remove("visible");
    topHeader.classList.remove("visible");
    homeView.classList.remove("hidden");
    homeInput.value = "";
    homeInput.focus();
  });

  // "/" focuses the active search box, unless the user is already typing somewhere
  document.addEventListener("keydown", (e) => {
    if (e.key !== "/" ) return;
    const tag = document.activeElement.tagName;
    if (tag === "INPUT" || tag === "TEXTAREA") return;
    e.preventDefault();
    (topHeader.classList.contains("visible") ? topInput : homeInput).focus();
  });
</script>

</body>
</html>
