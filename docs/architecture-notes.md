# SmartDocs Architect - Architecture Notes


## Problem
Users often have multiple documents but no efficient semantic search and grounded question-answering system.


## Solution
A cloud-hosted document intelligence system that uses Retrieval-Augmented Generation (RAG).


## Architecture Layers

### 1. Presentation Layer
- Streamlit web UI
- File upload interface
- Chat interaction interface

### 2. Processing Layer
- PDF, DOCX, TXT parsing
- Text cleaning and chunking

### 3. AI Layer
- Gemini embedding generation
- Gemini answer generation

### 4. Data Layer
- ChromaDB vector store
- Metadata storage for source tracking

### 5. Deployment Layer
- Streamlit Community Cloud


## Flow
1. User uploads files
2. Files are parsed
3. Text is chunked
4. Chunks are embedded
5. Embeddings are stored in ChromaDB
6. User asks a question
7. Query is embedded
8. Relevant chunks are retrieved
9. Gemini generates grounded response
10. Sources are shown to the user


## Security Considerations
- API key stored in environment variables
- No hardcoded credentials
- Local vector storage for simple prototype


## Limitations
- No authentication
- No multi-user separation
- No reranking layer
- Basic chunking strategy


## Future Improvements
- User login
- Cloud database
- Better chunking
- Reranking
- Role-based access
- Support for more file types
