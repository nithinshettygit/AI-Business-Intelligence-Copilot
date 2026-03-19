# 🧠 AI Business Intelligence Copilot

A conversational AI-powered business analytics platform that allows you to upload structured (CSV/Excel) and unstructured (PDF) data, ask natural language questions, and instantly receive dynamically generated charts and AI-driven insights.

## Features
- **Conversational Interface:** Ask questions like you would to ChatGPT.
- **Dynamic Charting:** Automatically generates Plotly charts (Bar, Line, Pie, Scatter) based on the data.
- **Structured Data Engine:** Uses Pandas & AI to generate deterministic Python code for accurate KPI calculations.
- **Unstructured Data Engine:** Uses a local HuggingFace embedding + FAISS vector store for local RAG on PDFs.
- **LangGraph Orchestrator:** Intelligently routes queries based on intent and available data files.

## Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **LLM Engine:** Groq (Llama3-70b-8192)
- **Orchestration:** LangGraph
- **Retrieval:** FAISS + PyMuPDF
- **Data:** Pandas + Plotly

## Quickstart

### Prerequisites
1. Python 3.9+
2. A Groq API Key

### Installation & Setup
1. Clone the repository.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/Scripts/activate # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up `.env` file:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running the Application
Open two terminal windows (with activated environments):

**Terminal 1 (Backend API):**
```bash
uvicorn backend.main:app --port 8000 --reload
```

**Terminal 2 (Frontend UI):**
```bash
streamlit run frontend/streamlit_app.py
```

### Usage
1. Open the Streamlit URL (usually `http://localhost:8501`).
2. Upload your CSV/Excel or PDF files from the sidebar.
3. Ask analytical questions in the chat!

## Project Structure
```text
ai-bi-copilot/
├── backend/
│   ├── main.py (FastAPI app)
│   ├── models/
│   │   └── api_models.py
│   └── services/
│       ├── analysis/
│       │   └── pandas_engine.py
│       ├── langgraph/
│       │   └── workflow.py
│       ├── llm/
│       │   └── groq_client.py
│       ├── rag/
│       │   └── pdf_engine.py
│       └── visualization/
│           └── chart_engine.py
├── frontend/
│   └── streamlit_app.py
├── data/ (File storage)
├── requirements.txt
└── .env
```
