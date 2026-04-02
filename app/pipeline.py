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

    # 🔥 SMART CHUNKING (FIX)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=[
            "\n\n\n",
            "\n\n",
            "\n",
            ". "
        ]
    )

    chunks = splitter.split_documents(documents)

    texts = [doc.page_content for doc in chunks]

    os.makedirs(DB_PATH, exist_ok=True)

    with open(os.path.join(DB_PATH, "data.txt"), "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(texts))  # custom separator

    print("TOTAL CHUNKS:", len(texts))


# ---------------- LOAD ----------------
def get_docs():
    file_path = os.path.join(DB_PATH, "data.txt")

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    return data.split("\n\n---\n\n")


# ---------------- QUERY ----------------
def query_rag(query: str):
    try:
        chunks = get_docs()

        if not chunks:
            return {
                "answer": "No documents processed yet.",
                "source_chunks": []
            }

        # 🔥 remove useless words
        stopwords = {"what", "is", "the", "of", "in", "a", "an"}
        query_words = [w for w in query.lower().split() if w not in stopwords]

        scored_chunks = []

        for i, chunk in enumerate(chunks):
            chunk_lower = chunk.lower()
            score = 0

            for word in query_words:
                if word in chunk_lower:
                    score += 5

            if query.lower() in chunk_lower:
                score += 10

            scored_chunks.append((score, i, chunk))

        # sort best first
        scored_chunks.sort(reverse=True, key=lambda x: x[0])

        # 🔥 TAKE BEST + NEIGHBOURS (FIX)
        selected_chunks = []

        for score, idx, chunk in scored_chunks[:4]:   # increased from 2 → 4
            selected_chunks.append(chunk)

            if idx + 1 < len(chunks):
                selected_chunks.append(chunks[idx + 1])

            if idx - 1 >= 0:
                selected_chunks.append(chunks[idx - 1])

        # remove duplicates
        selected_chunks = list(dict.fromkeys(selected_chunks))

        # 🔥 increase context size (FIX)
        context = "\n\n".join(selected_chunks)
        context = context[:7000]

        # 🔥 FINAL PROMPT
        prompt = f"""
Answer STRICTLY using the context.

- Include ALL steps if present
- Do NOT skip any section
- Do NOT write "(No details provided)"
- Keep answer structured and exam-friendly

Context:
{context}

Question:
{query}

Answer:
"""

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "source_chunks": selected_chunks
        }

    except Exception as e:
        return {
            "answer": f"Backend error: {str(e)}",
            "source_chunks": []
        }
