import os
import uuid
import time
from dotenv import load_dotenv
from google import genai
import chromadb

from app.parsers import extract_text
from app.utils.helpers import chunk_text

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


def get_embedding(text: str, max_retries: int = 5, delay_seconds: float = 3.0):
    last_error = None

    for attempt in range(max_retries):
        try:
            response = client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )
            return response.embeddings[0].values

        except Exception as e:
            last_error = e
            error_text = str(e)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                if attempt < max_retries - 1:
                    sleep_time = delay_seconds * (attempt + 1)
                    time.sleep(sleep_time)
                    continue

            raise e

    raise last_error


def ingest_file(file_path: str, file_name: str):
    text = extract_text(file_path)
    chunks = chunk_text(text, chunk_size=600, overlap=100)

    if not chunks:
        return 0

    ids = []
    embeddings = []
    documents = []
    metadatas = []

    for idx, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        chunk_id = str(uuid.uuid4())

        ids.append(chunk_id)
        embeddings.append(embedding)
        documents.append(chunk)
        metadatas.append({
            "source": file_name,
            "chunk_index": idx
        })

        time.sleep(1.0)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )

    return len(chunks)


def clear_collection():
    global collection

    try:
        chroma_client.delete_collection("documents")
    except Exception:
        pass

    collection = chroma_client.get_or_create_collection(name="documents")
