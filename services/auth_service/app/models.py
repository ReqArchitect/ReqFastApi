from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    user_id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # Owner, Admin, Editor, Viewer
    tenant_id = Column(String, index=True)

class AuthToken(Base):
    __tablename__ = "auth_token"
    token = Column(String, primary_key=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    user_id = Column(String, index=True)
    tenant_id = Column(String, index=True)
    role = Column(String)
