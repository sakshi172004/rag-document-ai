from dotenv import load_dotenv
load_dotenv()

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

# ---------------- PATH ----------------
DB_PATH = "vectorstore"

# ---------------- LLM ----------------
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
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

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

    return data.split("\n\n")


# ---------------- QUERY ----------------
def query_rag(query: str):
    try:
        chunks = get_docs()

        if not chunks:
            return {
                "answer": "No documents processed yet.",
                "source_chunks": []
            }

        # 🔥 REMOVE USELESS WORDS
        stopwords = {"what", "is", "the", "of", "in", "a", "an"}
        query_words = [w for w in query.lower().split() if w not in stopwords]

        scored_chunks = []

        for chunk in chunks:
            chunk_lower = chunk.lower()

            score = 0

            for word in query_words:
                if word in chunk_lower:
                    score += 5   # 🔥 strong boost

            # 🔥 exact phrase boost
            if query.lower() in chunk_lower:
                score += 10

            scored_chunks.append((score, chunk))

        # sort
        scored_chunks.sort(reverse=True, key=lambda x: x[0])

        # 🔥 TAKE BEST
        top_chunks = [chunk for score, chunk in scored_chunks[:4]]

        # 🔥 fallback (IMPORTANT)
        if all(score == 0 for score, _ in scored_chunks[:4]):
            top_chunks = chunks[:4]

        context = "\n\n".join(top_chunks)
        context = context[:3000]

        # 🔥 CONTROLLED PROMPT
        prompt = f"""
Answer using the context below.

- Keep answer similar to notes
- Give clear explanation
- Do NOT give generic textbook answer
- Do NOT say "not in context"

Context:
{context}

Question:
{query}

Answer:
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "source_chunks": top_chunks
        }

    except Exception as e:
        return {
            "answer": f"Backend error: {str(e)}",
            "source_chunks": []
        }
