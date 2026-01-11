"""Production server with REAL data - no mocks."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List, Dict
from datetime import datetime
import logging
from pydantic import BaseModel

# Real integrations
from integrations.reddit_public import RedditPublicClient
from integrations.polymarket_client import PolymarketClient
from integrations.kalshi_client import KalshiClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Prediq API",
    description="AI-powered prediction market intelligence with real-time sentiment analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
reddit_client = None
polymarket_client = None
kalshi_client = None
sentiment_analyzer = None

# Simple in-memory cache - Aggressive cleanup to minimize memory
markets_cache = {"polymarket": [], "kalshi": [], "timestamp": None}
sentiment_cache = {}  # Cache sentiment results: {market_id: {result, timestamp}}
CACHE_TTL = 1800  # 30 minutes - Aggressive cleanup to reduce memory
SENTIMENT_CACHE_TTL = 1800  # 30 minutes - Cache AI results
MAX_CACHE_SIZE = 150  # Maximum total markets to cache


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global reddit_client, polymarket_client, kalshi_client, sentiment_analyzer

    logger.info("🚀 Starting PRODUCTION server with REAL data...")

    # Initialize Reddit public client
    try:
        reddit_client = RedditPublicClient()
        logger.info("✅ Reddit public API client ready")
    except Exception as e:
        logger.error(f"❌ Reddit client failed: {e}")

    # Initialize Polymarket client
    try:
        polymarket_client = PolymarketClient()
        logger.info("✅ Polymarket API client ready")
    except Exception as e:
        logger.error(f"❌ Polymarket client failed: {e}")

    # Initialize Kalshi client
    try:
        kalshi_client = KalshiClient()
        logger.info("✅ Kalshi API client ready")
    except Exception as e:
        logger.error(f"❌ Kalshi client failed: {e}")

    # Initialize sentiment analyzer - Memory optimized version
    try:
        from transformers import pipeline
        logger.info("Loading sentiment model (optimized for memory)...")
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # CPU only
        )
        logger.info("✅ AI sentiment analyzer loaded (memory-optimized mode)")
    except Exception as e:
        logger.error(f"❌ Sentiment analyzer failed: {e}")
        sentiment_analyzer = None


def analyze_sentiment_batch(texts: List[str]) -> List[Dict]:
    """Analyze sentiment using real AI model."""
    if not sentiment_analyzer or not texts:
        return []

    try:
        # Filter and truncate texts
        valid_texts = [t[:512] for t in texts if t and len(t.strip()) > 0]

        if not valid_texts:
            return []

        # Batch inference
        results = sentiment_analyzer(valid_texts)

        # Normalize scores
        normalized = []
        for result in results:
            label = result['label'].upper()
            score = result['score']

            if 'POSITIVE' in label:
                normalized_score = score
            elif 'NEGATIVE' in label:
                normalized_score = -score
            else:
                normalized_score = 0.0

            normalized.append({
                'label': label,
                'score': score,
                'normalized_score': normalized_score
            })

        return normalized

    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return []


def calculate_sentiment_metrics(posts: List[Dict]) -> Dict:
    """Calculate aggregated sentiment from social posts."""
    if not posts:
        return {
            'sentiment_score': 0.0,
            'mention_count': 0,
            'engagement_score': 0.0,
            'positive_ratio': 0.0,
            'negative_ratio': 0.0,
            'neutral_ratio': 0.0
        }

    # Extract texts
    texts = []
    for post in posts:
        if post.get('platform') == 'reddit':
            text = f"{post.get('title', '')} {post.get('text', '')}"
            texts.append(text)

    # Analyze sentiments
    sentiments = analyze_sentiment_batch(texts)

    if not sentiments:
        return {'sentiment_score': 0.0, 'mention_count': len(posts)}

    # Calculate weighted sentiment
    weighted_scores = []
    total_weight = 0

    for post, sentiment in zip(posts, sentiments):
        engagement = post.get('upvotes', 0) + post.get('num_comments', 0) * 2
        weight = max(engagement, 1)

        weighted_scores.append(sentiment['normalized_score'] * weight)
        total_weight += weight

    avg_sentiment = sum(weighted_scores) / total_weight if total_weight > 0 else 0.0

    # Calculate ratios
    positive_count = sum(1 for s in sentiments if s['normalized_score'] > 0.3)
    negative_count = sum(1 for s in sentiments if s['normalized_score'] < -0.3)
    neutral_count = len(sentiments) - positive_count - negative_count

    total_count = len(sentiments)

    return {
        'sentiment_score': round(avg_sentiment, 3),
        'mention_count': len(posts),
        'engagement_score': sum(p.get('upvotes', 0) for p in posts),
        'positive_ratio': round(positive_count / total_count, 3) if total_count > 0 else 0,
        'negative_ratio': round(negative_count / total_count, 3) if total_count > 0 else 0,
        'neutral_ratio': round(neutral_count / total_count, 3) if total_count > 0 else 0,
        'timestamp': datetime.utcnow().isoformat()
    }


@app.get("/api")
async def api_info():
    """API info endpoint."""
    return {
        "message": "Prediq API",
        "version": "1.0.0",
        "status": "operational",
        "mode": "REAL_DATA",
        "data_sources": {
            "social": "Reddit Public JSON",
            "markets": "Polymarket + Kalshi Public APIs",
            "ai": "Hugging Face Transformers"
        }
    }


@app.get("/")
async def root():
    """Serve frontend."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {
            "message": "Prediq API",
            "version": "1.0.0",
            "status": "operational",
            "note": "Frontend not found. API is working at /api/markets"
        }


