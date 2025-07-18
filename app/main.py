from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag import query_rag
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    term: str

@app.post("/explain")
def explain_term(query: Query):
    try:
        if not query.term:
            raise HTTPException(status_code=400, detail="Term cannot be empty")
            
        logger.info(f"Processing query: {query.term}")
        result = query_rag(query.term)
        return {"response": result}
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "ok"}