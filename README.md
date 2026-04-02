# 🧠 IntelliDoc AI: Your Personal Document Chat Assistant

IntelliDoc AI is a full-stack, containerized Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF documents. It features a sophisticated backend built with FastAPI and a beautiful, intuitive frontend powered by Streamlit. The entire system is orchestrated with Docker for seamless local and cloud deployment.

## 🚀 Live Demo

You can try the live, deployed version of this application here:

[**➡️ IntelliDoc AI - Live App**](https://sakshi172004-rag-document-ai-frontend-kdoqlv.streamlit.app/)


# 🧠 IntelliDoc AI: Document Chat Assistant

IntelliDoc AI is a full-stack AI application that allows users to upload PDF documents and ask questions from them through a chat interface.

---

## 🚀 Live Demo
👉 https://your-app.streamlit.app  

---

## ✨ Features
- 💬 Chat with PDF documents  
- 📄 Upload multiple files  
- ⚡ Fast AI responses using Groq  
- 🧠 Context-based answers  
- ☁️ Cloud-friendly and lightweight  

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **LLM:** Groq (LLaMA 3.1)  
- **Core Logic:** LangChain  
- **Storage:** File-based (data.txt)  

---

## 🧠 How It Works
1. Upload PDF  
2. Extract and split text into chunks  
3. Store chunks in a file  
4. Retrieve relevant content  
5. Generate answer using AI  

---

## 📂 Project Structure

```
rag-document-ai/
│
├── app/
│   ├── main.py
│   ├── pipeline.py
│   ├── db.py
│   ├── models.py
│   └── __init__.py
│
├── frontend.py
├── deploy_app.py
├── data/
│   └── data.txt
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

