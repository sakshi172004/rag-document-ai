# app/pipeline.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# Path setup
CHROMA_DB_PATH = os.path.join("data", "chroma_db")
UPLOAD_PATH = os.path.join("data", "uploads")

# Use a free, local embedding model
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Setup the vector store
vectorstore = Chroma(
    persist_directory=CHROMA_DB_PATH, 
    embedding_function=embedding_function
)

# Setup the LLM. Langchain will grab the API key from the .env file
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",  # <-- YEH WALA NAAM HONA CHAHIYE
    temperature=0.3,
    convert_system_message_to_human=True 
)

def process_and_store_docs(file_paths: list[str]):
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(documents)
        
        # Create unique IDs for each chunk to avoid duplicates
        chunk_ids = [f"{os.path.basename(file_path)}_{i}" for i in range(len(chunks))]
        vectorstore.add_documents(documents=chunks, ids=chunk_ids)
        print(f"-> Processed {os.path.basename(file_path)}, added {len(chunks)} chunks.")

    # Save to disk
    vectorstore.persist()

def get_rag_chain():
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4}) # Get top 4 results

    # This is the prompt we send to Gemini
    template = """
    Answer the question based only on the following context.
    If the answer is not in the context, say "I don't have that information".

    Context:
    {context}

    Question: {question}
    """
    prompt = PromptTemplate.from_template(template)

    # This is where the LangChain magic happens
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

def query_rag(query: str):
    rag_chain = get_rag_chain()
    answer = rag_chain.invoke(query)
    
    # We can also get the source documents for debugging or display
    retriever = vectorstore.as_retriever(search_kwargs={'k': 4})
    source_docs = retriever.invoke(query)
    source_chunks = [doc.page_content for doc in source_docs]
    
    return {"answer": answer, "source_chunks": source_chunks}