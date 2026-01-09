# Prediq - AI Market Predictions

AI-powered prediction market intelligence with real-time sentiment analysis.

🌐 **Live at:** https://prediq.site

---

## 🎯 What is Prediq?

Prediq is an AI-powered platform that analyzes prediction markets from **Polymarket** and **Kalshi** with real-time sentiment intelligence from social media (Reddit). Get data-driven insights to make smarter trading decisions.

### Key Features

- ✅ **Real-time Market Data** - Live odds from Polymarket & Kalshi
- ✅ **AI Sentiment Analysis** - Hugging Face DistilBERT model analyzes social sentiment
- ✅ **Category Filters** - Politics, Crypto, Tech, Sports, and more
- ✅ **Platform Filters** - View Polymarket or Kalshi separately
- ✅ **Market Intelligence** - Volume, probability, end dates, and direct trade links

---

## 🚀 Tech Stack

### Backend
- **FastAPI** 0.109.0 - High-performance Python web framework
- **PyTorch** 2.2.0 - AI model inference
- **Transformers** 4.40.0 - Hugging Face sentiment analysis
- **Uvicorn** 0.27.0 - ASGI server

### Frontend
- **Vanilla JavaScript** - Lightweight and fast
- **Tailwind CSS** - Modern responsive design
- **No build step** - Pure HTML/CSS/JS

### APIs
- **Polymarket CLOB API (Gamma)** - Real-time prediction market data
- **Kalshi Events API** - Sports and events markets
- **Reddit Public JSON API** - Social sentiment data

### Deployment
- **Railway.app** - Backend hosting
- **Domain**: prediq.site
- **SSL**: Automatic Let's Encrypt

---

## 📁 Project Structure

```
poly77/
├── backend/                    # FastAPI backend
│   ├── production_server.py   # Main API server
│   ├── requirements.txt        # Python dependencies
│   └── src/
│       ├── integrations/       # API clients
│       │   ├── polymarket_client.py
│       │   ├── kalshi_client.py
│       │   └── reddit_public.py
│       └── ai/                 # AI models
│           └── sentiment_analyzer.py
│
├── frontend/                   # Static frontend
│   ├── index.html             # Main UI
│   └── assets/                # Images and logos
│
└── docs/                      # Documentation
    ├── RAILWAY_SETUP.md
    ├── CUSTOM_DOMAIN_GUIDE.md
    └── SECURITY_AUDIT_REPORT.md
```

---

## 🛠️ Local Development

### Prerequisites

- Python 3.12+
- pip
- Git

### Setup

1. **Clone repository:**
   ```bash
   git clone https://github.com/kimacc14/poly77.git
   cd poly77
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

4. **Run development server:**
   ```bash
   cd backend
   python production_server.py
   ```

5. **Open browser:**
   ```
   http://localhost:8002
   ```

---

## 🔑 Environment Variables

Create `backend/.env`:

```bash
# Reddit API (for sentiment analysis)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Twitter API (optional)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Kalshi API (optional - uses public API if not set)
KALSHI_API_KEY=your_kalshi_api_key

# Server port (default: 8002)
PORT=8002
```

### Get API Keys

**Reddit API:**
1. Go to: https://www.reddit.com/prefs/apps
2. Create app type "script"
3. Copy Client ID and Secret

**Kalshi API:**
- Uses public API by default
- Premium features: https://kalshi.com/api

---

## 🚀 Deployment

### Railway (Production)

```bash
# Login to Railway
railway login

# Link to project
railway link 77950b06-1505-4ce4-9198-d48dd25291a9

# Deploy
railway up
```

**Production URL:** https://poly77-ai-market-analyzer-production.up.railway.app
**Custom Domain:** https://prediq.site

### Other Platforms

- **Render.com** - See `RENDER_DEPLOYMENT_GUIDE.md`
- **Hugging Face Spaces** - See `HUGGINGFACE_DEPLOYMENT.md`

---

## 📊 API Endpoints

### Health Check
```bash
GET /health
```

Returns API status and service availability.

### Get Markets
```bash
GET /api/markets?platform={polymarket|kalshi}&category={politics|crypto|tech|sports}
```

Returns list of prediction markets with:
- Market ID, title, description
- Current probability & volume
- Platform, category, end date
- Direct trade URLs

### Get Market Details + AI Analysis
```bash
GET /api/markets/{market_id}
```

Returns detailed market info with:
- Full market data
- AI sentiment analysis
- Reddit discussion sentiment
- Prediction confidence

---

## 🧠 AI Sentiment Analysis

Prediq uses **DistilBERT** from Hugging Face for real-time sentiment analysis:

- **Model:** `distilbert-base-uncased-finetuned-sst-2-english`
- **Input:** Reddit posts and comments related to market topics
- **Output:** Sentiment score (-1 to +1) and confidence level
- **Performance:** ~100-300ms per analysis

---

## 🔐 Security

- ✅ No secrets in code - all use environment variables
- ✅ `.env` files properly gitignored
- ✅ CORS configured for production
- ✅ Input validation on all endpoints
- ✅ Rate limiting on API calls
- ✅ Comprehensive security audit passed

See `SECURITY_AUDIT_REPORT.md` for details.

---

## 📈 Performance

- **API Response Time:** <500ms average
- **Market Data Cache:** 5 minutes TTL
- **AI Analysis:** ~200ms per market
- **Concurrent Users:** Supports 100+ simultaneous connections

---

## 🛣️ Roadmap

### Completed ✅
- [x] Real-time Polymarket & Kalshi integration
- [x] AI sentiment analysis (Reddit)
- [x] Category and platform filtering
- [x] Railway deployment
- [x] Custom domain (prediq.site)
- [x] SSL certificate
- [x] Mobile-responsive UI

### In Progress 🚧
- [ ] User accounts & watchlists
- [ ] Email alerts for market changes
- [ ] Historical sentiment tracking
- [ ] Advanced charting

### Future 🔮
- [ ] Twitter/X sentiment integration
- [ ] Portfolio tracking
- [ ] Mobile app (React Native)
- [ ] API rate limiting & authentication
- [ ] Premium tier features

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📧 Contact

- **Website:** https://prediq.site
- **GitHub:** https://github.com/kimacc14/poly77
- **Issues:** https://github.com/kimacc14/poly77/issues

---

## 🙏 Acknowledgments

- **Polymarket** - Prediction market data
- **Kalshi** - Sports & events markets
- **Hugging Face** - AI sentiment models
- **Railway** - Cloud hosting
- **Reddit** - Social sentiment data

---

**Built with** 🤖 [Claude Code](https://claude.com/claude-code)

---

## 📚 Documentation

- [Railway Setup Guide](RAILWAY_SETUP_STEPS.md)
- [Custom Domain Setup](CUSTOM_DOMAIN_GUIDE.md)
- [Hostinger + Railway](HOSTINGER_RAILWAY_SETUP.md)
- [prediq.site DNS Setup](PREDIQ_SITE_DNS_SETUP.md)
- [Security Audit Report](SECURITY_AUDIT_REPORT.md)
- [Render Deployment](RENDER_DEPLOYMENT_GUIDE.md)
- [Hugging Face Deployment](HUGGINGFACE_DEPLOYMENT.md)

---

**Last Updated:** January 9, 2026
