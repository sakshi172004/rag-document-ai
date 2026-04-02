import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="IntelliDoc AI", layout="wide")

API_URL = "https://rag-backend.onrender.com/query"
UPLOAD_URL = "https://rag-backend.onrender.com/upload"

# ---------------- CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0f172a;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #020617;
}

.chat-user {
    background-color: #1e293b;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.chat-bot {
    background-color: #020617;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 15px;
    border-left: 4px solid #6366f1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "chats" not in st.session_state:
    st.session_state.chats = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📂 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process Documents"):
        if uploaded_files:
            files = [("files", (file.name, file.getvalue())) for file in uploaded_files]
            requests.post(UPLOAD_URL, files=files)

            # create new chat session (per PDF)
            st.session_state.chats.append({
                "title": uploaded_files[0].name,
                "messages": []
            })

            st.session_state.current_chat = len(st.session_state.chats) - 1
            st.success("Documents processed!")

    st.divider()

    st.title("💬 Chats")

    for i, chat in enumerate(st.session_state.chats):
        col1, col2 = st.columns([4,1])

        with col1:
            if st.button(chat["title"][:20], key=f"chat_{i}"):
                st.session_state.current_chat = i

        with col2:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.chats.pop(i)
                st.rerun()

# ---------------- MAIN ----------------
st.title("🤖 IntelliDoc AI")

# show full chat thread
if st.session_state.current_chat is not None:
    chat = st.session_state.chats[st.session_state.current_chat]

    for msg in chat["messages"]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ---------------- INPUT ----------------
query = st.chat_input("Ask something...")

if query and st.session_state.current_chat is not None:
    try:
        res = requests.post(API_URL, json={"query": query})
        data = res.json()

        # safe extraction
        answer = data.get("answer") or data.get("response") or str(data)

        chat = st.session_state.chats[st.session_state.current_chat]

        chat["messages"].append({"role": "user", "content": query})
        chat["messages"].append({"role": "bot", "content": answer})

        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")
