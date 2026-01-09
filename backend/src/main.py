"""Main FastAPI application for AI-Powered Mindshare Market Analyzer."""
import logging
from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
from contextlib import asynccontextmanager

from models.database import init_db, get_db, Market, SentimentScore, Prediction, Alert
from models.database import MarketSchema, SentimentScoreSchema, PredictionSchema, AlertSchema
from services.sentiment_analyzer import SentimentAnalyzer, MindshareCalculator
from services.semantic_matcher import SemanticMatcher
from services.prediction_engine import PredictionEngine
from integrations.twitter_client import TwitterClient
from integrations.reddit_client import RedditClient
from integrations.kalshi_client import KalshiClient
from integrations.polymarket_client import PolymarketClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global service instances
sentiment_analyzer = None
semantic_matcher = None
prediction_engine = None

# API clients
twitter_client = None
reddit_client = None
kalshi_client = None
polymarket_client = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown."""
    # Startup
    logger.info("Starting up application...")

    global sentiment_analyzer, semantic_matcher, prediction_engine
    global twitter_client, reddit_client, kalshi_client, polymarket_client

    # Initialize database
    init_db()

    # Initialize AI services
    try:
        sentiment_analyzer = SentimentAnalyzer()
        semantic_matcher = SemanticMatcher()
        prediction_engine = PredictionEngine()
        logger.info("AI services initialized")
    except Exception as e:
        logger.error(f"Error initializing AI services: {e}")

    # Initialize API clients
    try:
        twitter_client = TwitterClient()
        reddit_client = RedditClient()
        kalshi_client = KalshiClient()
        polymarket_client = PolymarketClient()
        logger.info("API clients initialized")
    except Exception as e:
        logger.error(f"Error initializing API clients: {e}")

    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="AI-Powered Mindshare Market Analyzer",
    description="Analyze social sentiment and predict prediction market shifts",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routes

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI-Powered Mindshare Market Analyzer API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/api/markets", response_model=List[MarketSchema])
async def get_markets(
    platform: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get prediction markets."""
    query = db.query(Market)

    if platform:
        query = query.filter(Market.platform == platform)
    if category:
        query = query.filter(Market.category == category)

    markets = query.order_by(Market.volume.desc()).limit(limit).all()
    return markets


@app.get("/api/markets/{market_id}")
async def get_market_details(market_id: int, db: Session = Depends(get_db)):
    """Get detailed market information."""
    market = db.query(Market).filter(Market.id == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    # Get recent predictions
    predictions = db.query(Prediction).filter(
        Prediction.market_id == market_id
    ).order_by(Prediction.created_at.desc()).limit(5).all()

    return {
        "market": market,
        "predictions": predictions
    }


@app.get("/api/sentiment/{topic}")
async def get_sentiment(
    topic: str,
    hours_back: int = 24,
    db: Session = Depends(get_db)
):
    """Get sentiment data for a topic."""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)

    sentiments = db.query(SentimentScore).filter(
        SentimentScore.topic == topic,
        SentimentScore.timestamp >= cutoff_time
    ).order_by(SentimentScore.timestamp.desc()).all()

    if not sentiments:
        raise HTTPException(status_code=404, detail="No sentiment data found for topic")

    return {
        "topic": topic,
        "current_sentiment": sentiments[0],
        "historical_data": sentiments
    }


