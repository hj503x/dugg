# Dugg

An answer-first search engine. Instead of returning pages of links, Dugg tries
to understand what you're actually asking and give you one direct answer —
or an honest "I don't know" when it isn't confident, rather than guessing.

This is the v0 build: **factual queries only, no live web retrieval.**
It answers from a small local knowledge base plus a couple of computable
fact types, so the query-understanding pipeline is visible and easy to extend.

## What it can answer right now

- **Country facts** — capital, population, currency, and language for ~24
  countries. e.g. `capital of india`, `currency of france`
- **Math** — basic arithmetic and percentages. e.g. `15% of 200`, `(4+5)*3`
- **Unit conversions** — km/miles, kg/lbs, celsius/fahrenheit.
  e.g. `10 km to miles`, `25 celsius to fahrenheit`

Anything outside that returns a clear "not confident" response instead of a
guess — that's a deliberate design choice, not a missing feature. See
`backend/query_engine.py` for the confidence logic.

## How it's built

```
dugg/
├── backend/
│   ├── main.py           FastAPI app, exposes GET/POST /search
│   ├── query_engine.py   classify() -> route() -> handler -> Answer
│   └── data/
│       └── countries.json
├── frontend/
│   └── index.html        single-page UI, no build step
├── requirements.txt
└── README.md
```

The pipeline is: **classify the query type first, then answer** — not
"search everything and rank it." That's the core bet of the whole project:
query understanding does more work than retrieval volume.

## Running it locally

```bash
# backend
cd backend
pip install -r ../requirements.txt
uvicorn main:app --reload --port 8000

# frontend — just open frontend/index.html in a browser
# (it calls http://localhost:8000 by default)
```

## Extending it

- **New fact type**: add a regex to `FACT_PATTERNS` in `query_engine.py` and
  a handler function, or add a new dataset under `backend/data/`.
- **More countries**: add entries to `backend/data/countries.json`.
- **Live web retrieval**: this is the natural next step — swap the
  "unknown" fallback in `answer()` for a real search + synthesis call,
  but keep the same confidence-gated pattern so it still says "I don't
  know" instead of confidently hallucinating.

## Roadmap (not yet built)

- Person / entity lookups ("who is X")
- Live web retrieval + synthesis for the long tail
- A real classifier (embeddings or a small model) instead of regex,
  once query variety outgrows pattern matching
