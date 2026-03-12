import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from app.ingest import ingest_file, clear_collection
from app.rag import answer_question

load_dotenv()

st.set_page_config(
    page_title="SmartDocs Architect",
    page_icon="📚",
    layout="wide"
)

st.title("📚 SmartDocs Architect")
st.caption("Cloud-Hosted AI-Powered Document Intelligence System")

st.markdown("""
This application allows users to upload PDF, DOCX, and TXT documents,
convert them into embeddings, store them in a vector database,
and ask grounded questions based on the uploaded content.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Document Management")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if st.button("Process Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            total_chunks = 0

            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=f"_{uploaded_file.name}"
                ) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                count = ingest_file(tmp_path, uploaded_file.name)
                total_chunks += count

                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            st.success(f"Processing complete. Indexed {total_chunks} chunks.")

    if st.button("Clear Knowledge Base"):
        clear_collection()
        st.session_state.messages = []
        st.success("Knowledge base cleared.")

st.subheader("Ask Questions")

if not st.session_state.messages:
    st.info("Upload and process documents first, then ask your questions here.")

for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

query = st.chat_input("Ask a question about your uploaded documents")

if query:
    st.session_state.messages.append(("user", query))

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Generating grounded answer..."):
            answer, sources = answer_question(query)
            st.markdown(answer)

            if sources:
                with st.expander("Retrieved Source Chunks"):
                    for i, (doc, meta) in enumerate(sources, start=1):
                        source_name = meta.get("source", "Unknown")
                        chunk_index = meta.get("chunk_index", -1)

                        st.markdown(
                            f"**Source {i}:** `{source_name}` | chunk `{chunk_index}`"
                        )
                        st.write(doc[:1200] + ("..." if len(doc) > 1200 else ""))

    st.session_state.messages.append(("assistant", answer))
