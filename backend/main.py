from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from query_engine import answer as get_answer

app = FastAPI(title="Dugg", description="Answer-first factual search engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"status": "Dugg backend running", "try": "/search?q=capital of india"}


@app.get("/search")
def search_get(q: str):
    result = get_answer(q)
    return {
        "query": q,
        "answer": result.text,
        "confidence": result.confidence,
        "source": result.source,
        "query_type": result.query_type,
    }


@app.post("/search")
def search_post(req: SearchRequest):
    result = get_answer(req.query)
    return {
        "query": req.query,
        "answer": result.text,
        "confidence": result.confidence,
        "source": result.source,
        "query_type": result.query_type,
    }
