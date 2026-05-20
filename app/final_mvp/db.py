import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./commerce.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True)
    sku = Column(String(120), index=True)
    title = Column(String(500))
    supplier_cost = Column(Float)
    shipping_cost = Column(Float)
    expected_sale_price = Column(Float)
    net_profit = Column(Float)
    margin_percent = Column(Float)
    risk_score = Column(Float)
    opportunity_score = Column(Float)
    decision = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class AutonomousEvent(Base):
    __tablename__ = "autonomous_events"

    id = Column(Integer, primary_key=True)
    event_type = Column(String(120))
    message = Column(Text)
    dry_run = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def db_status():
    init_db()
    return {
        "database": "postgresql" if DATABASE_URL.startswith("postgres") else "sqlite",
        "url_configured": bool(DATABASE_URL),
        "tables": ["opportunities", "autonomous_events"],
    }
