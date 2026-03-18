# SmartDocs Architect - Architecture Notes

## Problem
Users often work with multiple documents but lack an efficient system to semantically search content and obtain grounded answers based only on uploaded material.

Traditional keyword search is limited because it does not understand semantic meaning or contextual relevance.

## Solution
SmartDocs Architect is an AWS-hosted document intelligence system built using Retrieval-Augmented Generation (RAG).

The system allows users to:
- Upload documents
- Convert text into embeddings
- Store vectors
- Retrieve semantically relevant chunks
- Generate grounded answers using AI

## Implemented Architecture (MVP)

```text
User
  ↓
Internet
  ↓
AWS EC2 Instance
  ↓
Streamlit Application
  ↓
Gemini API + ChromaDB
```

## Target Scalable Architecture

```text
User
  ↓
Application Load Balancer
  ↓
Auto Scaling Group
  ↓
Multiple EC2 Instances
  ↓
Shared Storage / Amazon S3
```

## Architecture Layers

## 1. Presentation Layer
- Streamlit web UI
- File upload interface
- Question-answer chat interface
- Source chunk display for transparency

## 2. Processing Layer
- PDF and TXT parsing
- Text cleaning
- Chunking with overlap

## 3. AI Layer
- Gemini embedding generation
- Semantic retrieval
- Gemini grounded answer generation

## 4. Data Layer
- ChromaDB vector store
- Metadata storage for source tracking

## 5. Infrastructure Layer
- Amazon EC2 hosting
- Ubuntu server runtime
- Python virtual environment
- Security Group controlled network access

## System Flow

1. User uploads files  
2. Files are parsed  
3. Text is chunked  
4. Chunks are embedded  
5. Embeddings are stored in ChromaDB  
6. User submits a question  
7. Query is embedded  
8. Relevant chunks are retrieved  
9. Gemini generates grounded response  
10. Sources are displayed  

## AWS Networking Used

## Security Group Rules
- SSH on port 22 for server access
- TCP port 8501 for Streamlit application access

## Public Access
Application exposed using:

```text
http://EC2_PUBLIC_IP:8501
```

## Security Considerations
- API key stored in `.env`
- No hardcoded credentials
- Security Group restricts access
- Single-instance prototype for controlled deployment

## Architectural Decisions
- EC2 selected for infrastructure control
- ChromaDB kept local for MVP simplicity
- Streamlit selected for fast UI delivery
- Modular separation between ingestion, retrieval, and UI

## Limitations
- Single EC2 instance
- Local vector persistence
- No authentication
- No multi-user separation
- Basic chunking strategy

## Future Improvements
- Elastic IP for stable endpoint
- Application Load Balancer
- Auto Scaling Group
- Amazon S3 document storage
- Managed vector database
- Authentication layer
- Role-based access
- Better reranking pipeline
