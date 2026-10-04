import os
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./research_agent.db"

engine = create_engine(url=DATABASE_URL,connect_args={"check_same_thread": False})

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

class PaperRun(base):
    __tablename__ = "paper_runs"

    id = Column(Integer, primary_key=True, index=True)
    client_ip = Column(String(50))
    topic = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="INITIATED")
    log_detail = Column(Text, default="")
    
base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
