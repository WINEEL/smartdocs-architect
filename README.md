# SmartDocs Architect
> AWS-Hosted AI-Powered Document Intelligence System

## Overview
SmartDocs Architect is an AWS-hosted AI-powered document intelligence system built using Retrieval-Augmented Generation (RAG). It allows users to upload documents, process them into vector embeddings, retrieve relevant context, and ask grounded questions based only on uploaded content.

The current MVP is deployed on Amazon EC2 and designed as a cloud workload that can evolve into a scalable multi-instance architecture.

## Features
- Upload PDF and TXT files
- Extract and chunk document text
- Generate embeddings using Gemini API
- Store vectors in ChromaDB
- Ask grounded questions through a chat interface
- Display retrieved source chunks for transparency
- Clear knowledge base
- Deploy on AWS EC2

## Architecture

### MVP Architecture (Implemented)

```text
User
  ↓
Internet
  ↓
AWS EC2 Instance
  ↓
Streamlit Application
  ↓
Gemini API + Local ChromaDB
```

### Target Scalable Architecture (Proposed)

```text
User
  ↓
Application Load Balancer (ALB)
  ↓
Auto Scaling Group (EC2 Instances)
  ↓
Application Layer
  ↓
Amazon S3 for document storage
```

### Architectural Layers
1. Presentation Layer: Streamlit UI  
2. Processing Layer: Parsing and chunking  
3. AI Layer: Gemini embeddings and answer generation  
4. Data Layer: ChromaDB vector storage  
5. Infrastructure Layer: AWS EC2 within AWS networking  

## Tech Stack
- Python  
- Streamlit  
- Gemini API  
- ChromaDB  
- PyPDF  
- python-dotenv  
- AWS EC2  

## Project Structure

```text
SmartDocs Architect/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── app/
│   ├── __init__.py
│   ├── ingest.py
│   ├── rag.py
│   ├── parsers.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── docs/
│   ├── architecture-notes.md
│   └── demo-script.md
│
├── screenshots/
└── chroma_db/
```

## System Flow
1. User uploads one or more documents  
2. Documents are parsed into text  
3. Text is split into overlapping chunks  
4. Chunks are converted into embeddings  
5. Embeddings are stored in ChromaDB  
6. User submits a question  
7. Query is embedded  
8. Relevant chunks are retrieved  
9. Gemini generates a grounded answer  
10. Source chunks are displayed to the user  

## Local Run

### Clone repository

```bash
git clone https://github.com/WINEEL/smartdocs-architect.git
cd smartdocs-architect
```

### Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add environment variable

```env
GEMINI_API_KEY=your_api_key_here
```

### Run locally

```bash
streamlit run app.py
```

## AWS Deployment

### EC2 Deployment Steps
1. Launch Ubuntu EC2 instance  
2. Configure Security Group:
   - SSH (22) from My IP  
   - Custom TCP (8501) from Anywhere  
3. SSH into EC2  
4. Clone repository  
5. Install dependencies  
6. Add `.env` file  
7. Run:

```bash
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Public Access

```text
http://<EC2-Public-IP>:8501
```

## Architecture Considerations
- API keys protected through environment variables  
- Single-instance MVP for rapid delivery  
- Security Group controls external access  
- Clear separation between ingestion, retrieval, AI, and UI layers  
- Scalable target architecture aligned with AWS best practices  

## Limitations
- Single EC2 instance  
- Local vector persistence  
- No user authentication  
- No multi-user isolation  
- Basic chunking strategy  

## Future Improvements
- Elastic IP  
- Application Load Balancer  
- Auto Scaling Group  
- Amazon S3 document storage  
- Managed vector database  
- User authentication  

## Author
Wineel Wilson Dasari

## License
Academic project for Solution Architecture coursework
