# AI-Powered Mindshare Market Analyzer - Setup Guide

## Overview

This guide will help you set up and run the AI-Powered Mindshare Market Analyzer application. The system analyzes social media sentiment and predicts prediction market shifts on Kalshi and Polymarket.

## Prerequisites

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+** and **Node.js 18+** (for local development)
- **Git**
- API credentials for:
  - Twitter (X) API
  - Reddit API
  - Kalshi API (optional)
  - Kaito AI API (optional)

## Quick Start with Docker

### 1. Clone Repository

```bash
git clone <repository-url>
cd poly77
```

### 2. Configure Environment Variables

Create `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your API credentials:

```bash
# Required
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Optional
KALSHI_API_KEY=your_kalshi_api_key
KAITO_API_KEY=your_kaito_api_key
```

### 3. Start Services

From the root directory:

```bash
docker-compose up --build
```

This will start:
- PostgreSQL (port 5432)
- MongoDB (port 27017)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)

### 4. Access Application

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

1. **Create Virtual Environment**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Set Up Databases**

Install and start PostgreSQL, MongoDB, and Redis locally.

For macOS with Homebrew:
```bash
brew install postgresql mongodb-community redis
brew services start postgresql
brew services start mongodb-community
brew services start redis
```

4. **Initialize Database**

```bash
# The database will be initialized automatically on first run
python -c "from src.models.database import init_db; init_db()"
```

5. **Run Backend**

```bash
uvicorn src.main:app --reload
```

### Frontend Setup

1. **Install Dependencies**

```bash
cd frontend
npm install
```

2. **Configure Environment**

Create `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run Frontend**

```bash
npm run dev
```

## API Credentials Setup

### Twitter (X) API

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new project and app
3. Generate Bearer Token
4. Add to `.env`: `TWITTER_BEARER_TOKEN=your_token`

**Note**: Free tier has very limited access. Consider paid tier for production.

### Reddit API

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" type
4. Note Client ID and Client Secret
5. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   ```

### Kalshi API

1. Create account at https://kalshi.com
2. Apply for API access at https://kalshi.com/builders
3. Generate API key from dashboard
4. Add to `.env`: `KALSHI_API_KEY=your_key`

### Kaito AI API

1. Visit https://www.kaito.ai/portal
2. Sign up for API access
3. Generate API key
4. Add to `.env`: `KAITO_API_KEY=your_key`

**Note**: Kaito integration is optional. The system can use built-in NLP models.

## Blockchain Setup (Optional)

### Deploy Smart Contract on Base

1. **Install Hardhat**

```bash
cd blockchain/base
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
```

2. **Configure Hardhat**

Create `hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    base: {
      url: "https://mainnet.base.org",
      accounts: [process.env.BASE_PRIVATE_KEY]
    },
    "base-sepolia": {
      url: "https://sepolia.base.org",
      accounts: [process.env.BASE_PRIVATE_KEY]
    }
  }
};
```

3. **Deploy Contract**

```bash
# Deploy to testnet
npx hardhat run scripts/deploy.js --network base-sepolia

# Deploy to mainnet (after testing)
npx hardhat run scripts/deploy.js --network base
```

4. **Update Backend Configuration**

Add contract address to `backend/.env`:
```
BASE_CONTRACT_ADDRESS=0x...
```

### Solana Setup

Solana integration requires Rust and Anchor framework. See blockchain/solana/README.md for detailed instructions.

## Testing the Application

### 1. Refresh Market Data

```bash
curl -X POST http://localhost:8000/api/refresh-markets
```

This fetches latest markets from Kalshi and Polymarket.

### 2. Analyze a Topic

```bash
curl -X POST "http://localhost:8000/api/analyze-topic?topic=Bitcoin%20regulation&hours_back=24"
```

This:
- Fetches social media posts about "Bitcoin regulation"
- Analyzes sentiment using AI
- Matches to relevant prediction markets
- Returns sentiment metrics and matched markets

### 3. View Markets on Frontend

Open http://localhost:3000 and browse the dashboard.

## Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'transformers'`

**Solution**: Ensure virtual environment is activated and dependencies installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database Connection Error

**Error**: `could not connect to server: Connection refused`

**Solution**: Ensure PostgreSQL is running:
```bash
# Check status
brew services list  # macOS
sudo systemctl status postgresql  # Linux

# Start if not running
brew services start postgresql  # macOS
sudo systemctl start postgresql  # Linux
```

### Twitter API Rate Limit

**Error**: `429 Too Many Requests`

**Solution**:
- Wait for rate limit to reset (15 minutes)
- Reduce polling frequency
- Upgrade to paid Twitter API tier

### Frontend Can't Connect to Backend

**Error**: Network error in browser console

**Solution**:
- Verify backend is running on port 8000
- Check CORS settings in `backend/src/main.py`
- Verify `NEXT_PUBLIC_API_URL` in frontend `.env.local`

### AI Model Download Issues

**Error**: `OSError: Can't load model`

**Solution**:
```bash
# Manually download models
python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; AutoTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment'); AutoModelForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')"

python -m spacy download en_core_web_sm
```

## Performance Optimization

### For Production Deployment

1. **Use Production Web Server**

Instead of `uvicorn` with `--reload`, use Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
```

2. **Enable Redis Caching**

Configure aggressive caching for market data:
```python
# Cache market data for 5 minutes
cache_ttl = 300
```

3. **Optimize Database Queries**

Add indexes on frequently queried columns:
```sql
CREATE INDEX idx_markets_platform ON markets(platform);
CREATE INDEX idx_markets_category ON markets(category);
CREATE INDEX idx_sentiment_topic ON sentiment_scores(topic);
CREATE INDEX idx_sentiment_timestamp ON sentiment_scores(timestamp);
```

4. **Use CDN for Frontend**

Deploy frontend to Vercel or Netlify with automatic CDN.

5. **Background Jobs**

Use Celery for periodic tasks (market refresh, sentiment analysis):
```bash
celery -A src.celery_app worker --loglevel=info
celery -A src.celery_app beat --loglevel=info
```

## Monitoring and Logging

### View Backend Logs

```bash
# Docker
docker-compose logs -f backend

# Manual
tail -f logs/app.log
```

### Health Check

```bash
curl http://localhost:8000/health
```

Returns status of all services.

## Next Steps

1. **Add Topics to Monitor**: Edit backend configuration to specify which topics to track
2. **Set Up Alerts**: Configure email/webhook notifications for high-confidence predictions
3. **Train Custom Models**: Fine-tune sentiment models on domain-specific data
4. **Deploy to Production**: Use cloud platforms (AWS, GCP, Vercel)
5. **Enable Authentication**: Add user accounts and personalized watchlists

## Support

For issues and questions:
- Check logs: `docker-compose logs`
- Review API documentation: http://localhost:8000/docs
- Submit GitHub issues for bugs

## Security Notes

⚠️ **Important**:
- Never commit `.env` files to Git
- Use environment-specific secrets management in production
- Rotate API keys regularly
- Use HTTPS in production
- Implement rate limiting for public APIs
- Validate and sanitize all user inputs

## License

See LICENSE file for details.
