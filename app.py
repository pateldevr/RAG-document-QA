import streamlit as st
import tempfile
import os
import chromadb
from dotenv import load_dotenv

from indexing.pdf_extractor import extract_text
from indexing.chunker import chunking
from indexing.embedder import embedding
from vector_store.chroma_client import initialize, store
from query.retriever import retrieving
from query.generator import response_drafting

load_dotenv()

COLLECTION_NAME = "my_collection"


def init_session():
    if "has_documents" not in st.session_state:
        collection = initialize(COLLECTION_NAME)
        st.session_state.has_documents = collection.count() > 0
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_reset_warning" not in st.session_state:
        st.session_state.show_reset_warning = False


def run_indexing(tmp_path: str):
    text = extract_text(tmp_path)
    chunks = chunking(text)
    vectors = embedding(chunks)
    collection = initialize(COLLECTION_NAME)
    store(collection, chunks, vectors)


def get_response(query: str) -> str:
    chunks = retrieving(query, COLLECTION_NAME)
    return response_drafting(query, chunks)


def reset_collection():
    client = chromadb.PersistentClient()
    client.delete_collection(COLLECTION_NAME)
    st.session_state.has_documents = False
    st.session_state.messages = []
    st.session_state.show_reset_warning = False


def show_upload_section():
    st.subheader("No documents indexed yet")
    st.write("Upload a PDF to start chatting.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file and st.button("Index Document"):
        with st.spinner("Processing PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            try:
                run_indexing(tmp_path)
            finally:
                os.unlink(tmp_path)

        st.session_state.has_documents = True
        st.success("Document indexed!")
        st.rerun()


def show_chat_section():
    with st.sidebar:
        st.header("Document Controls")
        if st.button("Upload New PDF"):
            st.session_state.show_reset_warning = True

    if st.session_state.show_reset_warning:
        st.warning(
            "Uploading a new PDF will delete all indexed documents and chat history. "
            "This cannot be undone."
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, reset and upload new"):
                reset_collection()
                st.rerun()
        with col2:
            if st.button("Cancel"):
                st.session_state.show_reset_warning = False
                st.rerun()
        return

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if query := st.chat_input("Ask a question about your document..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(query)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    st.title("RAG Document QA")
    init_session()
    if st.session_state.has_documents:
        show_chat_section()
    else:
        show_upload_section()


if __name__ == "__main__":
    main()
