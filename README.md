# My RAG App

A simple API to upload PDF documents and ask questions about them. Built with FastAPI and powered by Google Gemini.

## How it Works

1.  You upload PDF files.
2.  The app splits them into smaller pieces (chunks).
3.  It stores these chunks in a local vector database (ChromaDB).
4.  When you ask a question, the app finds the most relevant chunks and sends them to Google Gemini along with your question.
5.  Gemini generates an answer based on the information provided.

## How to Run This

### Prerequisites
*   You need [Docker](https://www.docker.com/get-started) installed.
*   You need a Google Gemini API Key.

### Setup Steps

1.  **Clone this project:**
    ```bash
    git clone <your-repo-url>
    cd rag-app
    ```

2.  **Create your `.env` file:**
    Copy the example file and add your key.
    ```bash
    cp .env.example .env
    ```
    Now open `.env` and paste your key.

3.  **Run with Docker Compose:**
    This command does everything: builds the app image and starts it.
    ```bash
    docker-compose up --build
    ```

    Your app is now running at `http://localhost:8000`.

## Using the API

The easiest way to use the API is with the auto-generated docs.

*   **Go to:** `http://localhost:8000/docs`

From there you can test all the endpoints:
- `POST /upload`: To upload your PDFs.
- `POST /query`: To ask a question.
- `GET /documents`: To see what you've uploaded.

## Running Tests

To make sure everything is working, you can run the tests. Make sure the app is running first.

```bash
docker-compose exec rag-api pytest
```