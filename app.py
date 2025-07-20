import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS  # ✅ updated
from langchain_community.embeddings import HuggingFaceEmbeddings  # ✅ updated
from langchain.text_splitter import RecursiveCharacterTextSplitter  # ✅ stays the same
from langchain_community.document_loaders import PyPDFLoader  # ✅ updated
from langchain.docstore.document import Document  # ✅ stays the same
import tempfile
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
project_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="NeuroRecursion", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")
# Model options and sidebar dropdown
MODEL_OPTIONS = {
    "LLaMA 3 (70B, 8K context)": "llama3-70b-8192",
    "Gemma 7B (Instruction-tuned)": "gemma-7b-it",
    "LLaMA 2 (70B, 4K context)": "llama2-70b-4096"
}

st.sidebar.title("🔧 Model Settings")
selected_model_name = st.sidebar.selectbox("Choose a model", list(MODEL_OPTIONS.keys()))
selected_model = MODEL_OPTIONS[selected_model_name]

st.markdown(f"**Using model:** `{selected_model_name}`")



load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


st.markdown(
    """
    <style>
        .main {
            background-color: #1e1e2f;
            color: #f4f4f4;
        }
        .stTextInput>div>div>input {
            background-color: #2e2e3e;
            color: white;
        }
        .stButton>button {
            background-color: #4a4a6a;
            color: white;
        }
        .stChatMessage {
            background-color: #333;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True
)

st.title("🧠 NeuroRecursion: Your friend who remembers everything!")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def reformat_input(user_input):
    return {"role": "user", "content": user_input}
vectordb = None  # Global vector DB object

def get_contextual_docs(query):
    if "vectordb" in st.session_state and st.session_state.vectordb:
        similar_docs = st.session_state.vectordb.similarity_search(query, k=3)
        return "\n\n".join([doc.page_content for doc in similar_docs])
    else:
        return ""

def get_gpt_response(message_list):
    last_user_msg = ""
    for msg in reversed(message_list):
        if msg["role"] == "user":
            last_user_msg = msg["content"]
            break

    context = get_contextual_docs(last_user_msg)
    if context:
        message_list = message_list[:-1]  # Remove original user message
        message_list.append({"role": "user", "content": f"Context: {context}\n\nQuestion: {last_user_msg}"})

    response = client.chat.completions.create(
        model=selected_model,
        messages=message_list,
        temperature=0.7,
        max_tokens=1024,
    )

    return response.choices[0].message.content


st.sidebar.title("Settings")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
# ========== RAG: PDF Upload, Vector Store, Retrieval ==========
st.sidebar.markdown("### 📄 Upload Knowledge Base (PDF)")
uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type="pdf")

vectordb = None  # Default

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name

    loader = PyPDFLoader(pdf_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(pages)
    vectordb = FAISS.from_documents(docs, embeddings)
    st.session_state.vectordb = vectordb
    st.sidebar.success("✅ Knowledge base processed!")



user_input = st.chat_input("Type anything...")
if user_input:
    formatted = reformat_input(user_input)
    st.session_state.messages.append(formatted)
    with st.chat_message("user"):
        st.markdown(user_input)
    reply = get_gpt_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Optional: Save chat history
if st.sidebar.button("💾 Save Chat"):
    history_path = os.path.join(project_dir, "chat_history.txt")
    with open(history_path, "w", encoding="utf-8") as f:
        for msg in st.session_state.messages:
            role = msg["role"]
            content = msg["content"]
            f.write(f"{role.upper()}: {content}\n\n")
    st.sidebar.success("Chat saved to chat_history.txt")