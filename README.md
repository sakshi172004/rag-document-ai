# 🧠 IntelliDoc AI: Your Personal Document Chat Assistant

IntelliDoc AI is a full-stack, containerized Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF documents. It features a sophisticated backend built with FastAPI and a beautiful, intuitive frontend powered by Streamlit. The entire system is orchestrated with Docker for seamless local and cloud deployment.

## 🚀 Live Demo

You can try the live, deployed version of this application here:

[**➡️ IntelliDoc AI - Live App**](https://sakshi172004-rag-document-ai-frontend-kdoqlv.streamlit.app/)


✨ Features
💬 Interactive chat-based UI
📄 Upload and query multiple PDF documents
⚡ Lightweight RAG pipeline (no heavy dependencies)
🤖 Powered by Groq (LLaMA 3.1) for fast responses
🧠 Context-based answer generation (reduced hallucination)
💾 Session-based chat history
☁️ Fully cloud deployable (Streamlit + Render)


🛠️ Tech Stack
Frontend: Streamlit
Backend: FastAPI
LLM: Groq (LLaMA 3.1 8B Instant)
Core Logic: LangChain
Document Loader: PyPDFLoader
Text Splitting: RecursiveCharacterTextSplitter
Storage: File-based (data.txt)
Deployment: Streamlit Cloud + Render


🧠 How It Works (Workflow)
User uploads PDF
Backend extracts text using PyPDFLoader
Text is split into chunks (smart chunking)
Chunks are stored in a file (data.txt)
User asks a question
System retrieves relevant chunks (keyword-based)
Context + query sent to Groq LLM
LLM generates final answer
Answer displayed in chat UI


📂 Project Structure 
rag-document-ai/
│
├── app/
│   ├── main.py          # FastAPI backend (routes: /upload, /query)
│   ├── pipeline.py      # Core logic (PDF → chunking → retrieval → LLM)
│   ├── db.py            # Metadata handling
│   ├── models.py        # Request/response schemas
│   └── __init__.py
│
├── frontend.py          # Streamlit UI (chat + upload)
├── deploy_app.py        # Streamlit-only version (for cloud deployment)
│
├── data/                # Stored processed text (data.txt)
│
├── requirements.txt     # Dependencies
├── Dockerfile           # Container setup
├── docker-compose.yml   # Multi-service orchestration (frontend + backend)
│
├── .env.example         # Environment variables template
├── .gitignore
└── README.md
