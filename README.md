# Dugg

**Answer-first search.** Ask a factual question, get one plain answer — or an honest "I don't know" instead of a page of guesses to sift through.

## What it does

Dugg takes a short factual query (a capital city, a population, a unit conversion, a percentage) and returns a single stated answer with its confidence, source, and query type. Below a confidence threshold, the result is shown as *unresolved* rather than dressed up as fact.

## Tech

- Static single-page frontend (`dugg.html`) — no build step, no framework
- Fonts: Fraunces (display/serif), Inter (UI), IBM Plex Mono (data labels)
- Talks to a backend over a simple `GET /search?q=` endpoint

## Running locally

1. Start your backend (see your API repo) and note the URL it runs on.
2. Open `dugg.html` and set `API_BASE` near the top of the `<script>` block to that URL.
3. Open the file in a browser — no server required for the frontend itself.

## API contract

The frontend expects `GET {API_BASE}/search?q=<query>` to return JSON:

```json
{
  "answer": "New Delhi",
  "confidence": 0.97,
  "source": "wikidata",
  "query_type": "capital"
}
```

- `confidence >= 0.5` renders as **confirmed** (green)
- `confidence < 0.5` renders as **unresolved** (amber)

## Status

Frontend UI is functional; backend is expected to be hosted separately (Render/Railway/etc.) and pointed to via `API_BASE`.
