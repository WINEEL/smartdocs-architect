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

# ----------------------------
# Session state
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0

if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = []

if "last_retrieved_count" not in st.session_state:
    st.session_state.last_retrieved_count = 0


# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.header("Document Management")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.subheader("Uploaded Documents")
        for file in uploaded_files:
            st.write(f"- {file.name}")
    elif st.session_state.uploaded_file_names:
        st.subheader("Last Processed Documents")
        for file_name in st.session_state.uploaded_file_names:
            st.write(f"- {file_name}")

    if st.button("Process Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            total_chunks = 0
            file_names = []
            failed_files = []

            for uploaded_file in uploaded_files:
                tmp_path = None
                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=f"_{uploaded_file.name}"
                    ) as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name

                    count = ingest_file(tmp_path, uploaded_file.name)
                    total_chunks += count
                    file_names.append(uploaded_file.name)

                except Exception as e:
                    failed_files.append((uploaded_file.name, str(e)))

                finally:
                    if tmp_path and os.path.exists(tmp_path):
                        os.remove(tmp_path)

            st.session_state.total_chunks = total_chunks
            st.session_state.uploaded_file_names = file_names
            st.session_state.last_retrieved_count = 0

            if file_names:
                st.success(f"Processing complete. Indexed {total_chunks} chunks.")

            if failed_files:
                for failed_name, error_text in failed_files:
                    st.error(f"Failed to process {failed_name}: {error_text}")

            st.rerun()

    if st.button("Clear Knowledge Base"):
        clear_collection()
        st.session_state.messages = []
        st.session_state.total_chunks = 0
        st.session_state.uploaded_file_names = []
        st.session_state.last_retrieved_count = 0
        st.success("Knowledge base cleared.")
        st.rerun()


# ----------------------------
# Main page
# ----------------------------
st.title("📚 SmartDocs Architect")
st.caption("Cloud-Hosted AI-Powered Document Intelligence System")

st.markdown("""
This application allows users to upload PDF and TXT documents,
convert them into embeddings, store them in a vector database,
and ask grounded questions based on the uploaded content.
""")

st.markdown("""
### Example Questions
- Summarize the uploaded document
- What are the main concepts discussed?
- Explain the key points in this file
""")

col1, col2, col3 = st.columns(3)
col1.metric("Files Uploaded", len(st.session_state.uploaded_file_names))
col2.metric("Indexed Chunks", st.session_state.total_chunks)
col3.metric("Retrieved Chunks", st.session_state.last_retrieved_count)

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
            try:
                answer, sources = answer_question(query)
                st.session_state.last_retrieved_count = len(sources)

                st.markdown(answer)

                if sources:
                    source_files = sorted(
                        {meta.get("source", "Unknown") for _, meta in sources}
                    )

                    st.markdown("### Sources Used")
                    for source_file in source_files:
                        st.write(f"- {source_file}")

                    with st.expander("Retrieved Source Chunks"):
                        for i, (doc, meta) in enumerate(sources, start=1):
                            source_name = meta.get("source", "Unknown")
                            chunk_index = meta.get("chunk_index", -1)

                            st.markdown(
                                f"**Source {i}:** `{source_name}` | chunk `{chunk_index}`"
                            )
                            st.write(doc[:1200] + ("..." if len(doc) > 1200 else ""))

            except Exception as e:
                answer = f"Error while generating answer: {e}"
                st.error(answer)
                st.session_state.last_retrieved_count = 0

    st.session_state.messages.append(("assistant", answer))
    st.rerun()
