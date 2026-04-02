# 🧠 IntelliDoc AI: Your Personal Document Chat Assistant

IntelliDoc AI is a full-stack, containerized Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF documents. It features a sophisticated backend built with FastAPI and a beautiful, intuitive frontend powered by Streamlit. The entire system is orchestrated with Docker for seamless local and cloud deployment.

## 🚀 Live Demo

You can try the live, deployed version of this application here:

[**➡️ IntelliDoc AI - Live App**](https://sakshi172004-rag-document-ai-frontend-kdoqlv.streamlit.app/)


✨ Features
Interactive Chat UI (Streamlit-based clean interface)
Multi-PDF Upload Support
Custom RAG Pipeline (no heavy dependencies)
Smart Chunking with structure preservation
Keyword-based Retrieval with scoring
Neighbor Chunk Retrieval (avoids missing info)
Context-aware Answer Generation
Session-based Chat History
Lightweight & Cloud-friendly (works on free tier)
🛠️ Tech Stack
Frontend: Streamlit
Backend: FastAPI
LLM: Groq (llama-3.1-8b-instant)
Core Logic: LangChain
Document Loader: PyPDFLoader
Text Splitting: RecursiveCharacterTextSplitter
Retrieval: Custom keyword-based retrieval
Storage: File-based (data.txt)
Deployment: Render (backend) + Streamlit Cloud (frontend)
🔄 How It Works (Workflow)
User uploads PDF
Backend extracts text using PyPDFLoader
Text is split into chunks (smart chunking)
Chunks are stored in a file (data.txt)
User asks a question
System retrieves relevant chunks using keyword scoring
Neighbor chunks are also selected to avoid missing context
Context is sent to Groq LLM
LLM generates final answer
Answer displayed in chat UI
⚙️ Running Locally
Prerequisites
Python 3.9+
Git
Groq API Key
Setup Steps
Clone the repo:
git clone https://github.com/sakshi172004/rag-document-ai.git
cd rag-document-ai
Create .env file:
GROQ_API_KEY="your_groq_api_key"
Install dependencies:
pip install -r requirements.txt
Run backend:
uvicorn app.main:app --reload
Run frontend:
streamlit run frontend.py
Open:
http://localhost:8501


## 📂 Project Structure

```rag-app/
├── app/
│   ├── pipeline.py       # Core RAG logic (chunking + retrieval + Groq)
│   └── ...
├── deploy_app.py         # All-in-one app for Streamlit Cloud deployment
├── frontend.py           # Streamlit UI for local Docker setup
├── .env.example          # Environment variable template
├── Dockerfile            # Instructions to build the application container
├── docker-compose.yml    # Orchestrates the backend and frontend services
├── requirements.txt      
└── README.md             # You are here!
