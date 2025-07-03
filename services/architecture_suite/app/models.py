from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime


Base = declarative_base()

# Real parent tables (minimal for FK checks)
class BusinessCase(Base):
    __tablename__ = "business_case"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)

class Initiative(Base):
    __tablename__ = "initiative"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)

class KPIService(Base):
    __tablename__ = "kpi_service"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)

class BusinessModelCanvas(Base):
    __tablename__ = "business_model_canvas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)

# Many-to-many linking table for ArchiMate elements
class ArchitectureElementLink(Base):
    __tablename__ = "architecture_element_link"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id = Column(UUID(as_uuid=True), ForeignKey("architecture_package.id"), nullable=False)
    element_type = Column(String, nullable=False)  # e.g., "ApplicationComponent"
    element_id = Column(UUID(as_uuid=True), nullable=False)
    traceability_fk = Column(String, nullable=False)  # e.g., "business_case_id"

class ArchitecturePackage(Base):
    __tablename__ = "architecture_package"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    business_case_id = Column(UUID(as_uuid=True), ForeignKey("business_case.id"), nullable=False)
    initiative_id = Column(UUID(as_uuid=True), ForeignKey("initiative.id"), nullable=False)
    kpi_id = Column(UUID(as_uuid=True), ForeignKey("kpi_service.id"), nullable=False)
    business_model_id = Column(UUID(as_uuid=True), ForeignKey("business_model_canvas.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
