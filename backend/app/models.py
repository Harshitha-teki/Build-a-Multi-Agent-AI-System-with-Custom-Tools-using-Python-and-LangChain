from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Run(Base):
    __tablename__ = "runs"
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    query = Column(Text)
    status = Column(String, default="running")
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, index=True)
    agent = Column(String)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ToolCall(Base):
    __tablename__ = "tool_calls"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, index=True)
    tool_name = Column(String)
    params = Column(Text)
    result = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
