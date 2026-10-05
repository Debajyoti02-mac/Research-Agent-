from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from slowapi import Limiter , _rate_limit_exceeded_handler 
from slowapi.util import get_remote_address 
from slowapi.errors import RateLimitExceeded
from research_agent.qa import qa_graph
from research_agent.database import get_db, User
from research_agent.security.auth import hash_password , verify_pasword , create_access_token , decode_access_token
from fastapi.security import OAuth2PasswordRequestForm
import os 
import jwt 
from dotenv import load_dotenv 
load_dotenv()


from fastapi.responses import FileResponse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
INDEX_FILE = BASE_DIR / "index.html"


# REDIS_URL = os.getenv("REDIS_URL")

limiter = Limiter(key_func=get_remote_address )


import logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("Research_agent")


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
    
class RegisterRequest(BaseModel):
    username: str
    password: str
    
@app.get("/", include_in_schema=False)
async def frontend():
    return FileResponse(INDEX_FILE)

@app.post("/api/v1/auth/register")
def register(data:RegisterRequest , db : Session=Depends(get_db)):
    existing_user = (db.query((User)).filter(User.username==data.username).first())
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed_password = hash_password(data.password)

    user = User(
        username=data.username,
        password_hash=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "username": user.username
    }

@app.post("/api/v1/auth/login")
def login(form_data : OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    users = (
        db.query(User).filter(User.username == form_data.username).first()
        
    )
    
    if not users:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
        
    if not verify_pasword(
        form_data.password,
        users.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(users.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
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
    logger.info("Research request received")
    try:
        final_output = graph.invoke(initial_state)
        logger.info("Research graph completed successfully")
    except Exception as e:
        logger.exception("Research graph failed")
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
@app.post(
    "/api/v1/ask",
    response_model=AskResponse,
    tags=["Q&A"]
)
async def QuestionAnswering(
    response: Ask_Request,
    request: Request,
    db: Session = Depends(get_db)
):
    client_ip = request.client.host if request.client else "unknown"

    logger.info("get Question request")

    clean_question = senetize_input(response.question)

    # 1. Create database record
    run_log = PaperRun(
        client_ip=client_ip,
        topic=f"Q&A: {clean_question[:50]}",
        status="INITIATED"
    )

    db.add(run_log)
    db.commit()
    db.refresh(run_log)

    # 2. Create initial state
    initial_state = {
        "query": clean_question,
        "raw_notes": "",
        "retry": 0,
        "context": [],
        "grounded": False,
        "answer": ""
    }

    # 3. Create LangGraph config
    config = {
        "configurable": {
            "thread_id": str(run_log.id)
        }
    }

    # 4. Run QA graph
    try:
        result = qa_graph.invoke(
            initial_state,
            config=config
        )

    except Exception as e:
        run_log.status = "FAILED"
        run_log.log_detail = str(e)
        db.commit()

        logger.exception("Research graph failed")

        raise HTTPException(
            status_code=500,
            detail="Q&A processing failed."
        )

    # 5. Get answer
    raw_answer = result.get("answer", "")
    final_text = getattr(raw_answer, "content", raw_answer)

    # 6. Save successful run
    run_log.status = "SUCCESS"
    db.commit()

    # 7. Return response
    return AskResponse(
        question=clean_question,
        answer=final_text,
        grounded=result.get("grounded", False)
    )