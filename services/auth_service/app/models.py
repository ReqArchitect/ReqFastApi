from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)  # Added for frontend support
    hashed_password = Column(String)
    role = Column(String)  # Owner, Admin, Editor, Viewer
    tenant_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class AuthToken(Base):
    __tablename__ = "auth_token"
    token = Column(String, primary_key=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    user_id = Column(String, index=True)
    tenant_id = Column(String, index=True)
    role = Column(String)

class Invitation(Base):
    __tablename__ = "invitation"
    invite_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    invite_token = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    role = Column(String)
    tenant_id = Column(String, index=True)
    invited_by = Column(String, index=True)
    message = Column(Text, nullable=True)
    expires_at = Column(DateTime)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
