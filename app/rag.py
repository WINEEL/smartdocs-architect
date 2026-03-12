import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


def get_query_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values


def retrieve_context(query: str, top_k: int = 4):
    query_embedding = get_query_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return list(zip(documents, metadatas))


def answer_question(query: str):
    retrieved = retrieve_context(query, top_k=4)

    if not retrieved:
        return "No relevant context found. Please upload and process documents first.", []

    context_blocks = []
    for doc, meta in retrieved:
        source = meta.get("source", "Unknown")
        chunk_index = meta.get("chunk_index", -1)
        context_blocks.append(
            f"[Source: {source} | Chunk: {chunk_index}]\n{doc}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a document intelligence assistant.

Answer ONLY from the retrieved context below.
Do not make up information.
If the answer is not present, say:
"I could not find that in the uploaded documents."

Retrieved Context:
{context}

User Question:
{query}

Return:
1. A clear answer
2. A short list of source files used
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text, retrieved
