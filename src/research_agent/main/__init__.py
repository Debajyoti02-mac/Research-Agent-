from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from slowapi import Limiter , _rate_limit_exceeded_handler 
from slowapi.util import get_remote_address 
from slowapi.errors import RateLimitExceeded
from research_agent.qa import qa_graph

REDIS_URL = "redis://localhost:6379"
limiter = Limiter(key_func=get_remote_address , storage_uri=REDIS_URL)


# Local application imports
from research_agent.database import get_db , PaperRun
from research_agent.security import senetize_input
from research_agent.graph import graph
from research_agent.pdf_engine import generate_paper_pdf

app = FastAPI(title="Research_agent")
app.state.limiter = limiter 
app.add_exception_handler(RateLimitExceeded , _rate_limit_exceeded_handler)


# Questions anwers 
class Ask_Request(BaseModel):
    question : str = Field(..., max_length=500, description="The specific question to ask the documents")
class AskResponse(BaseModel):
    question: str
    answer: str
    grounded: bool

# That for only the Research Field 
class ResearchRequest(BaseModel):
    topic: str = Field(..., max_length=300)
    raw_notes: str = Field(default="", max_length=15000)
    
@app.get("/api/v1/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/generate-paper", tags=["Paper engine"])
@limiter.limit("5/minute")
async def generate_paper(
    request: Request,
    payload: ResearchRequest,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host if request.client else "unknown"

    # 1. Sanitize user inputs
    clean_topic = senetize_input(payload.topic)
    clean_notes = senetize_input(payload.raw_notes)

    # 2. Record run initiation in database
    run_log = PaperRun(client_ip=client_ip, topic=clean_topic, status="INITIATED")
    db.add(run_log)
    db.commit()
    db.refresh(run_log)

    # 3. LangGraph Execution
    initial_state = {
        "query": clean_topic,
        "raw_notes": clean_notes,
        "retry": 0
    }

    try:
        final_output = graph.invoke(initial_state)
    except Exception as e:
        run_log.status = "FAILED"
        run_log.log_detail = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail="Failed to generate research paper.")

    # 4. Generate PDF buffer and mark run complete
    pdf_buffer = generate_paper_pdf(final_output)

    run_log.status = "SUCCESS"
    db.commit()

    file_slug = clean_topic[:30].strip().replace(" ", "_")
    filename = f"{file_slug}_Paper.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
# Question answer function build ------------- 
@app.post("/api/v1/ask",response_model=AskResponse,tags=["Q&A"])
async def QuestionAnswering(response :Ask_Request , request : Request , db:Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "unknown"
    
    clean_question = senetize_input(response.question)
    
    run_log = PaperRun(client_ip=client_ip , topic=f"Q&A: {clean_question[:50]}", status="INITIATED")
    db.add(run_log)
    db.commit()
    
    initial_state = {
        "query": clean_question,
        "raw_notes": "",
        "retry": 0,
        "context": [],
        "grounded": False,
        "answer": ""
    }
    
    try:
        # Run graph
        result = qa_graph.invoke(initial_state)
    except Exception as e:
        run_log.status = "FAILED"
        run_log.log_detail = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail="Q&A processing failed.")
    
    raw_answer = result.get("answer", "")
    
    final_text = getattr(raw_answer, "content", raw_answer)

    run_log.status = "SUCCESS"
    db.commit()

    return AskResponse(
        question=clean_question,
        answer=final_text,
        grounded=result.get("grounded", False)
    )