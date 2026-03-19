# SmartDocs Architect - Architecture Notes


## Problem
Users need a cloud-based way to search document content semantically and receive grounded answers beyond traditional keyword search.


## Solution
SmartDocs Architect is an AWS-hosted Retrieval-Augmented Generation (RAG) document intelligence system.


## Implemented MVP Architecture

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


## Architecture Layers

### Presentation Layer
- Streamlit UI
- File upload
- Question interface

### Processing Layer
- PDF and TXT parsing
- Text chunking

### AI Layer
- Gemini embeddings
- Semantic retrieval
- Grounded answer generation

### Data Layer
- ChromaDB vector storage

### Infrastructure Layer
- AWS EC2
- Ubuntu server
- Security Group rules


## AWS Networking
- Port 22 for SSH
- Port 8501 for Streamlit


## Architectural Decisions
- EC2 for infrastructure control
- ChromaDB local for MVP simplicity
- Streamlit for rapid delivery


## Future Architecture
- Elastic IP
- Load Balancer
- Auto Scaling Group
- Amazon S3
