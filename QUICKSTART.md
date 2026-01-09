# Quick Start Guide - AI-Powered Mindshare Market Analyzer

## 🚀 Get Started in 5 Minutes

### Option 1: Docker (Recommended)

```bash
# 1. Navigate to project
cd poly77

# 2. Set up environment variables
cd backend
cp .env.example .env
# Edit .env and add your Twitter & Reddit API credentials

# 3. Run the quick start script
cd ..
./start.sh

# 4. Open browser
# Visit http://localhost:3000
```

### Option 2: Manual Setup

**Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
# Edit .env with your API keys
uvicorn src.main:app --reload
```

**Frontend** (new terminal):
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

**Databases** (new terminal):
```bash
# Install PostgreSQL, MongoDB, Redis
# macOS:
brew install postgresql mongodb-community redis
brew services start postgresql
brew services start mongodb-community
brew services start redis
```

## 📝 Required API Keys

### Twitter API
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create app → Get Bearer Token
3. Add to `.env`: `TWITTER_BEARER_TOKEN=xxx`

### Reddit API
1. Go to https://www.reddit.com/prefs/apps
2. Create app (type: script)
3. Add to `.env`:
   ```
   REDDIT_CLIENT_ID=xxx
   REDDIT_CLIENT_SECRET=xxx
   ```

## 🎯 First Steps

### 1. Refresh Market Data
```bash
curl -X POST http://localhost:8000/api/refresh-markets
```

### 2. Analyze a Topic
```bash
curl -X POST "http://localhost:8000/api/analyze-topic?topic=Bitcoin&hours_back=24"
```

### 3. View Dashboard
Open http://localhost:3000 in your browser

## 📚 Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/markets` | GET | List all markets |
| `/api/markets/{id}` | GET | Market details + predictions |
| `/api/sentiment/{topic}` | GET | Sentiment data for topic |
| `/api/predictions` | GET | List predictions |
| `/api/alerts` | GET | Recent alerts |
| `/api/refresh-markets` | POST | Fetch latest markets |
| `/api/analyze-topic` | POST | Analyze topic sentiment |
| `/docs` | GET | Interactive API documentation |

## 🛠️ Common Commands

**View logs**:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Stop services**:
```bash
docker-compose down
```

**Restart**:
```bash
docker-compose restart
```

**Rebuild**:
```bash
docker-compose up --build
```

## 🐛 Troubleshooting

**Port already in use**:
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection error**:
```bash
docker-compose restart postgres
```

**Frontend can't connect**:
- Check backend is running: `curl http://localhost:8000/health`
- Verify `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`

**API rate limit**:
- Reduce polling frequency
- Wait 15 minutes for Twitter rate limit reset
- Consider Twitter API paid tier

## 📊 Project Structure

```
poly77/
├── backend/              # FastAPI Python backend
│   ├── src/
│   │   ├── main.py      # API entry point
│   │   ├── models/      # Database models
│   │   ├── services/    # AI services
│   │   └── integrations/# API clients
│   └── requirements.txt
├── frontend/            # Next.js React frontend
│   ├── src/
│   │   ├── app/        # Pages
│   │   └── components/ # UI components
│   └── package.json
├── blockchain/          # Smart contracts
│   └── base/
│       └── contracts/
└── docker-compose.yml   # Multi-service setup
```

## 🎓 Next Steps

1. **Explore the Dashboard**: Browse markets, view predictions
2. **Check API Docs**: Visit http://localhost:8000/docs
3. **Read Full Documentation**: See `SETUP.md` and `PROJECT_SUMMARY.md`
4. **Deploy Smart Contract**: See `blockchain/base/README.md`
5. **Customize**: Modify topics, thresholds, prediction algorithms

## 💡 Tips

- Start with popular topics: "Bitcoin", "Trump", "AI regulation"
- High engagement posts = better sentiment signals
- Cross-platform agreement (Twitter + Reddit) = higher confidence
- Market volume matters for liquidity
- Check alerts panel for significant sentiment shifts

## 📞 Need Help?

- **Setup Issues**: See `SETUP.md`
- **API Questions**: Check `/docs`
- **Architecture**: Read `PROJECT_SUMMARY.md`
- **Logs**: `docker-compose logs -f`

## ⚡ Performance Tips

- Use Redis caching (enabled by default)
- Limit social data fetch frequency
- Focus on high-volume markets
- Filter by category for faster loading
- Use WebSocket for real-time updates (no polling needed)

---

**Ready to predict markets with AI? Start now! 🚀**
