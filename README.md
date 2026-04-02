# 🧠 IntelliDoc AI: Your Personal Document Chat Assistant

IntelliDoc AI is a full-stack, containerized Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF documents. It features a sophisticated backend built with FastAPI and a beautiful, intuitive frontend powered by Streamlit. The entire system is orchestrated with Docker for seamless local and cloud deployment.

## 🚀 Live Demo

You can try the live, deployed version of this application here:

[**➡️ IntelliDoc AI - Live App**](https://sakshi172004-rag-document-ai-frontend-kdoqlv.streamlit.app/)


## ✨ Features

- **Interactive Chat UI:** A clean, modern, and user-friendly interface inspired by leading AI chatbots.
- **Multi-Document Support:** Upload and process multiple PDF documents at once.
- **Advanced RAG Pipeline:** Utilizes a powerful sentence-transformer for embeddings and FAISS for efficient vector storage and retrieval.
- **Powered by Google Gemini:** Leverages the `gemini-1.5-flash` model for fast and accurate answer generation.
- **Persistent Chat History:** Conversations are saved in the session, with options to start a new chat or delete old ones.
- **View Document Metadata:** Users can view a list of all documents processed by the system and their upload timestamps.
- **Fully Containerized:** The entire application (backend + frontend) is managed by Docker Compose for easy, one-command setup.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** FastAPI
- **LLM:** Google Gemini (`gemini-1.5-flash-latest`)
- **Core Logic:** LangChain
- **Vector Database:** FAISS (CPU)
- **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Deployment:** Docker, Streamlit Community Cloud

## ⚙️ Running Locally

### Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- [Git](https://git-scm.com/)
- A **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Setup Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/sakshi172004/rag-document-ai.git
    cd rag-document-ai
    ```

2.  **Set Up Environment Variables:**
    Create a `.env` file by copying the example and add your API key.
    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and paste your key:
    ```
    GOOGLE_API_KEY="YourGoogleApiKeyHere"
    ```

3.  **Build and Run with Docker Compose:**
    This single command builds and starts both the backend API and the frontend UI.
    ```bash
    docker compose up --build
    ```

4.  **Access the Application:**
    Your professional chat application is now running! Open your browser and go to:
    **`http://localhost:8501`**

## 📂 Project Structure

```rag-app/
├── app/
│   ├── db.py             # Metadata DB logic (SQLite)
│   ├── pipeline.py       # Core RAG logic (FAISS, LangChain, Gemini)
│   └── ...
├── deploy_app.py         # All-in-one app for Streamlit Cloud deployment
├── frontend.py           # Streamlit UI for local Docker setup
├── .env.example          # Environment variable template
├── Dockerfile            # Instructions to build the application container
├── docker-compose.yml    # Orchestrates the backend and frontend services
├── requirements.txt      # Python dependencies
└── README.md             # You are here!
