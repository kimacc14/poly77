"""Database models and connection setup."""
from datetime import datetime
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Database setup - use SQLite for local development if PostgreSQL not available
USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() == 'true'

if USE_SQLITE:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./mindshare_analyzer.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL setup
    POSTGRES_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    engine = create_engine(POSTGRES_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# SQLAlchemy Models
class Market(Base):
    """Prediction market from Kalshi or Polymarket."""
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)  # 'kalshi' or 'polymarket'
    market_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    category = Column(String, index=True)
    current_probability = Column(Float)
    volume = Column(Float)
    close_time = Column(DateTime)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sentiment_matches = relationship("SentimentMatch", back_populates="market")
    predictions = relationship("Prediction", back_populates="market")


class SentimentScore(Base):
    """Aggregated sentiment scores for topics."""
    __tablename__ = "sentiment_scores"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    platform = Column(String)  # 'twitter' or 'reddit'
    sentiment_score = Column(Float)  # -1 to +1
    mention_count = Column(Integer)
    engagement_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON)

    # Relationships
    sentiment_matches = relationship("SentimentMatch", back_populates="sentiment")


class SentimentMatch(Base):
    """Mapping between sentiment topics and markets."""
    __tablename__ = "sentiment_matches"

    id = Column(Integer, primary_key=True, index=True)
    sentiment_id = Column(Integer, ForeignKey("sentiment_scores.id"))
    market_id = Column(Integer, ForeignKey("markets.id"))
    similarity_score = Column(Float)
    manual_override = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sentiment = relationship("SentimentScore", back_populates="sentiment_matches")
    market = relationship("Market", back_populates="sentiment_matches")


class Prediction(Base):
    """Market shift predictions."""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(Integer, ForeignKey("markets.id"))
    predicted_shift = Column(Float)  # Percentage points
    confidence_level = Column(String)  # 'high', 'medium', 'low'
    reasoning = Column(String)
    time_horizon = Column(String)  # '1h', '6h', '24h'
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Accuracy tracking
    actual_shift = Column(Float, nullable=True)
    accuracy_calculated = Column(Boolean, default=False)

    # Relationships
    market = relationship("Market", back_populates="predictions")


class BlockchainProof(Base):
    """On-chain verification proofs."""
    __tablename__ = "blockchain_proofs"

    id = Column(Integer, primary_key=True, index=True)
    chain = Column(String)  # 'base' or 'solana'
    transaction_hash = Column(String, unique=True)
    data_hash = Column(String)
    sentiment_score = Column(Float)
    topic = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    verified = Column(Boolean, default=False)
    metadata = Column(JSON)


class Alert(Base):
    """User alerts."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String)  # 'sentiment_spike', 'prediction_high_confidence', etc.
    topic = Column(String)
    message = Column(String)
    severity = Column(String)  # 'high', 'medium', 'low'
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    read = Column(Boolean, default=False)


# Pydantic schemas for API
class MarketSchema(BaseModel):
    id: Optional[int] = None
    platform: str
    market_id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    current_probability: Optional[float] = None
    volume: Optional[float] = None
    close_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class SentimentScoreSchema(BaseModel):
    id: Optional[int] = None
    topic: str
    platform: str
    sentiment_score: float
    mention_count: int
    engagement_score: float
    timestamp: datetime

    class Config:
        from_attributes = True


class PredictionSchema(BaseModel):
    id: Optional[int] = None
    market_id: int
    predicted_shift: float
    confidence_level: str
    reasoning: str
    time_horizon: str
    created_at: datetime

    class Config:
        from_attributes = True


class AlertSchema(BaseModel):
    id: Optional[int] = None
    alert_type: str
    topic: str
    message: str
    severity: str
    created_at: datetime
    read: bool

    class Config:
        from_attributes = True


# Create tables
def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