@app.get("/api/predictions", response_model=List[PredictionSchema])
async def get_predictions(
    confidence_level: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get market predictions."""
    query = db.query(Prediction)

    if confidence_level:
        query = query.filter(Prediction.confidence_level == confidence_level)

    predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
    return predictions


@app.get("/api/alerts", response_model=List[AlertSchema])
async def get_alerts(
    unread_only: bool = False,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get alerts."""
    query = db.query(Alert)

    if unread_only:
        query = query.filter(Alert.read == False)

    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    return alerts


@app.post("/api/refresh-markets")
async def refresh_markets(db: Session = Depends(get_db)):
    """Refresh market data from Kalshi and Polymarket."""
    try:
        new_markets = []

        # Fetch from Kalshi
        if kalshi_client:
            kalshi_markets = kalshi_client.get_markets(limit=100)
            for market_data in kalshi_markets:
                market = Market(
                    platform=market_data['platform'],
                    market_id=market_data['market_id'],
                    title=market_data['title'],
                    description=market_data.get('description', ''),
                    category=market_data.get('category', ''),
                    current_probability=market_data.get('current_probability', 0.5),
                    volume=market_data.get('volume', 0),
                    close_time=market_data.get('close_time'),
                    metadata=market_data.get('metadata', {})
                )

                # Check if exists
                existing = db.query(Market).filter(
                    Market.market_id == market.market_id
                ).first()

                if existing:
                    # Update existing
                    existing.current_probability = market.current_probability
                    existing.volume = market.volume
                    existing.updated_at = datetime.utcnow()
                else:
                    # Add new
                    db.add(market)
                    new_markets.append(market)

        # Fetch from Polymarket
        if polymarket_client:
            poly_markets = polymarket_client.get_markets(limit=100)
            for market_data in poly_markets:
                market = Market(
                    platform=market_data['platform'],
                    market_id=market_data['market_id'],
                    title=market_data['title'],
                    description=market_data.get('description', ''),
                    category=market_data.get('category', ''),
                    current_probability=market_data.get('current_probability', 0.5),
                    volume=market_data.get('volume', 0),
                    close_time=market_data.get('close_time'),
                    metadata=market_data.get('metadata', {})
                )

                existing = db.query(Market).filter(
                    Market.market_id == market.market_id
                ).first()

                if existing:
                    existing.current_probability = market.current_probability
                    existing.volume = market.volume
                    existing.updated_at = datetime.utcnow()
                else:
                    db.add(market)
                    new_markets.append(market)

        db.commit()

        return {
            "status": "success",
            "new_markets": len(new_markets),
            "total_markets": db.query(Market).count()
        }

    except Exception as e:
        logger.error(f"Error refreshing markets: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-topic")
async def analyze_topic(
    topic: str,
    hours_back: int = 24,
    db: Session = Depends(get_db)
):
    """Analyze sentiment for a topic and match to markets."""
    try:
        # Fetch social data
        twitter_posts = []
        reddit_posts = []

        if twitter_client:
            twitter_posts = twitter_client.search_recent_tweets(topic, hours_back=hours_back)

        if reddit_client:
            reddit_posts = reddit_client.search_posts(topic, time_filter='day')

        all_posts = twitter_posts + reddit_posts

        if not all_posts:
            raise HTTPException(status_code=404, detail="No social data found for topic")

        # Analyze sentiment
        if sentiment_analyzer:
            sentiment_metrics = sentiment_analyzer.analyze_social_posts(all_posts)

            # Save sentiment score
            sentiment_record = SentimentScore(
                topic=topic,
                platform='combined',
                sentiment_score=sentiment_metrics['sentiment_score'],
                mention_count=sentiment_metrics['mention_count'],
                engagement_score=sentiment_metrics['engagement_score'],
                metadata=sentiment_metrics
            )
            db.add(sentiment_record)
            db.commit()

        # Match to markets
        markets = db.query(Market).all()
        topic_description = semantic_matcher.create_topic_description(all_posts) if semantic_matcher else ""

        matches = []
        if semantic_matcher:
            matches = semantic_matcher.match_topic_to_markets(
                topic,
                topic_description,
                [m.__dict__ for m in markets]
            )

        return {
            "topic": topic,
            "sentiment": sentiment_metrics if sentiment_analyzer else {},
            "matched_markets": [
                {"market": m[0], "similarity": m[1]} for m in matches
            ]
        }

    except Exception as e:
        logger.error(f"Error analyzing topic: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection for real-time updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(30)
            await websocket.send_json({"type": "ping", "timestamp": datetime.utcnow().isoformat()})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "sentiment_analyzer": sentiment_analyzer is not None,
            "semantic_matcher": semantic_matcher is not None,
            "prediction_engine": prediction_engine is not None,
            "twitter_client": twitter_client is not None,
            "reddit_client": reddit_client is not None,
            "kalshi_client": kalshi_client is not None,
            "polymarket_client": polymarket_client is not None
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
