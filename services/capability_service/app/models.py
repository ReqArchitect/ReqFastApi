from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class Capability(Base):
    __tablename__ = "capability"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    business_case_id = Column(UUID(as_uuid=True), ForeignKey("business_case.id"), nullable=False)
    initiative_id = Column(UUID(as_uuid=True), ForeignKey("initiative.id"), nullable=False)
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("kpi_service.id"), nullable=False)
    business_model_id = Column(UUID(as_uuid=True), ForeignKey("business_model_canvas.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
