"""
Dugg query engine.

Philosophy: understand the query well enough to answer it directly,
or say plainly that we can't -- never pad with irrelevant results.

Pipeline:
  1. classify()   -> figure out what TYPE of question this is
  2. route()      -> send it to the right handler for that type
  3. each handler returns (answer, confidence, source) or None

If nothing matches with enough confidence, we return a clear
"not confident" response instead of guessing.
"""

import re
import json
import os
from dataclasses import dataclass
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(DATA_DIR, "countries.json"), encoding="utf-8") as f:
    COUNTRIES = json.load(f)


@dataclass
class Answer:
    text: str
    confidence: float          # 0.0 - 1.0
    source: str
    query_type: str


# ---------------------------------------------------------------------------
# 1. Query classification
# ---------------------------------------------------------------------------

FACT_PATTERNS = {
    "capital": re.compile(r"\bcapital\s+of\s+([a-z\s]+?)\??$", re.I),
    "population": re.compile(r"\bpopulation\s+of\s+([a-z\s]+?)\??$", re.I),
    "currency": re.compile(r"\bcurrency\s+of\s+([a-z\s]+?)\??$", re.I),
    "language": re.compile(r"\b(?:official\s+)?language\s+of\s+([a-z\s]+?)\??$", re.I),
    "continent": re.compile(r"\bcontinent\s+is\s+([a-z\s]+?)\s+in\??$|\bwhat\s+continent\s+is\s+([a-z\s]+?)\s+in\??$", re.I),
}

MATH_PATTERN = re.compile(r"^[\d\s\.\+\-\*\/\(\)%]+$")
PERCENT_OF_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)", re.I)

UNIT_CONVERSIONS = {
    ("km", "miles"): 0.621371,
    ("miles", "km"): 1.60934,
    ("kg", "lbs"): 2.20462,
    ("lbs", "kg"): 0.453592,
    ("celsius", "fahrenheit"): None,   # handled specially
    ("fahrenheit", "celsius"): None,
}
UNIT_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(km|miles|kg|lbs|celsius|fahrenheit)\s+(?:to|in)\s+(km|miles|kg|lbs|celsius|fahrenheit)",
    re.I,
)


def classify(query: str) -> str:
    """Return a rough query-type label. This is the 'understand the
    query' step -- everything downstream depends on getting this right."""
    q = query.strip().lower()

    if UNIT_PATTERN.search(q):
        return "unit_conversion"
    if PERCENT_OF_PATTERN.search(q):
        return "math"
    if MATH_PATTERN.match(q.replace(" ", "")):
        return "math"
    for label, pattern in FACT_PATTERNS.items():
        if pattern.search(q):
            return f"country_fact:{label}"
    if any(q.startswith(p) for p in ["who is", "who was"]):
        return "unsupported:person"
    return "unknown"


# ---------------------------------------------------------------------------
# 2. Handlers
# ---------------------------------------------------------------------------

def _lookup_country(name: str) -> Optional[dict]:
    name = name.strip().lower()
    return COUNTRIES.get(name)


def handle_country_fact(query: str, fact_key: str) -> Optional[Answer]:
    q = query.strip().lower().rstrip("?")
    pattern = FACT_PATTERNS[fact_key]
    m = pattern.search(q)
    if not m:
        return None
    country_name = next((g for g in m.groups() if g), "").strip()
    data = _lookup_country(country_name)
    if not data or fact_key not in data:
        return Answer(
            text=f"I don't have a fact on file for '{country_name.title()}'. "
                 f"Try one of the ~24 countries currently in the knowledge base.",
            confidence=0.0,
            source="local knowledge base",
            query_type=f"country_fact:{fact_key}",
        )
    label = fact_key.replace("_", " ")
    return Answer(
        text=f"The {label} of {country_name.title()} is {data[fact_key]}.",
        confidence=0.95,
        source="local knowledge base",
        query_type=f"country_fact:{fact_key}",
    )


def handle_math(query: str) -> Optional[Answer]:
    q = query.strip().lower()
    pm = PERCENT_OF_PATTERN.search(q)
    if pm:
        pct, base = float(pm.group(1)), float(pm.group(2))
        result = pct / 100 * base
        return Answer(
            text=f"{pm.group(1)}% of {pm.group(2)} is {result:g}.",
            confidence=1.0,
            source="calculation",
            query_type="math",
        )
    expr = q.replace(" ", "")
    if MATH_PATTERN.match(expr):
        try:
            # restricted eval: only digits/operators reach this point
            result = eval(expr, {"__builtins__": {}}, {})
            return Answer(
                text=f"{query.strip()} = {result:g}" if isinstance(result, float) else f"{query.strip()} = {result}",
                confidence=1.0,
                source="calculation",
                query_type="math",
            )
        except Exception:
            return None
    return None


def handle_unit_conversion(query: str) -> Optional[Answer]:
    m = UNIT_PATTERN.search(query.lower())
    if not m:
        return None
    value, from_unit, to_unit = float(m.group(1)), m.group(2), m.group(3)

    if {from_unit, to_unit} == {"celsius", "fahrenheit"}:
        if from_unit == "celsius":
            result = value * 9 / 5 + 32
        else:
            result = (value - 32) * 5 / 9
    else:
        factor = UNIT_CONVERSIONS.get((from_unit, to_unit))
        if factor is None:
            return None
        result = value * factor

    return Answer(
        text=f"{value:g} {from_unit} = {result:.2f} {to_unit}",
        confidence=1.0,
        source="calculation",
        query_type="unit_conversion",
    )


# ---------------------------------------------------------------------------
# 3. Router
# ---------------------------------------------------------------------------

def answer(query: str) -> Answer:
    if not query or not query.strip():
        return Answer("Type a question to search.", 0.0, "n/a", "empty")

    qtype = classify(query)

    if qtype.startswith("country_fact:"):
        fact_key = qtype.split(":", 1)[1]
        result = handle_country_fact(query, fact_key)
        if result:
            return result

    if qtype == "math":
        result = handle_math(query)
        if result:
            return result

    if qtype == "unit_conversion":
        result = handle_unit_conversion(query)
        if result:
            return result

    if qtype == "unsupported:person":
        return Answer(
            text="Dugg's factual mode doesn't cover people yet -- only "
                 "countries, math, and unit conversions in this build.",
            confidence=0.0,
            source="n/a",
            query_type=qtype,
        )

    return Answer(
        text="I'm not confident I can answer that precisely with what's "
             "currently in Dugg's knowledge base, rather than guess. "
             "Try a country fact (capital/population/currency/language of X), "
             "a calculation, or a unit conversion.",
        confidence=0.0,
        source="n/a",
        query_type="unknown",
    )
