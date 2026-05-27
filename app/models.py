from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.db import Base

class MetaEvent(Base):
    __tablename__ = "meta_events"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(100), nullable=False)
    pixel_id = Column(String(100), nullable=False)
    status_code = Column(Integer, nullable=True)
    ok = Column(String(20), nullable=False)
    source = Column(String(100), nullable=True)
    event_source_url = Column(String(500), nullable=True)
    meta_response = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
