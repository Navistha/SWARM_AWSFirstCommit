# local_server.py
from fastapi import FastAPI
from pydantic import BaseModel
from orchestrator import run_review

app = FastAPI()


class ReviewRequest(BaseModel):
    code: str


@app.post("/review")
def review(req: ReviewRequest):
    return run_review(req.code)


@app.get("/")
def health():
    return {"status": "ok", "message": "Code Review Swarm is running"}