@app.get("/api/markets")
async def get_markets(
    platform: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50
):
    """Get REAL prediction markets from Polymarket and Kalshi."""
    global markets_cache

    # Check cache
    cache_valid = markets_cache["timestamp"] and \
                  (datetime.utcnow() - markets_cache["timestamp"]).total_seconds() < CACHE_TTL

    if cache_valid:
        logger.info("Using cached markets")
    else:
        await fetch_fresh_markets()

    # Get markets based on platform filter
    if platform == "polymarket":
        markets = markets_cache["polymarket"]
    elif platform == "kalshi":
        markets = markets_cache["kalshi"]
    else:
        # Return both platforms
        markets = markets_cache["polymarket"] + markets_cache["kalshi"]

    # Filter by category
    if category:
        markets = [m for m in markets if m.get("category") == category]

    return markets[:limit]


async def fetch_fresh_markets():
    """Fetch fresh markets from both Polymarket and Kalshi."""
    global markets_cache
    import gc

    # Clear old cache to free memory before fetching new data
    if markets_cache["polymarket"] or markets_cache["kalshi"]:
        markets_cache["polymarket"] = []
        markets_cache["kalshi"] = []
        gc.collect()  # Force garbage collection

    polymarket_markets = []
    kalshi_markets = []

    # Fetch from Polymarket
    if polymarket_client:
        try:
            logger.info("Fetching REAL markets from Polymarket...")
            polymarket_markets = polymarket_client.get_markets(limit=100, active=True)
            logger.info(f"✅ Fetched {len(polymarket_markets)} markets from Polymarket")
        except Exception as e:
            logger.error(f"Error fetching Polymarket markets: {e}")

    # Fetch from Kalshi
    if kalshi_client:
        try:
            logger.info("Fetching REAL markets from Kalshi...")
            kalshi_markets = kalshi_client.get_markets(limit=100, status="open")
            logger.info(f"✅ Fetched {len(kalshi_markets)} markets from Kalshi")
        except Exception as e:
            logger.error(f"Error fetching Kalshi markets: {e}")

    # Limit cache size to prevent memory overflow
    total_markets = len(polymarket_markets) + len(kalshi_markets)
    if total_markets > MAX_CACHE_SIZE:
        # Keep markets with highest volume
        all_markets = polymarket_markets + kalshi_markets
        all_markets.sort(key=lambda x: x.get('volume', 0), reverse=True)
        all_markets = all_markets[:MAX_CACHE_SIZE]

        # Split back
        polymarket_markets = [m for m in all_markets if m.get('platform') == 'polymarket']
        kalshi_markets = [m for m in all_markets if m.get('platform') == 'kalshi']
        logger.info(f"⚠️  Cache limited to {MAX_CACHE_SIZE} markets (was {total_markets})")

    # Update cache
    markets_cache["polymarket"] = polymarket_markets
    markets_cache["kalshi"] = kalshi_markets
    markets_cache["timestamp"] = datetime.utcnow()

    # Force garbage collection after cache update
    import gc
    gc.collect()

    return polymarket_markets + kalshi_markets


