# SmartDocs Architect
> Cloud-Hosted AI-Powered Document Intelligence System

## Overview
SmartDocs Architect is a cloud-hosted AI-powered document intelligence system built using Retrieval-Augmented Generation (RAG). It allows users to upload documents, process them into vector embeddings, retrieve relevant context, and ask grounded questions based only on the uploaded content.


## Features
- Upload PDF, DOCX, and TXT files
- Extract and chunk document text
- Generate embeddings using Gemini
- Store vectors in ChromaDB
- Ask grounded questions through a chat interface
- Display retrieved source chunks for transparency
- Deployable on Streamlit Community Cloud


## Architecture
### Layers
1. Presentation Layer: Streamlit UI  
2. Processing Layer: Parsing and chunking  
3. AI Layer: Gemini embeddings and answer generation  
4. Data Layer: Vector storage using ChromaDB  
5. Deployment Layer: Cloud-hosted web app  


## Tech Stack
- Python  
- Streamlit  
- Gemini API  
- ChromaDB  
- PyPDF  
- python-docx  
- python-dotenv  


## Project Structure
```text
SmartDocs Architect/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── .env
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
├── data/
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


## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/wineel/smartdocs-architect.git
cd smartdocs-architect
```

### 2. Create and activate virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add environment variable
Create a `.env` file in the root folder:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the application
```bash
streamlit run app.py
```


## Deployment
This project is designed for deployment using Streamlit Community Cloud.

### Deployment Steps
1. Push project to GitHub  
2. Connect repository to Streamlit Cloud  
3. Set `app.py` as main entry file  
4. Add secret:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

5. Deploy  


## Demo Flow
- Upload a PDF, DOCX, or TXT document  
- Click **Process Documents**  
- Ask a question related to uploaded content  
- View grounded answer  
- Expand retrieved source chunks  


## Architecture Considerations
- Environment variables are used for API key protection  
- Local persistent vector store used for prototype simplicity  
- Clear separation between ingestion, retrieval, and UI layers  
- Designed for easy future extension  


## Limitations
- No user authentication  
- No multi-user document isolation  
- Basic chunking strategy  
- No reranking layer  


## Future Improvements
- User authentication  
- Cloud-native vector database  
- Better semantic reranking  
- Support for additional document formats  
- Multi-user workspace support  


## Author
Wineel Wilson Dasari


## License
Academic project for Solution Architecture coursework
