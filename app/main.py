# app/main.py
from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List

from . import db, models, pipeline

# Check if the API key is there right at the start.
if not os.getenv("GOOGLE_API_KEY"):
    raise SystemExit("ERROR: GOOGLE_API_KEY is not set in the .env file.")

app = FastAPI(title="My RAG App")

@app.on_event("startup")
def startup_event():
    db.init_db()
    os.makedirs(pipeline.UPLOAD_PATH, exist_ok=True)

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Uploads one or more PDF files for processing."""
    if len(files) > 20:
        raise HTTPException(status_code=400, detail="Can't upload more than 20 files.")

    saved_files = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"{file.filename} is not a PDF.")
        
        file_path = os.path.join(pipeline.UPLOAD_PATH, file.filename)
        
        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        saved_files.append(file_path)
        db.add_document(file.filename)

    # Process them all at once
    pipeline.process_and_store_docs(saved_files)

    return {"message": f"Successfully uploaded and processed {len(saved_files)} files."}

@app.post("/query", response_model=models.QueryResponse)
def ask_question(request: models.QueryRequest):
    """Asks a question to the RAG system."""
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query can't be empty.")
    
    try:
        result = pipeline.query_rag(request.query)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong while querying.")

@app.get("/documents", response_model=List[models.DocumentMetadata])
def list_documents():
    """Lists all the documents that have been uploaded."""
    return db.get_all_documents()