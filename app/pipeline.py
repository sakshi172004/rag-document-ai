from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# ---------------- PATH ----------------
DB_PATH = "vectorstore"

# ---------------- EMBEDDINGS ----------------
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ---------------- LLM (WORKING 🔥) ----------------
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

    db = FAISS.from_documents(chunks, embedding_model)

    os.makedirs(DB_PATH, exist_ok=True)
    db.save_local(DB_PATH)

# ---------------- LOAD ----------------
def get_vectorstore():
    if not os.path.exists(DB_PATH):
        return None

    return FAISS.load_local(
        DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

# ---------------- QUERY ----------------
def query_rag(query: str):
    vs = get_vectorstore()

    if vs is None:
        return {
            "answer": "No documents processed yet",
            "source_chunks": []
        }

    retriever = vs.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question using ONLY the context.

Context:
{context}

Question:
{query}

Give short clean answer (2-3 lines).
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "source_chunks": [doc.page_content for doc in docs]
    }