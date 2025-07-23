# app/models.py
from pydantic import BaseModel
from typing import List

# What the user sends when they ask a question
class QueryRequest(BaseModel):
    query: str

# What we send back
class QueryResponse(BaseModel):
    answer: str
    source_chunks: List[str]

# How we show document info
class DocumentMetadata(BaseModel):
    id: int
    filename: str
    uploaded_at: str