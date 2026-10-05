from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./research_agent.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

class PaperRun(Base):
    __tablename__ = "paper_runs"

    id = Column(Integer, primary_key=True, index=True)
    client_ip = Column(String(50))
    topic = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="INITIATED")
    log_detail = Column(Text, default="")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()