# frontend.py
import streamlit as st
import requests
import time
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="IntelliDoc AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- API URL ---
API_URL = "http://127.0.0.1:8000" 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"], .st-emotion-cache-16txtl3 {
        font-family: 'Inter', sans-serif;
    }
    .stApp { background-color: #343541; }
    .main .block-container { max-width: 900px; padding-top: 2rem; }
    [data-testid="stSidebar"] { background-color: #202123; border-right: 1px solid #444654; }
    h1, h2, h3 { color: #FFFFFF; font-weight: 600; }
    .stButton>button { background-color: #444654; color: #FFFFFF; border-radius: 8px; border: 1px solid #565869; }
    .stButton>button:hover { background-color: #565869; border-color: #676879; }
    .stButton>button[kind="primary"] { background-color: #315EFB; border: none; }
    .stButton>button[kind="primary"]:hover { background-color: #1A42E6; }
    [data-testid="stChatInput"] { background-color: #40414F; border-top: 1px solid #565869; }
    [data-testid="stChatMessage"] { background-color: #444654; border-radius: 10px; }
    .welcome-container { text-align: center; padding-top: 5rem; }
    
    header[data-testid="stHeader"] { display: none !important; visibility: hidden !important; }
    html, body { overflow: hidden !important; }
    [data-testid="stSidebarContent"] { overflow: auto; }
</style>
""", unsafe_allow_html=True)

# --- Session State Management with History ---
def initialize_session():
    if "conversations" not in st.session_state or not st.session_state.conversations:
        st.session_state.conversations = {}
        chat_id = f"chat_{time.time()}"
        st.session_state.conversations[chat_id] = {
            "name": "New Conversation",
            "messages": [],
            "docs_are_processed": False # Master switch for UI
        }
        st.session_state.active_chat_id = chat_id
    elif "active_chat_id" not in st.session_state or st.session_state.active_chat_id not in st.session_state.conversations:
        st.session_state.active_chat_id = list(st.session_state.conversations.keys())[-1]

initialize_session()

# --- Helper Functions ---
def switch_chat(chat_id):
    st.session_state.active_chat_id = chat_id

def delete_chat(chat_id_to_delete):
    del st.session_state.conversations[chat_id_to_delete]
    if not st.session_state.conversations or st.session_state.active_chat_id == chat_id_to_delete:
        initialize_session()
    st.rerun()

def get_all_system_documents():
    try:
        response = requests.get(f"{API_URL}/documents")
        return response.json() if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        return None

# --- Sidebar ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 1.5rem; padding-bottom: 1rem;'>🧠 IntelliDoc AI</h1>", unsafe_allow_html=True)
    
    if st.button("➕ New Chat", use_container_width=True):
        chat_id = f"chat_{time.time()}"
        st.session_state.conversations[chat_id] = { "name": f"Chat #{len(st.session_state.conversations) + 1}", "messages": [], "docs_are_processed": False }
        switch_chat(chat_id); st.rerun()
        
    st.markdown("---")
    
    st.header("Upload Documents")
    active_chat = st.session_state.conversations.get(st.session_state.active_chat_id, {})

    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True, label_visibility="collapsed", key=f"uploader_{st.session_state.active_chat_id}")

    if uploaded_files:
        if st.button("Process Documents", use_container_width=True, type="primary"):
            with st.spinner("Analyzing documents..."):
                files_to_send = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                try:
                    response = requests.post(f"{API_URL}/upload", files=files_to_send)
                    if response.status_code == 200:
                        active_chat["docs_are_processed"] = True
                        active_chat["messages"] = [{"role": "assistant", "content": "Documents are ready! How can I help you?"}]
                        st.rerun()
                    else: st.error(f"Error: {response.text}")
                except requests.exceptions.RequestException: st.error("Connection Error.")
        st.info(f"{len(uploaded_files)} file(s) ready to process.")
        
    st.markdown("---")
    st.header("Chat History")
    for chat_id, chat_data in reversed(list(st.session_state.conversations.items())):
        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            if st.button(chat_data["name"], key=f"history_{chat_id}", use_container_width=True):
                switch_chat(chat_id); st.rerun()
        with col2:
            st.button("🗑️", key=f"delete_{chat_id}", on_click=delete_chat, args=(chat_id,), use_container_width=True)

    st.markdown("---")
    st.header("System Documents")
    all_docs = get_all_system_documents() 
    if all_docs is None:
        st.error("Could not connect to the backend.") # Yeh ab nahi dikhna chahiye
    elif not all_docs:
        st.info("No documents have been processed yet.")
    else: 
        for doc in all_docs:
            try:
                dt_object = datetime.fromisoformat(doc['uploaded_at'].replace('Z', '+00:00'))
                formatted_date = dt_object.strftime('%b %d, %Y - %I:%M %p')
                st.info(f"**File:** `{doc['filename']}`\n\n**Uploaded:** {formatted_date}")
            except (ValueError, KeyError):
                st.info(f"**File:** `{doc.get('filename', 'N/A')}`")
        
# --- Main Interface ---
active_chat = st.session_state.conversations.get(st.session_state.active_chat_id)

if not active_chat or not active_chat.get("docs_are_processed"):
    st.markdown("""
    <div class="welcome-container">
        <div style="font-size: 4rem;">🧠</div>
        <div style="font-size: 2.5rem; font-weight: 600; margin-top: 1rem;">IntelliDoc AI</div>
        <div style="color: #B0B0B0; margin-top: 0.5rem;">Upload and process a document in the sidebar to begin the chat.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in active_chat["messages"]:
        with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about your documents..."):
        active_chat["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

      
        if active_chat["name"].startswith("Chat #") or active_chat["name"] == "New Conversation":
            active_chat["name"] = prompt[:30] + "..."
            

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{API_URL}/query", json={"query": prompt}) # <-- Ab yeh zaroor chalega
                    if response.status_code == 200:
                        answer = response.json().get("answer", "I couldn't find an answer.")
                        for chunk in answer.split():
                            full_response += chunk + " "; time.sleep(0.05)
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        active_chat["messages"].append({"role": "assistant", "content": full_response})
                    else:
                        error_detail = response.json().get('detail', 'Unknown error')
                        st.error(f"Error from backend: {error_detail}")
                except requests.exceptions.RequestException:
                    st.error("Failed to connect to the backend.")