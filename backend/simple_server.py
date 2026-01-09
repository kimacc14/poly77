"""Simplified server for quick testing without heavy AI dependencies."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
import logging
from pydantic import BaseModel

# Mock data generator
from integrations.mock_data_generator import MockDataGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI-Powered Mindshare Market Analyzer (Simplified)",
    description="Quick demo version with mock data",
    version="1.0.0-demo"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize mock generator
mock_generator = MockDataGenerator()

# Mock markets data
MOCK_MARKETS = [
    {
        "id": 1,
        "platform": "kalshi",
        "market_id": "CRYPTO-REG-2026",
        "title": "Will Congress pass crypto regulation by Q2 2026?",
        "description": "This market resolves YES if comprehensive crypto regulation passes",
        "category": "politics",
        "current_probability": 0.623,
        "volume": 1234567,
        "close_time": "2026-06-30T23:59:59"
    },
    {
        "id": 2,
        "platform": "polymarket",
        "market_id": "BTC-100K-2026",
        "title": "Will Bitcoin reach $100,000 by end of 2026?",
        "description": "YES if BTC price exceeds $100,000 on any major exchange",
        "category": "cryptocurrency",
        "current_probability": 0.738,
        "volume": 2456789,
        "close_time": "2026-12-31T23:59:59"
    },
    {
        "id": 3,
        "platform": "kalshi",
        "market_id": "AI-MORATORIUM-2026",
        "title": "Will AI data center moratorium be enacted in 2026?",
        "description": "Federal or state level moratorium on new AI data centers",
        "category": "technology",
        "current_probability": 0.452,
        "volume": 567890,
        "close_time": "2026-12-31T23:59:59"
    },
    {
        "id": 4,
        "platform": "polymarket",
        "market_id": "SENATE-2026",
        "title": "Will Democrats control Senate after 2026 midterms?",
        "description": "Majority control of US Senate after November 2026 elections",
        "category": "politics",
        "current_probability": 0.517,
        "volume": 3789012,
        "close_time": "2026-11-04T23:59:59"
    },
    {
        "id": 5,
        "platform": "kalshi",
        "market_id": "CHIEFS-SB-2027",
        "title": "Will Chiefs win Super Bowl LXI in 2027?",
        "description": "Kansas City Chiefs win Super Bowl 61",
        "category": "sports",
        "current_probability": 0.684,
        "volume": 890234,
        "close_time": "2027-02-07T23:59:59"
    },
    {
        "id": 6,
        "platform": "polymarket",
        "market_id": "GPT5-2026",
        "title": "Will OpenAI release GPT-5 in 2026?",
        "description": "Official public release of GPT-5 model",
        "category": "technology",
        "current_probability": 0.821,
        "volume": 1678543,
        "close_time": "2026-12-31T23:59:59"
    }
]


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI-Powered Mindshare Market Analyzer API (Simplified Demo)",
        "version": "1.0.0-demo",
        "status": "operational",
        "mode": "mock_data",
        "note": "This is a lightweight demo version without heavy AI models"
    }


@app.get("/api/markets")
async def get_markets(
    platform: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50
):
    """Get prediction markets (mock data)."""
    markets = MOCK_MARKETS.copy()

    if platform:
        markets = [m for m in markets if m["platform"] == platform]
    if category:
        markets = [m for m in markets if m["category"] == category]

    return markets[:limit]


@app.get("/api/markets/{market_id}")
async def get_market_details(market_id: int):
    """Get detailed market information."""
    market = next((m for m in MOCK_MARKETS if m["id"] == market_id), None)

    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    # Mock prediction
    import random
    prediction = {
        "id": 1,
        "market_id": market_id,
        "predicted_shift": round(random.uniform(-5, 10), 2),
        "confidence_level": random.choice(["high", "medium", "low"]),
        "reasoning": "Sentiment increased significantly with high cross-platform agreement",
        "time_horizon": "6h",
        "created_at": datetime.utcnow().isoformat()
    }

    return {
        "market": market,
        "predictions": [prediction]
    }


@app.post("/api/analyze-topic")
async def analyze_topic(topic: str, hours_back: int = 24):
    """Analyze sentiment for a topic (using mock data)."""
    try:
        # Generate mock social data
        tweets = mock_generator.generate_mock_tweets(topic, count=50, hours_back=hours_back)
        reddit_posts = mock_generator.generate_mock_reddit_posts(topic, count=30)

        all_posts = tweets + reddit_posts

        # Mock sentiment analysis
        import random
        sentiment_metrics = {
            "topic": topic,
            "sentiment_score": round(random.uniform(-0.5, 0.8), 3),
            "mention_count": len(all_posts),
            "engagement_score": sum(
                p.get("likes", 0) + p.get("retweets", 0) + p.get("upvotes", 0)
                for p in all_posts
            ),
            "positive_ratio": round(random.uniform(0.3, 0.6), 3),
            "negative_ratio": round(random.uniform(0.2, 0.4), 3),
            "neutral_ratio": round(random.uniform(0.2, 0.3), 3),
            "timestamp": datetime.utcnow().isoformat()
        }

        # Match to markets (simple keyword matching)
        matched_markets = []
        for market in MOCK_MARKETS:
            if any(word.lower() in market["title"].lower() for word in topic.split()):
                matched_markets.append({
                    "market": market,
                    "similarity": round(random.uniform(0.6, 0.9), 2)
                })

        return {
            "topic": topic,
            "sentiment": sentiment_metrics,
            "matched_markets": matched_markets[:5],
            "posts_analyzed": len(all_posts),
            "mode": "mock_data"
        }

    except Exception as e:
        logger.error(f"Error analyzing topic: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/refresh-markets")
async def refresh_markets():
    """Refresh market data (mock - just returns static data)."""
    return {
        "status": "success",
        "new_markets": 0,
        "total_markets": len(MOCK_MARKETS),
        "mode": "mock_data",
        "note": "Using static mock data for demo"
    }


@app.get("/api/predictions")
async def get_predictions(confidence_level: Optional[str] = None, limit: int = 50):
    """Get market predictions (mock)."""
    import random
    predictions = []

    for market in MOCK_MARKETS[:limit]:
        pred = {
            "id": market["id"],
            "market_id": market["id"],
            "market_title": market["title"],
            "predicted_shift": round(random.uniform(-5, 10), 2),
            "confidence_level": random.choice(["high", "medium", "low"]),
            "reasoning": "Mock prediction based on simulated sentiment analysis",
            "time_horizon": "6h",
            "created_at": datetime.utcnow().isoformat()
        }

        if not confidence_level or pred["confidence_level"] == confidence_level:
            predictions.append(pred)

    return predictions


@app.get("/api/alerts")
async def get_alerts(unread_only: bool = False, limit: int = 50):
    """Get alerts (mock)."""
    mock_alerts = [
        {
            "id": 1,
            "alert_type": "sentiment_spike",
            "topic": "Bitcoin regulation",
            "message": "Bitcoin sentiment jumped +18% in last hour with 3.2x volume increase",
            "severity": "high",
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        },
        {
            "id": 2,
            "alert_type": "prediction_high_confidence",
            "topic": "2026 election",
            "message": "High confidence prediction: +5.2% shift expected in next 6 hours",
            "severity": "medium",
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        },
        {
            "id": 3,
            "alert_type": "market_update",
            "topic": "AI policy",
            "message": "Cross-platform sentiment agreement at 89%",
            "severity": "low",
            "created_at": datetime.utcnow().isoformat(),
            "read": True
        }
    ]

    if unread_only:
        mock_alerts = [a for a in mock_alerts if not a["read"]]

    return mock_alerts[:limit]


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "mock_data_demo",
        "services": {
            "api": True,
            "mock_generator": True,
            "database": "sqlite",
            "ai_models": False  # Not loaded for speed
        }
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting simplified demo server...")
    logger.info("Mode: Mock data only (no heavy AI models)")
    logger.info("Access at: http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)
