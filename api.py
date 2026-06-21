from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil

from src.rag_engine import ask_rfp
from src.ai_analyzer import (
    analyze_rfp,
    requirement_intelligence,
    bid_readiness_assessment,
    go_no_go_recommendation,
)

app = FastAPI(title="RFP Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "RFP Intelligence API is running",
        "status": "ok"
    }


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": file_path,
        "note": "Run ingest.py to update FAISS index."
    }


@app.post("/chat")
def chat(payload: dict):
    question = payload.get("question")

    if not question:
        return {"error": "Question is required"}

    return ask_rfp(question)


@app.get("/analyze")
def analyze():
    return analyze_rfp()

@app.get("/requirements")
def requirements():
    return requirement_intelligence()

@app.get("/assessment")
def assessment():
    return bid_readiness_assessment()

@app.get("/decision")
def decision():
    return go_no_go_recommendation()