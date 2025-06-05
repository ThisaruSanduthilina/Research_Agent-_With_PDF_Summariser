from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
from main import ResearchAgent
import time
import json
import os
from io import BytesIO

from utils.pdf_parser import PDFParser

app = FastAPI(
    title="Research Agent API",
    description="API for AI-powered research and text summarization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create global instances
research_agent = ResearchAgent()
pdf_parser = PDFParser()

# History of research results
research_history = []
history_file = 'research_history.json'

# Load research history if file exists
if os.path.exists(history_file):
    try:
        with open(history_file, 'r') as f:
            research_history = json.load(f)
    except:
        research_history = []

# Pydantic models for request/response validation
class ResearchRequest(BaseModel):
    topic: str
    depth: int = 2

class PromptRequest(BaseModel):
    prompt: str
    depth: int = 2

class SummarizeRequest(BaseModel):
    text: str
    max_sentences: int = 3

class ResearchResult(BaseModel):
    topic: str
    source: str
    summary: str
    timestamp: float

class HistoryEntry(BaseModel):
    id: int
    topic: str
    timestamp: float
    result_count: int
    results: List[ResearchResult]
    prompt: Optional[str] = None

class ResearchResponse(BaseModel):
    research_id: int
    topic: str
    results: List[Dict[str, Any]]
    result_count: int
    processing_time: float
    prompt: Optional[str] = None

class SummaryResponse(BaseModel):
    original_length: int
    summary: str
    summary_length: int
    processing_time: float

class PDFResponse(BaseModel):
    filename: str
    content_sample: str
    summary: str

class ErrorResponse(BaseModel):
    error: str

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Check if the API is healthy and running."""
    return {"status": "healthy", "service": "research-agent-api"}

@app.get("/api/research", response_model=ResearchResponse, tags=["Research"])
@app.post("/api/research", response_model=ResearchResponse, tags=["Research"])
async def perform_research(
    research_req: Optional[ResearchRequest] = None,
    topic: Optional[str] = Query(None, description="Research topic"),
    depth: int = Query(2, description="Search depth (number of sources to analyze)")
):
    """
    Perform research on a given topic.
    
    - **topic**: Topic to research
    - **depth**: Number of sources to analyze (default: 2)
    """
    # For POST requests with body parameters
    if research_req is not None:
        if not research_req.topic or research_req.topic.strip() == "" or research_req.topic.strip() == "string":
            raise HTTPException(status_code=400, detail="Missing or invalid topic parameter in request body")
        research_topic = research_req.topic.strip()
        research_depth = research_req.depth
    # For GET requests or POST with query parameters
    else:
        if not topic or topic.strip() == "" or topic.strip() == "string":
            raise HTTPException(status_code=400, detail="Missing or invalid topic parameter in query")
        research_topic = topic.strip()
        research_depth = depth
    
    print(f"API received research  request for topic: '{research_topic}'")
    
    try:
        # Perform the research
        start_time = time.time()
        results = research_agent.research(research_topic, research_depth)
        end_time = time.time()
        
        # Format the results
        formatted_results = []
        for item in results:
            formatted_results.append({
                'topic': item['topic'],
                'source': item['source'],
                'summary': item['summary'],
                'timestamp': item['timestamp']
            })

        # Save to history
        history_entry = {
            'id': len(research_history) + 1,
            'topic': research_topic,
            'timestamp': time.time(),
            'result_count': len(formatted_results),
            'results': formatted_results
        }
        research_history.append(history_entry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
        
        # Save history to file
        with open(history_file, 'w') as f:
            json.dump(research_history, f)
        
        # Return the results
        return {
            'research_id': history_entry['id'],
            'topic': research_topic,
            'results': formatted_results,
            'result_count': len(formatted_results),
            'processing_time': round(end_time - start_time, 2)
        }
    
    except Exception as e:
        print(f"Error performing research: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history", response_model=List[HistoryEntry], tags=["History"])
async def get_history():
    """Get the complete research history."""
    return research_history

@app.get("/api/history/{research_id}", response_model=HistoryEntry, tags=["History"])
async def get_research_by_id(research_id: int):
    """Get a specific research entry by its ID."""
    for entry in research_history:
        if entry['id'] == research_id:
            return entry
    
    raise HTTPException(status_code=404, detail="Research not found")

@app.get("/api/topics", response_model=List[str], tags=["Research"])
async def get_topics():
    """Get a list of all researched topics."""
    topics = list(set(entry['topic'] for entry in research_history))
    return topics

@app.get("/api/prompt", response_model=ResearchResponse, tags=["Research"])
@app.post("/api/prompt", response_model=ResearchResponse, tags=["Research"])
async def handle_prompt(
    prompt_req: Optional[PromptRequest] = None,
    prompt: Optional[str] = Query(None, description="Research prompt"),
    depth: int = Query(2, description="Search depth (number of sources to analyze)")
):
    """
    Perform research based on a natural language prompt.
    
    - **prompt**: Natural language research prompt
    - **depth**: Number of sources to analyze (default: 2)
    """
    # Handle GET requests
    if prompt_req is None:
        if prompt is None:
            raise HTTPException(status_code=400, detail="Missing prompt parameter")
        research_prompt = prompt
        research_depth = depth
    # Handle POST requests
    else:
        research_prompt = prompt_req.prompt
        research_depth = prompt_req.depth
    
    try:
        # Extract research topic from the prompt
        topic = research_prompt  # Simple approach - use prompt as topic
        
        # Perform the research
        start_time = time.time()
        results = research_agent.research(topic, research_depth)
        end_time = time.time()
        
        # Format the results
        formatted_results = []
        for item in results:
            formatted_results.append({
                'topic': item['topic'],
                'source': item['source'],
                'summary': item['summary'],
                'timestamp': item['timestamp']
            })
        
        # Save to history
        history_entry = {
            'id': len(research_history) + 1,
            'prompt': research_prompt,
            'topic': topic,
            'timestamp': time.time(),
            'result_count': len(formatted_results),
            'results': formatted_results
        }
        research_history.append(history_entry)
        
        # Save history to file
        with open(history_file, 'w') as f:
            json.dump(research_history, f)
        
        # Return the results
        return {
            'research_id': history_entry['id'],
            'prompt': research_prompt,
            'topic': topic,
            'results': formatted_results,
            'result_count': len(formatted_results),
            'processing_time': round(end_time - start_time, 2)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/pdf", response_model=PDFResponse, tags=["Content Processing"])
async def process_pdf(file: UploadFile = File(...)):
    """
    Process a PDF file and generate a summary of its content.
    
    - **file**: PDF file to process (must be a valid PDF document)
    
    Returns:
    - **filename**: Name of the processed file
    - **content_sample**: Sample of the extracted content
    - **summary**: AI-generated summary of the PDF content
    """
    # Validate file extension
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Only PDF files are accepted."
        )
    
    try:
        # Read the file content
        contents = await file.read()
        
        # Check if file is empty
        if len(contents) == 0:
            raise HTTPException(status_code=400, detail="The PDF file appears to be empty")
            
        file_stream = BytesIO(contents)
        
        # Process the PDF
        pdf_content = pdf_parser.parse_pdf(file_stream)
        
        # Check if content was successfully extracted
        if not pdf_content or pdf_content.startswith("Error extracting text:"):
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from the PDF. It may be encrypted, damaged, or contain only images."
            
            )
        
        # Generate summary using the AI processor
        summary = research_agent.processor.summarize(pdf_content)
        
        # Prepare the response
        content_sample = pdf_content[:500] + "..." if len(pdf_content) > 500 else pdf_content
        
        return {
            'filename': file.filename,
            'content_sample': content_sample,
            'summary': summary
        }
        
    except Exception as e:
        # Log the error (you might want to use a proper logging system)
        print(f"Error processing PDF: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing PDF: {str(e)}"
        )
    
