# app/pipeline.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# --- YEH HAIN NAYE IMPORTS ---
from langchain_community.vectorstores import FAISS
# -----------------------------
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Constants
FAISS_DB_PATH = os.path.join("data", "faiss_db") # Changed from CHROMA_DB_PATH
UPLOAD_PATH = os.path.join("data", "uploads")

embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.3, 
    convert_system_message_to_human=True
)

def process_and_store_docs(file_paths: list[str]):
    """Loads, chunks, and stores documents in the FAISS vector database."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    
    all_chunks = []
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        chunks = text_splitter.split_documents(documents)
        all_chunks.extend(chunks)
        print(f"-> Processed {os.path.basename(file_path)}, created {len(chunks)} chunks.")

    if not all_chunks:
        return

    # --- NAYA, FAISS WALA LOGIC ---
    if os.path.exists(FAISS_DB_PATH):
        # If DB exists, load it and add new documents
        vectorstore = FAISS.load_local(FAISS_DB_PATH, embedding_function, allow_dangerous_deserialization=True)
        vectorstore.add_documents(documents=all_chunks)
        print("Added new chunks to existing FAISS DB.")
    else:
        # If DB doesn't exist, create a new one
        vectorstore = FAISS.from_documents(documents=all_chunks, embedding=embedding_function)
        print("Created new FAISS DB.")

    vectorstore.save_local(FAISS_DB_PATH)
    print("FAISS DB saved to disk.")
    
def query_rag(query: str):
    """Queries the RAG system and returns the answer and source chunks."""
    if not os.path.exists(FAISS_DB_PATH):
        return {"answer": "No documents have been processed yet. Please upload a document first.", "source_chunks": []}

    vectorstore = FAISS.load_local(FAISS_DB_PATH, embedding_function, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})
    
    template = """
    Answer the question based only on the following context.
    If the answer is not in the context, say "I don't have that information".

    Context:
    {context}

    Question: {question}
    """
    prompt = PromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    answer = rag_chain.invoke(query)
    source_docs = retriever.invoke(query)
    source_chunks = [doc.page_content for doc in source_docs]
    
    return {"answer": answer, "source_chunks": source_chunks}