@app.get("/api/markets/{market_id}")
async def get_market_details(market_id: str):
    """Get market details with AI analysis (memory-optimized)."""
    global sentiment_cache

    # Search in both Polymarket and Kalshi caches
    all_markets = markets_cache.get("polymarket", []) + markets_cache.get("kalshi", [])
    market = next((m for m in all_markets if m.get("market_id") == market_id), None)

    if not market:
        raise HTTPException(status_code=404, detail="Market not found")

    # Check sentiment cache first
    now = datetime.utcnow()
    cached = sentiment_cache.get(market_id)
    if cached and (now - cached['timestamp']).total_seconds() < SENTIMENT_CACHE_TTL:
        logger.info(f"💾 Using cached sentiment for {market_id}")
        return {
            "market": market,
            "predictions": [cached['prediction']]
        }

    # REAL AI-powered prediction - Memory optimized
    try:
        title = market.get('title', '')
        keywords = ' '.join(title.split()[:3])

        logger.info(f"🔍 Analyzing sentiment for: {keywords}")

        # Fetch Reddit posts - REDUCED to 5 posts for memory optimization
        reddit_posts = reddit_client.search_posts(
            query=keywords,
            subreddit="all",
            time_filter="day",
            limit=5  # Reduced to 5 for memory optimization
        )

        if reddit_posts:
            metrics = calculate_sentiment_metrics(reddit_posts)
            sentiment_score = metrics.get('sentiment_score', 0.0)
            positive_ratio = metrics.get('positive_ratio', 0.5)
            mention_count = metrics.get('mention_count', 0)

            current_prob = market.get('current_probability', 0.5)
            sentiment_prob = (sentiment_score + 1) / 2

            gap = sentiment_prob - current_prob
            predicted_shift = gap * 100 * 0.7

            if mention_count > 20:
                confidence = "high"
            elif mention_count > 10:
                confidence = "medium"
            else:
                confidence = "low"

            reasoning = f"Sentiment: {sentiment_score:+.2f} ({int(positive_ratio*100)}% positive from {mention_count} posts). Market at {current_prob*100:.1f}%, sentiment suggests {sentiment_prob*100:.1f}%"

            logger.info(f"✅ AI Analysis: shift={predicted_shift:+.2f}%, confidence={confidence}, posts={mention_count}")

            # Aggressive memory cleanup
            import gc
            del reddit_posts, metrics
            gc.collect()
        else:
            predicted_shift = 0.0
            confidence = "low"
            reasoning = "No recent social media discussion found"
            logger.warning(f"⚠️  No Reddit posts found for: {keywords}")

    except Exception as e:
        logger.error(f"Error in AI prediction: {e}")
        predicted_shift = 0.0
        confidence = "low"
        reasoning = "Analysis unavailable"

    prediction = {
        "market_id": market_id,
        "predicted_shift": round(predicted_shift, 2),
        "confidence_level": confidence,
        "reasoning": reasoning,
        "time_horizon": "6h",
        "created_at": datetime.utcnow().isoformat()
    }

    # Cache the result
    sentiment_cache[market_id] = {
        'prediction': prediction,
        'timestamp': now
    }

    # Limit sentiment cache size
    if len(sentiment_cache) > 100:
        # Remove oldest entries
        sorted_cache = sorted(sentiment_cache.items(), key=lambda x: x[1]['timestamp'])
        for key, _ in sorted_cache[:50]:
            del sentiment_cache[key]

    return {
        "market": market,
        "predictions": [prediction]
    }


