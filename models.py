from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Text, DateTime
from datetime import datetime
from db import engine

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile = Column(JSON, default={})   # other relative contents (such as signatures, intro, etc.)

class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    provider = Column(String)            # 'gmail' | 'outlook'
    email = Column(String)
    token_encrypted = Column(Text)       # 加密后的 token JSON
    scopes = Column(JSON, default={})

class EmailThread(Base):
    __tablename__ = "email_threads"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    provider_thread_id = Column(String)
    last_intent = Column(String)         # meeting_request / follow_up / ...
    state = Column(JSON, default={})
    updated_at = Column(DateTime, default=datetime.utcnow)

class EmailMessage(Base):
    __tablename__ = "email_messages"
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey("email_threads.id"))
    provider_msg_id = Column(String)
    from_addr = Column(String)
    to_addr = Column(String)
    subject = Column(String)
    raw_text = Column(Text)
    parsed_text = Column(Text)
    entities = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)    # meeting_request / follow_up / rejection
    jinja = Column(Text)

class Outbox(Base):
    __tablename__ = "outbox"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    provider = Column(String)            # gmail/outlook
    from_email = Column(String)
    to_email = Column(String)
    subject = Column(String)
    body_html = Column(Text)
    body_text = Column(Text)
    status = Column(String, default="pending")  # pending/approved/sent/failed
    meta = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

# 首次运行时建表
Base.metadata.create_all(bind=engine)
