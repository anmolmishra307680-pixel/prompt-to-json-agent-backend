from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from app.db import Base

class Spec(Base):
    __tablename__ = "specs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt = Column(Text, nullable=False)
    spec = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spec_id = Column(UUID(as_uuid=True), ForeignKey("specs.id"))
    evaluation = Column(JSONB)
    score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class FeedbackLog(Base):
    __tablename__ = "feedback_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    spec_id = Column(UUID(as_uuid=True))
    iteration = Column(Integer)
    before = Column(JSONB)
    after = Column(JSONB)
    feedback = Column(JSONB)
    reward = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ValuesLog(Base):
    __tablename__ = "values_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    honesty = Column(Text)
    integrity = Column(Text)
    discipline = Column(Text)
    gratitude = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())