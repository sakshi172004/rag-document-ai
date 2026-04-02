from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# ---------------- PATH ----------------
DB_PATH = "vectorstore"

# ---------------- LLM (Groq) ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------- PROCESS ----------------
def process_and_store_docs(file_paths):
    documents = []

    for path in file_paths:
        loader = PyPDFLoader(path)
        documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    # ❌ NO embeddings → simple storage (temporary fix)
    texts = [doc.page_content for doc in chunks]

    os.makedirs(DB_PATH, exist_ok=True)

    with open(os.path.join(DB_PATH, "data.txt"), "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t + "\n\n")

# ---------------- LOAD ----------------
def get_docs():
    file_path = os.path.join(DB_PATH, "data.txt")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------- QUERY ----------------
def query_rag(query: str):
    data = get_docs()

    if data is None:
        return {
            "answer": "No documents processed yet",
            "source_chunks": []
        }

    # simple retrieval (top part only)
    context = data

    prompt = f"""
Answer the question using ONLY the context.

Context:
{context}

Question:
{query}

Explain in detail with proper points.
If steps exist, list them clearly.
Do not say "not in context" unless absolutely missing.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "source_chunks": [context[:500]]
    }
