from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

    # store chunks properly
    texts = [doc.page_content for doc in chunks]

    os.makedirs(DB_PATH, exist_ok=True)

    with open(os.path.join(DB_PATH, "data.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(texts))

    print("TOTAL CHUNKS:", len(texts))


# ---------------- LOAD ----------------
def get_docs():
    file_path = os.path.join(DB_PATH, "data.txt")

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    # split back into chunks
    return data.split("\n\n")


# ---------------- QUERY ----------------
def query_rag(query: str):
    chunks = get_docs()

    if not chunks:
        return {
            "answer": "No documents processed yet",
            "source_chunks": []
        }

    # 🔥 SMART RETRIEVAL (keyword based)
    query_words = query.lower().split()

    scored_chunks = []
    for chunk in chunks:
        score = sum(word in chunk.lower() for word in query_words)
        scored_chunks.append((score, chunk))

    # sort by relevance
    scored_chunks.sort(reverse=True, key=lambda x: x[0])

    # take top relevant chunks only
    top_chunks = [chunk for score, chunk in scored_chunks[:5]]

    context = "\n\n".join(top_chunks)

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}

Give a detailed answer with:
- Proper explanation
- Bullet points if needed
- Steps if applicable

Answer like for exams.
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "source_chunks": top_chunks
    }