@app.post("/api/analyze-topic")
async def analyze_topic(topic: str, hours_back: int = 24):
    """Analyze sentiment from Reddit (memory-optimized)."""
    if not reddit_client:
        raise HTTPException(status_code=503, detail="Reddit client not available")

    try:
        logger.info(f"🔍 Analyzing REAL data for topic: {topic}")

        # Fetch Reddit posts - REDUCED to 5 posts for memory
        reddit_posts = reddit_client.search_posts(
            query=topic,
            subreddit="all",
            time_filter="day",
            limit=5  # Reduced to 5 for memory optimization
        )

        if not reddit_posts:
            raise HTTPException(
                status_code=404,
                detail=f"No Reddit posts found for topic: {topic}"
            )

        logger.info(f"📊 Found {len(reddit_posts)} real Reddit posts")

        # Analyze sentiment with REAL AI
        sentiment_metrics = calculate_sentiment_metrics(reddit_posts)

        # Match to markets
        matched_markets = []
        markets = markets_cache.get("polymarket", []) + markets_cache.get("kalshi", [])

        for market in markets[:50]:  # Limit to 50 markets to save memory
            title_lower = market.get("title", "").lower()
            topic_words = topic.lower().split()

            if any(word in title_lower for word in topic_words):
                matched_markets.append({
                    "market": market,
                    "similarity": 0.75
                })

        posts_count = len(reddit_posts)

        # Aggressive memory cleanup
        import gc
        del reddit_posts
        gc.collect()

        return {
            "topic": topic,
            "sentiment": sentiment_metrics,
            "matched_markets": matched_markets[:5],
            "posts_analyzed": posts_count,
            "mode": "REAL_DATA",
            "sources": ["Reddit Public API", "Hugging Face AI (optimized)"]
        }

    except Exception as e:
        logger.error(f"Error analyzing topic: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/refresh-markets")
async def refresh_markets():
    """Refresh markets from Polymarket and Kalshi."""
    markets = await fetch_fresh_markets()

    return {
        "status": "success",
        "total_markets": len(markets),
        "mode": "REAL_DATA",
        "source": "Polymarket + Kalshi Public APIs"
    }


@app.post("/api/clear-cache")
async def clear_cache():
    """Clear all cached data to free memory."""
    global markets_cache, sentiment_cache
    import gc

    old_markets = len(markets_cache.get("polymarket", [])) + len(markets_cache.get("kalshi", []))
    old_sentiments = len(sentiment_cache)

    markets_cache["polymarket"] = []
    markets_cache["kalshi"] = []
    markets_cache["timestamp"] = None
    sentiment_cache.clear()

    # Force aggressive garbage collection
    gc.collect()
    gc.collect()

    logger.info(f"🧹 Cache cleared: {old_markets} markets, {old_sentiments} sentiment results removed")

    return {
        "status": "success",
        "message": f"Cleared {old_markets} markets and {old_sentiments} sentiment results",
        "memory_freed": True
    }


@app.get("/api/alerts")
async def get_alerts(limit: int = 10):
    """Get alerts (simplified for now)."""
    return [
        {
            "id": 1,
            "alert_type": "system",
            "topic": "Production Mode",
            "message": "System is using REAL data from Reddit and Polymarket",
            "severity": "low",
            "created_at": datetime.utcnow().isoformat(),
            "read": False
        }
    ]


@app.get("/health")
async def health_check():
    """Health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "mode": "PRODUCTION",
        "services": {
            "api": True,
            "reddit_client": reddit_client is not None,
            "polymarket_client": polymarket_client is not None,
            "kalshi_client": kalshi_client is not None,
            "sentiment_analyzer": sentiment_analyzer is not None
        }
    }


# Mount static files for frontend assets
frontend_assets_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "assets")
if os.path.exists(frontend_assets_path):
    app.mount("/assets", StaticFiles(directory=frontend_assets_path), name="assets")
    logger.info(f"✅ Mounted frontend assets from: {frontend_assets_path}")


if __name__ == "__main__":
    import uvicorn
    logger.info("=" * 60)
    logger.info("🚀 PRODUCTION MODE - REAL DATA ONLY")
    logger.info("=" * 60)

    # Support PORT environment variable for cloud platforms (Render, Railway, etc.)
    port = int(os.getenv("PORT", 8002))
    logger.info(f"🌐 Starting server on port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
