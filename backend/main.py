import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.models.api_models import ChatRequest, ChatResponse

app = FastAPI(title="AI BI Copilot API", description="Conversational BI platform API")

# Setup CORS for the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "AI BI Copilot API is running"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Endpoint to upload files (CSV, PDF) for analysis.
    """
    uploaded_files = []
    
    for file in files:
        if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx") or file.filename.endswith(".pdf")):
            raise HTTPException(status_code=400, detail=f"File {file.filename} is not supported. Upload CSV, Excel, or PDF.")
            
        file_path = os.path.join(DATA_DIR, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files.append(file.filename)
            
            # TODO: Trigger ingestion/processing for this file
            # Phase 2 Data Engine will be hooked up here
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not upload {file.filename}: {str(e)}")
            
    return {"message": f"Successfully uploaded {len(uploaded_files)} files.", "files": uploaded_files}

from backend.services.langgraph.workflow import agent_graph

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main endpoint for asking analytical questions.
    """
    # Initialize the state
    initial_state = {
        "query": request.query,
        "intent": "",
        "target_files": [],
        "context": "",
        "analysis_result": None,
        "charts": [],
        "insight": "",
        "final_response": "",
        "error": ""
    }
    
    try:
        # Run through LangGraph
        result_state = agent_graph.invoke(initial_state)
        
        # Check for error
        if result_state.get("error"):
            return ChatResponse(
                text=f"Error executing query: {result_state['error']}",
                chart=None,
                insight=None
            )
            
        return ChatResponse(
            text=result_state.get("final_response", "I could not generate an answer."),
            charts=result_state.get("charts", []),
            insight=result_state.get("insight")
        )
    except Exception as e:
        return ChatResponse(
            text=f"System error: {str(e)}",
            chart=None,
            insight=None
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
