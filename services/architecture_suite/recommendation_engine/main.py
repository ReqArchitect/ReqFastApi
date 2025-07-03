from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Recommendation Engine", version="0.1.0")

class Recommendation(BaseModel):
    suggestion: str
    score: float
    rationale: str

@app.get("/recommendations/{package_id}", response_model=List[Recommendation])
def get_recommendations(package_id: str):
    # Stub: Ingest metrics, run rule-based/ML logic
    # Example: If package_id is even, suggest decomposition
    recs = []
    if int(package_id[-1], 16) % 2 == 0:
        recs.append(Recommendation(
            suggestion="Consider decomposing large packages",
            score=0.85,
            rationale="Package size exceeds recommended threshold."
        ))
    recs.append(Recommendation(
        suggestion="Increase partition size",
        score=0.65,
        rationale="Observed high load in recent metrics."
    ))
    return recs
