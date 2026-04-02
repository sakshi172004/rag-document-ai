from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from app.pipeline import process_and_store_docs, query_rag

app = FastAPI()

# ✅ CORS (IMPORTANT for Streamlit → Render communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Upload folder
UPLOAD_PATH = "data"
os.makedirs(UPLOAD_PATH, exist_ok=True)


# ---------------- HEALTH CHECK (IMPORTANT) ----------------
@app.get("/")
def home():
    return {"message": "API is running 🚀"}


# ---------------- UPLOAD ----------------
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    file_paths = []

    for file in files:
        path = os.path.join(UPLOAD_PATH, file.filename)

        with open(path, "wb") as f:
            f.write(await file.read())

        file_paths.append(path)

    process_and_store_docs(file_paths)

    return {"message": "Documents processed successfully"}


# ---------------- QUERY ----------------
@app.post("/query")
async def query(data: dict):
    query_text = data.get("query", "")

    if not query_text:
        return {"answer": "Please provide a query"}

    result = query_rag(query_text)
    return result
