# AI-Powered Mindshare Market Analyzer - Development Prompt

## Introduction

This document contains a comprehensive, self-contained prompt designed to instruct an AI model (such as Grok, ChatGPT, Claude, or similar) to build a complete "AI-Powered Mindshare Market Analyzer" application. This prompt includes all necessary background research, technical specifications, and implementation guidance to enable the target AI to construct a functional Web3/dApp application that analyzes social sentiment, matches insights to prediction markets, and provides verifiable on-chain computations.

---

## MASTER PROMPT FOR TARGET AI

### Role Assignment

You are an expert full-stack developer AI with deep specialization in Web3 technologies, blockchain integration (specifically Base and Solana), AI/ML systems for sentiment analysis, API integrations for social media platforms, and decentralized application (dApp) development. Your expertise spans:

- **Backend Development**: Python (FastAPI, Flask, Django) and Node.js (Express, NestJS) for building robust APIs and data processing pipelines
- **Frontend Development**: React, Next.js, TypeScript, and modern UI frameworks (Tailwind CSS, Material-UI) for creating responsive, real-time dashboards
- **Blockchain Technologies**: Solana Web3.js, Ethereum/Base Web3.js, smart contract interactions, wallet integrations (MetaMask, Phantom), and understanding of Layer 2 scaling solutions
- **AI/ML Systems**: Natural Language Processing (NLP), sentiment analysis using transformers (Hugging Face), topic modeling, semantic similarity matching, and integration with third-party AI APIs
- **Data Engineering**: Real-time data streaming, WebSocket implementations, ETL pipelines, database design (PostgreSQL, MongoDB, Redis for caching)
- **Cryptographic Systems**: Zero-Knowledge Proofs (ZK-SNARKs, ZK-STARKs), verifiable computation frameworks, cryptographic proof generation and validation
- **DevOps**: Docker containerization, CI/CD pipelines, cloud deployment (Vercel, AWS, Google Cloud), monitoring and logging systems

You have a comprehensive understanding of prediction markets, decentralized finance (DeFi), and the emerging field of verifiable AI computations. You are tasked with building a production-ready application that bridges Web2 social data with Web3 prediction markets through verifiable AI analysis.

---

### Project Goal

**Primary Objective**: Build a comprehensive "AI-Powered Mindshare Market Analyzer" that serves as a decision-support tool for traders, researchers, and analysts interested in prediction markets. This application will:

1. **Aggregate and Analyze Social Data**: Continuously monitor and analyze sentiment, mindshare (attention metrics), and narrative trends from major social platforms including X (formerly Twitter) and Reddit, focusing on topics relevant to prediction markets (politics, culture, cryptocurrency, sports, technology, current events).

2. **Integrate AI-Powered Analysis**: Leverage Kaito AI's verifiable mindshare analysis platform (or build custom AI models if Kaito integration is not feasible) to process unstructured social data, extract sentiment signals, identify trending narratives, and quantify attention metrics that correlate with market movements.

3. **Match Insights to Prediction Markets**: Semantically map analyzed social insights to relevant prediction markets on two major platforms:
   - **Kalshi**: CFTC-regulated US prediction market for events (politics, culture, sports, crypto, weather)
   - **Polymarket**: Decentralized prediction market on Polygon covering politics, culture, news, sports, technology

4. **Predict Market Shifts**: Develop predictive algorithms that correlate sentiment trends with potential market movements (price changes, odds shifts) by analyzing historical patterns, volume changes, sentiment velocity, and cross-platform sentiment divergence.

5. **Provide Verifiable On-Chain Proofs**: Implement cryptographic verification systems on Base (Ethereum L2 via Coinbase) and Solana blockchains to create tamper-proof, auditable records of AI analysis results, ensuring trustlessness and transparency through Zero-Knowledge Proofs and verifiable computation frameworks.

6. **Deliver Actionable Insights**: Present data through an intuitive, real-time dashboard with:
   - Live sentiment scores and mindshare metrics
   - Matched prediction markets with current odds/prices
   - Predicted market shift probabilities
   - Real-time alerts for significant sentiment changes
   - Direct clickable links to trade on Kalshi and Polymarket
   - Historical performance tracking of predictions
   - Data export capabilities for research purposes

**Real-World Usability**: The application must be production-ready, handling real-time data streams, providing low-latency responses, and serving as a reliable tool for making informed decisions in prediction markets. It should be valuable for day traders seeking alpha, researchers studying sentiment-market correlations, and institutions analyzing public opinion trends.

---

### Background Research and Context

To ensure you have comprehensive knowledge for building this application, the following research has been compiled covering the key technologies and platforms:

#### 1. Kaito AI - Verifiable Mindshare Analysis Platform

**Overview**: Kaito is a cutting-edge AI-powered Web3 platform launched to address the challenge of analyzing vast amounts of unstructured data in the cryptocurrency and prediction market ecosystems. The platform aggregates data from diverse sources including:
- Social media platforms (X/Twitter, Reddit, Discord, Telegram)
- Governance forums and DAOs
- Podcasts and audio content
- Research papers and technical documentation
- News articles and blog posts

**Core Technology**: Kaito measures "mindshare," which quantifies the share of attention and sentiment that specific topics, tokens, narratives, or events receive across the information landscape. This is accomplished through:
- Advanced AI models trained on Web3-specific language and contexts
- Real-time indexing and processing of millions of data points daily
- Proprietary sentiment analysis algorithms calibrated for crypto/prediction market terminology
- Network analysis to identify influencers and information cascades

**Key Features**:
- **Real-Time Search**: Query any ticker symbol, topic, or emerging narrative to get instant sentiment and attention metrics
- **AI Agents**: Automated analysis systems that combine on-chain data, market data, and social sentiment to generate trading signals and insights
- **Mindshare Indices**: Quantitative metrics showing relative attention levels across different assets, topics, or events over time
- **Narrative Tracking**: Identification and monitoring of emerging narratives before they reach mainstream awareness
- **Yaps Token System**: Gamification layer that tokenizes attention through "Yaps" points, rewarding users for quality contributions
- **KAITO Token**: Native cryptocurrency token used for ecosystem rewards, governance, and accessing premium features

**Verifiable AI Innovation (November 2025)**: In a groundbreaking development, Kaito partnered with Polymarket to launch the world's first "verifiable mindshare markets." This innovation addresses a critical challenge in AI systems: opacity and lack of trust. The partnership leverages:
- **EigenCloud's EigenAI**: A platform for verifiable off-chain computations that uses cryptographic proofs to ensure AI inferences are tamper-proof and reproducible
- **Brevis_zk**: Zero-Knowledge proof infrastructure that validates AI outputs without revealing underlying data or model internals
- **On-Chain Proof Anchoring**: Results are cryptographically committed to blockchain, creating an immutable audit trail

This makes Kaito's AI outputs trustless—users can verify that sentiment scores and mindshare metrics were computed correctly without needing to trust Kaito as an intermediary. This transforms prediction markets from relying on opaque "black box" AI to using verifiable, transparent AI systems.

**Market Expansion**: According to team communications on X (@KaitoAI), they emphasize this as creating an entirely new market category: "predicting mindshare on anything." Initial markets focus on cryptocurrency sentiment, but expansion is planned to cover political figures, cultural trends, technology adoption, and more.

**API Access**: Kaito provides a developer API portal at https://www.kaito.ai/portal with endpoints for:
- Fetching real-time sentiment scores for topics/tokens
- Retrieving mindshare indices and historical trends
- Accessing AI-driven narrative analysis
- Integrating verifiable computation proofs
- Webhook subscriptions for real-time alerts

**Integration Strategy**: Your application should integrate Kaito's API as the primary AI analysis engine if possible, using their verified mindshare data. If API access is limited or costs are prohibitive, you should build a custom AI pipeline that mimics Kaito's approach using open-source NLP models and social data APIs.

#### 2. Kalshi - CFTC-Regulated US Prediction Markets

**Overview**: Kalshi is the first CFTC-regulated exchange in the United States that allows trading on event outcomes. Founded to democratize access to event markets, Kalshi offers legally compliant prediction markets for US users, covering:
- **Politics**: Elections, legislation outcomes, approval ratings, political events
- **Culture**: Entertainment awards, celebrity events, social trends
- **Sports**: Game outcomes, championships, player performances
- **Cryptocurrency**: Price levels, adoption metrics, regulatory decisions
- **Weather**: Temperature ranges, precipitation, seasonal patterns
- **Economics**: Inflation data, GDP figures, employment statistics

**Regulatory Advantage**: As a CFTC-regulated entity, Kalshi operates with legal clarity in the US market, offering:
- Fiat currency deposits and withdrawals (USD)
- Full KYC/AML compliance
- Institutional-grade security and custody
- Legal enforceability of contracts
- Tax reporting (1099 forms for US users)

**Public API**: Kalshi provides a comprehensive REST API documented at https://docs.kalshi.com with key endpoints including:
- **GET /markets**: List all available markets with filtering by category, status, date
- **GET /markets/{market_id}**: Retrieve detailed information about a specific market including current prices, volume, open interest, historical data
- **GET /markets/{market_id}/orderbook**: Access order book data for liquidity analysis
- **WebSocket API**: Real-time streaming of price updates, trades, and market events
- **Authentication**: API key-based authentication for user-specific operations

**Developer Ecosystem**: Kalshi actively encourages third-party development through:
- **Builder Grants**: Over $2 million allocated to developers building on Kalshi's API (applications at https://kalshi.com/builders)
- **Builder Codes**: Revenue-sharing program where developers earn based on trading volume generated through their applications
- **Technical Support**: Dedicated developer relations team and community
- **Educational Resources**: Code examples, tutorials, and best practices documentation

**Blockchain Integration**: In 2024-2025, Kalshi partnered with Solana ecosystem projects to enable:
- **Tokenized Markets**: On-chain representations of Kalshi markets on Solana
- **DeFi Integration**: Partnerships with DFlow (decentralized orderflow), Jupiter Exchange (DEX aggregator), and Phantom Wallet
- **Crypto Deposits**: Support for cryptocurrency funding alongside traditional fiat
- **Cross-Chain Bridges**: Potential for multi-chain expansion

**AI Agent Ecosystem**: According to team posts on X (@Kalshi, @KalshiEco), Kalshi is fostering an ecosystem of AI-powered trading agents that:
- Monitor social sentiment and correlate with market movements
- Execute automated trading strategies based on external data signals
- Provide real-time alerts for market opportunities
- Generate research reports combining on-chain, market, and sentiment data

**Integration Strategy**: Your application should use Kalshi's public API to fetch market data, current prices/odds, and match them with sentiment insights. Implement WebSocket connections for real-time price tracking to detect sentiment-driven shifts.

#### 3. Polymarket - Decentralized Prediction Markets

**Overview**: Polymarket is the world's largest decentralized prediction market platform, operating on Polygon (an Ethereum Layer 2 scaling solution) with bridges to other blockchains. Polymarket has gained significant traction for:
- **Decentralization**: Non-custodial trading using smart contracts
- **Global Access**: Available to users worldwide (with some regional restrictions)
- **Market Breadth**: Comprehensive coverage of politics, culture, news, sports, technology, and current events
- **Trading Volume**: Billions of dollars in cumulative trading volume
- **Accuracy**: Historical 94% accuracy in aggregating crowd wisdom for event predictions

**Technical Architecture**:
- **Polygon Blockchain**: Primary settlement layer for low fees and fast transactions
- **USDC Liquidity**: Markets denominated in USDC stablecoin
- **Automated Market Maker (AMM)**: Liquidity provision through algorithmic pricing
- **Order Book Hybrid**: Combines AMM with off-chain order matching for efficiency
- **Cross-Chain Bridges**: Support for assets from Ethereum, other L2s

**GraphQL API**: Polymarket provides a modern GraphQL API (Gamma Markets API) documented at https://docs.polymarket.com/developers/gamma-markets-api/overview offering:
- **Market Queries**: Fetch markets by category, event, date range, or search terms
- **Event Data**: Retrieve event details, resolution criteria, and metadata
- **Price/Probability Data**: Current token prices representing market probabilities
- **Historical Data**: Time-series price data for backtesting and analysis
- **Real-Time Subscriptions**: GraphQL subscriptions for live price updates
- **Trader Statistics**: Volume, positions, and performance metrics

**Developer Ecosystem**: Polymarket incentivizes builders through:
- **Builder Programs**: Grants and accelerator programs for developers
- **Fee Sharing**: Revenue share for applications that drive volume
- **Relayer Support**: Infrastructure support for building custom trading interfaces
- **Liquidity Rewards**: Incentives for market makers and liquidity providers
- **Documentation Hub**: Comprehensive guides at https://docs.polymarket.com/developers/rewards/overview

**Strategic Partnerships**:
- **MetaMask**: Wallet integration for seamless trading
- **NYSE/ICE Investment**: Institutional backing from Intercontinental Exchange
- **Kaito AI Partnership (2025)**: Verifiable mindshare markets using ZK proofs (as detailed in Kaito section)
- **Media Integrations**: Data partnerships with Bloomberg, FiveThirtyEight, and research institutions

**AI Integration Examples**: According to team posts on X (@Polymarket):
- **Grok 4 Integration**: xAI's Grok 4 model trained on Polymarket historical data to provide trading insights and market analysis
- **AI Topic Markets**: New markets specifically on AI-related events (e.g., "Will there be a federal moratorium on AI data centers in 2025?")
- **Predictive Analytics**: Third-party tools using Polymarket data for arbitrage and alpha generation

**Verifiable Mindshare Markets**: The Kaito-Polymarket partnership (announced November 2025) creates markets where outcomes are determined by verifiable AI analysis of social sentiment, with:
- **ZK Proofs**: On-chain verification that sentiment calculations are correct
- **Trustless Resolution**: Market resolution based on cryptographically proven data
- **Transparency**: Full auditability of how sentiment is measured and markets are settled

**Integration Strategy**: Your application should use Polymarket's GraphQL API to query relevant markets, subscribe to real-time price updates, and display current probabilities alongside sentiment data. Implement deep linking to Polymarket's trading interface for frictionless user experience.

#### 4. Mindshare Analysis and Social Data Sources

**Definition of Mindshare**: In the context of this project, "mindshare" refers to the quantitative share of attention, conversation volume, and sentiment that a particular topic, entity, or narrative receives across social media and information platforms. It differs from simple mention counts by weighting for:
- **Sentiment Intensity**: Strongly positive or negative opinions carry more weight
- **Influencer Amplification**: Content from high-follower accounts has greater impact
- **Engagement Velocity**: Rapidly accelerating conversations signal emerging trends
- **Cross-Platform Consistency**: Topics trending across multiple platforms indicate stronger signals

**Primary Data Sources**:

1. **X (formerly Twitter)**:
   - **Relevance**: Real-time pulse of public opinion, especially for politics, crypto, and cultural events
   - **API Access**: X API v2 provides endpoints for searching tweets, streaming, and user data
   - **Python Library**: Tweepy is the standard library for X API integration
   - **Data Points**: Tweet text, timestamps, engagement metrics (likes, retweets, replies), user metadata, hashtags, geolocation
   - **Rate Limits**: Free tier is highly restrictive; paid tiers required for production use
   - **Challenges**: API costs, bot detection, spam filtering, sarcasm detection

2. **Reddit**:
   - **Relevance**: In-depth discussions, niche community sentiment, long-form analysis
   - **API Access**: Reddit API provides endpoints for posts, comments, subreddit data
   - **Python Library**: PRAW (Python Reddit API Wrapper) is the standard integration tool
   - **Data Points**: Post titles/content, comments, upvotes/downvotes, awards, subreddit classification, user karma
   - **Rate Limits**: Generally more permissive than X, but still require compliance with API terms
   - **Challenges**: Detecting irony, community-specific jargon, nested comment analysis

3. **Alternative Sources** (for enhanced coverage):
   - Discord: Community-specific discussions, requires bot integration
   - Telegram: Crypto communities, signal channels
   - News Aggregators: Google News, NewsAPI for mainstream media sentiment
   - Podcasts: Transcription and analysis of audio content (as Kaito does)

**AI/NLP Processing Pipeline**:

1. **Data Collection**: Use APIs to fetch relevant posts/tweets based on keywords, hashtags, or entities related to prediction market topics
2. **Preprocessing**: Clean text, remove spam, filter bots, normalize language
3. **Sentiment Analysis**:
   - Use pre-trained transformer models from Hugging Face (e.g., DistilBERT, RoBERTa fine-tuned for sentiment)
   - Custom models trained on prediction market-relevant data
   - Multi-class sentiment: Positive, Negative, Neutral, or numerical scores (-1 to +1)
4. **Topic Modeling**: LDA, BERTopic, or semantic clustering to identify themes and narratives
5. **Entity Recognition**: NER to extract mentions of candidates, companies, events, tokens
6. **Semantic Matching**: Use sentence transformers (SBERT) to compute similarity between social content and prediction market descriptions
7. **Aggregation**: Time-windowed aggregation (hourly, daily) to compute mindshare scores and trend direction

**Existing Tools and Precedents**:

- **PredictionlyAI** (launched December 2025): According to Reddit discussions (https://www.reddit.com/r/SaaS/comments/1prlfg3/launched_predictionlyai_realtime_arbitrage/), this tool analyzes sentiment from 36 different sources (including X and Reddit) and compares against Kalshi and Polymarket odds to identify arbitrage opportunities. It demonstrates the viability of sentiment-based prediction market analysis.

- **Google Finance AI Integration** (November 2025): Google integrated Kalshi and Polymarket data into its AI-powered finance tools, using sentiment analysis to provide predictions on event markets. This validates the commercial interest in sentiment-driven market analysis.

- **Academic Research**: Studies show correlation between social media sentiment velocity and prediction market movements, particularly for political events (elections, referendums) and cryptocurrency price predictions.

**Correlation with Market Movements**: Research and empirical observation suggest:
- **Leading Indicators**: Sentiment shifts often precede market price movements by hours to days
- **Volume Amplification**: High social volume + strong sentiment = more likely market impact
- **Cross-Platform Validation**: Sentiment agreement between X and Reddit is stronger signal than single-platform trends
- **Influencer Impact**: Sentiment from high-follower accounts correlates with larger market movements
- **False Signals**: Bot activity, coordinated campaigns, and ephemeral trends create noise requiring filtering

**Implementation Approach**: Build a robust data pipeline that fetches social data every 5-15 minutes, processes it through NLP models, computes mindshare scores, and stores time-series data for trend analysis. Use this as the foundation for matching to markets and predicting shifts.

#### 5. Verifiable Computations on Base and Solana

**The Problem**: Traditional AI and data analysis systems are "black boxes"—users cannot verify that computations were performed correctly without trusting the service provider. In prediction markets, where trust and accuracy are paramount, this opacity creates:
- **Manipulation Risk**: Operators could falsify sentiment scores to influence markets
- **Lack of Auditability**: No way to independently verify analysis results
- **Regulatory Concerns**: Difficulty demonstrating fairness to regulators
- **User Skepticism**: Traders hesitant to rely on unverifiable AI outputs

**The Solution**: Verifiable computation using cryptographic proofs allows off-chain AI analysis to be verified on-chain, creating trustless systems where:
- AI computations are performed off-chain (for efficiency and privacy)
- Cryptographic proofs are generated demonstrating correctness
- Proofs are validated on-chain by smart contracts
- Results are permanently recorded on blockchain for auditability
- Anyone can verify outputs without re-running expensive computations

**Implementation on Solana**:

Solana is a high-performance blockchain known for:
- **High Throughput**: ~65,000 transactions per second
- **Low Costs**: Fraction of a cent per transaction
- **Fast Finality**: Sub-second confirmation times
- **Developer Ecosystem**: Rust-based programming, extensive tooling

**Verifiable Compute Frameworks on Solana**:

1. **Bonsol** (ZK Co-Processor):
   - Zero-Knowledge co-processor enabling verifiable off-chain execution
   - Allows complex computations (like AI inference) to run off-chain with on-chain proof verification
   - Integration via Solana programs that verify ZK proofs
   - Documentation and examples available in Solana ecosystem repos

2. **Brevis_zk** (Zero-Knowledge Proof Infrastructure):
   - As used in Kaito-Polymarket partnership
   - Generates ZK-SNARKs or ZK-STARKs for data processing
   - Validates proofs on-chain without revealing computation details
   - Enables privacy-preserving verifiable AI

3. **Proof of History (PoH)**:
   - Solana's native timestamping mechanism
   - Can anchor sentiment analysis timestamps to create immutable historical records
   - Proves when data was processed (critical for "prediction" vs "postdiction" distinction)

**Implementation Pattern for Solana**:
1. Perform sentiment analysis off-chain using your AI pipeline
2. Generate cryptographic commitment to input data (hash of social media posts)
3. Compute sentiment score and generate ZK proof of correct computation
4. Submit proof + result to Solana program
5. On-chain program verifies proof validity
6. If valid, result is stored on-chain with timestamp
7. Users can query on-chain records to see verifiable sentiment history

**Kalshi-Solana Integration**: Leverage Kalshi's tokenized markets on Solana for seamless integration of verifiable sentiment with on-chain market contracts.

**Resources**:
- Solana ZK Documentation: https://www.helius.dev/blog/zero-knowledge-proofs-its-applications-on-solana
- On-Chain Randomness Examples: https://adevarlabs.com/blog/on-chain-randomness-on-solana-predictability-manipulation-safer-alternatives-part-1

**Implementation on Base (Ethereum L2)**:

Base is:
- **Ethereum Layer 2**: Built on Optimism stack (Optimistic Rollup)
- **Coinbase-Backed**: Institutional grade infrastructure
- **EVM-Compatible**: Easy migration of Ethereum contracts and tools
- **Growing Ecosystem**: DeFi, NFTs, social applications

**Verifiable Compute Frameworks on Base**:

1. **EigenLayer/EigenCloud**:
   - As detailed in Delphi Digital research (https://members.delphidigital.io/reports/the-verifiable-cloud-how-eigencloud-is-unlocking-cryptos-app-and-ai-era)
   - Platform for verifiable off-chain computations with cryptographic proofs
   - "Verifiable Cloud" concept: Heavy computations run off-chain, verified on-chain
   - Used in Kaito's verifiable AI implementation
   - Integration via smart contracts that validate EigenLayer proofs

2. **ZK Rollup Infrastructure**:
   - Base inherits Optimism's fraud-proof security
   - Can integrate ZK-proof systems for additional verification layers
   - Libraries like Circom, SnarkJS for custom ZK circuits

3. **EigenAI** (from EigenCloud):
   - Specifically designed for verifiable AI inferences
   - Allows AI models to run off-chain with on-chain proof validation
   - Perfect for sentiment analysis use case

**Implementation Pattern for Base**:
1. Deploy smart contract on Base for storing verified sentiment results
2. Run AI sentiment analysis off-chain
3. Generate proof using EigenCloud/EigenAI framework
4. Submit proof to Base smart contract via transaction
5. Contract validates proof and emits event with sentiment data
6. Front-end listens to contract events for verified sentiment updates
7. Users can query contract to see immutable sentiment history

**Why Both Chains?**:
- **Diversification**: Multi-chain approach reduces single-point-of-failure risk
- **Market Integration**: Kalshi has Solana integration; Polymarket on Polygon (can bridge to Base/Ethereum)
- **Performance Trade-offs**: Solana for high-frequency updates; Base for Ethereum ecosystem compatibility
- **Developer Experience**: Showcase ability to work across different blockchain paradigms

**Simplified MVP Approach**: If full ZK implementation is too complex for initial version, implement:
- **Commit-Reveal Scheme**: Commit hash of sentiment data before market movements, reveal later to prove no post-hoc manipulation
- **Data Anchoring**: Store hashes of analysis results on-chain with timestamps
- **Proof-of-Existence**: Demonstrate when analysis was performed, building toward full ZK in v2

**Resources**:
- EigenCloud Overview: https://members.delphidigital.io/reports/the-verifiable-cloud-how-eigencloud-is-unlocking-cryptos-app-and-ai-era
- Base vs Solana Comparison: https://franciscodex.substack.com/p/base-vs-solana-2025

#### 6. Market Matching and Prediction Logic

**Semantic Matching Challenge**: Social media discussions use natural language, slang, abbreviations, and context-dependent terminology, while prediction markets have formal titles and descriptions. Your system must bridge this gap by:

**Natural Language Processing Techniques**:

1. **Keyword Extraction**:
   - Extract key entities (people, organizations, events, dates) from social posts
   - Extract key entities from market titles and descriptions
   - Match based on entity overlap

2. **Semantic Similarity**:
   - Use sentence transformers (e.g., Sentence-BERT) to encode social content and market descriptions into vector embeddings
   - Compute cosine similarity between social content vectors and market vectors
   - Match social content to markets with highest similarity scores (e.g., > 0.7 threshold)

3. **Topic Modeling**:
   - Cluster social media posts into topics using BERTopic or LDA
   - Manually or automatically label topics
   - Match topics to market categories (politics, crypto, sports, etc.)

4. **Rule-Based Matching**:
   - Create mapping rules for common scenarios:
     - "Trump" mentions → Presidential election markets, political figure markets
     - "Bitcoin", "BTC" → Cryptocurrency price level markets
     - "Super Bowl", "NFL" → Sports championship markets
   - Combine rules with ML-based matching for robustness

**Example Matching Scenarios**:

- Social Data: "Reddit sentiment on r/politics shows 80% negative sentiment toward proposed crypto regulation bill"
- Matched Markets:
  - Kalshi: "Will Congress pass crypto regulation by Q2 2026?"
  - Polymarket: "US Crypto Regulation Bill Passage"

- Social Data: "X trending: #Election2026 with 45% positive sentiment for Candidate A, 30% for Candidate B"
- Matched Markets:
  - Kalshi: "Will Candidate A win 2026 Senate race in State X?"
  - Polymarket: "2026 Midterm Elections - Senate Control"

**Prediction Logic**: Once matched, predict market shifts by:

1. **Sentiment-Price Correlation**:
   - Hypothesis: Positive sentiment increase → higher probability for "Yes" outcome
   - Compute sentiment change (delta) over time windows (1hr, 6hr, 24hr)
   - Compare with historical sentiment-price correlations
   - Predict probability shift magnitude

2. **Volume-Volatility Analysis**:
   - High social media volume + strong sentiment → higher confidence in prediction
   - Low volume = potential noise, lower confidence
   - Use statistical significance testing (t-tests, z-scores)

3. **Cross-Platform Validation**:
   - If X and Reddit sentiment align → strong signal, higher predicted shift
   - If sentiment diverges → weak signal, lower predicted shift or flag as uncertain

4. **Velocity Metrics**:
   - Sentiment acceleration (rate of change of sentiment) can predict near-term price movements
   - Sudden sentiment spikes often precede short-term volatility

5. **Machine Learning Models** (advanced):
   - Train regression models (XGBoost, neural networks) on historical data:
     - Input features: Sentiment score, volume, velocity, cross-platform agreement, time of day, market liquidity
     - Output: Predicted price change in next 1hr, 6hr, 24hr
   - Backtest on historical data to validate
   - Implement live prediction with confidence intervals

**Probability Calculation Standards**:
- **Polymarket**: Token prices directly represent implied probability (e.g., 0.65 USDC price = 65% probability)
- **Kalshi**: Contracts priced in cents; divide by 100 for probability (e.g., 73 cents = 73% probability)
- Ensure your system normalizes both to percentage probabilities for comparison

**Output Format**: For each matched market, provide:
- Current market probability (%)
- Current sentiment score and trend
- Predicted probability shift (e.g., "+5% likely in next 6 hours")
- Confidence level (high/medium/low based on signal strength)
- Reasoning (e.g., "Positive Reddit sentiment increased 25% in last hour with 3x volume")

---

### Key Features - Detailed Requirements

Your AI-Powered Mindshare Market Analyzer must implement the following features with production-grade quality:

#### Feature 1: Social Data Ingestion and Processing

**Requirements**:
- Implement automated data collection from X (Twitter) and Reddit APIs
- Schedule periodic fetching (every 5-15 minutes) to maintain real-time data freshness
- Support keyword-based filtering for topics relevant to active prediction markets
- Store raw social media data in database with timestamps for historical analysis
- Implement retry logic and error handling for API rate limits and failures
- Support incremental data fetching to avoid duplicate processing
- Anonymize user data to protect privacy (remove/hash usernames if storing)

**Technical Specifications**:
- **X Integration**: Use Tweepy library with X API v2, implement bearer token authentication, search recent tweets endpoint, filter by keywords/hashtags
- **Reddit Integration**: Use PRAW library with OAuth2, fetch posts/comments from relevant subreddits (e.g., r/politics, r/cryptocurrency, r/sports), filter by keywords and recency
- **Data Schema**: Store post ID, text content, timestamp, author metadata (follower count, verification status), engagement metrics (likes, shares, comments), source platform, associated market IDs (after matching)
- **Rate Limit Handling**: Implement exponential backoff, request queuing, token bucket algorithm for rate limiting compliance
- **Data Quality**: Filter spam, bots (check for automated posting patterns), duplicates, low-quality content (very short posts, excessive emojis)

**Deliverables**:
- Python/Node.js module for data collection
- Database schema for storing social data
- Configuration file for API credentials (use environment variables, never hardcode)
- Logging and monitoring for data pipeline health

#### Feature 2: AI-Powered Sentiment and Mindshare Analysis

**Requirements**:
- Integrate Kaito AI API (preferred) or build custom NLP pipeline for sentiment analysis
- Compute sentiment scores (-1 to +1 scale, or negative/neutral/positive classification) for each post/tweet
- Aggregate sentiment by time windows (hourly, daily) for trend analysis
- Calculate mindshare metrics: volume of mentions, share of voice, engagement-weighted attention
- Identify trending narratives and topics using topic modeling
- Extract key entities (people, organizations, events) using Named Entity Recognition
- Compute sentiment velocity (rate of change) and acceleration

**Technical Specifications**:

**Option A - Kaito Integration**:
- Register for Kaito API access at https://www.kaito.ai/portal
- Implement authentication using API keys
- Query sentiment scores and mindshare indices for topics/entities
- Fetch verifiable computation proofs if available
- Cache results to minimize API costs

**Option B - Custom NLP Pipeline**:
- Use Hugging Face Transformers library
- Load pre-trained sentiment model: `distilbert-base-uncased-finetuned-sst-2-english` or `cardiffnlp/twitter-roberta-base-sentiment`
- For crypto/prediction market specific: Fine-tune on domain-specific labeled dataset if available
- Batch processing for efficiency (process multiple posts in single inference)
- Use sentence transformers (e.g., `all-MiniLM-L6-v2`) for semantic similarity computations
- Implement topic modeling with BERTopic or Latent Dirichlet Allocation (LDA)
- Use spaCy or Hugging Face NER models for entity extraction

**Mindshare Calculation Formula** (if building custom):
```
Mindshare Score = (
    0.4 * NormalizedMentionVolume +
    0.3 * WeightedSentiment +
    0.2 * EngagementRate +
    0.1 * InfluencerAmplification
)
```

Where:
- NormalizedMentionVolume = (current mentions / historical average) normalized 0-1
- WeightedSentiment = average sentiment score weighted by engagement
- EngagementRate = (likes + shares + comments) / total posts
- InfluencerAmplification = bonus for high-follower account mentions

**Deliverables**:
- AI analysis module with clear API interface
- Sentiment scoring function with confidence scores
- Mindshare aggregation function with time-series output
- Unit tests with sample social media data
- Documentation of model selection and performance metrics

#### Feature 3: Prediction Market Integration and Matching

**Requirements**:
- Integrate with Kalshi REST API and WebSocket for market data
- Integrate with Polymarket GraphQL API and subscriptions for market data
- Fetch all active markets on application startup and refresh periodically
- Implement semantic matching algorithm to connect social insights with relevant markets
- Store matched market data with current prices/odds
- Subscribe to real-time price updates for matched markets
- Provide manual override capability for users to specify custom matches

**Technical Specifications**:

**Kalshi Integration**:
- Base URL: `https://api.kalshi.com/trade-api/v2`
- Authentication: API key in headers (requires Kalshi account)
- Key Endpoints:
  - `GET /markets` - List markets with filters (category, status)
  - `GET /markets/{market_ticker}` - Get specific market details, current price, volume
  - `GET /markets/{market_ticker}/history` - Historical price data
  - WebSocket: `wss://api.kalshi.com/trade-api/ws/v2` for real-time updates
- Parse response: Extract ticker, title, description, current Yes price (in cents), volume, close_time
- Store: Market ID, title, category, current probability (price/100), last update timestamp

**Polymarket Integration**:
- API URL: `https://gamma-api.polymarket.com/`
- GraphQL endpoint: `/query`
- Key Queries:
  ```graphql
  query Markets {
    markets(limit: 100, active: true) {
      id
      question
      description
      outcomes
      outcomePrices
      volume
      endDate
    }
  }
  ```
- Subscription:
  ```graphql
  subscription MarketUpdates($marketId: ID!) {
    marketUpdated(id: $marketId) {
      id
      outcomePrices
      timestamp
    }
  }
  ```
- Parse response: Extract market ID, question, outcome prices (array of probabilities), volume
- Calculate probability: outcomePrices already in 0-1 range, convert to percentage

**Semantic Matching Algorithm**:
1. Preprocess: Clean market titles/descriptions and social content (lowercase, remove punctuation)
2. Entity Extraction: Extract named entities from both sources
3. Keyword Overlap: Calculate Jaccard similarity of keywords
4. Semantic Similarity:
   - Encode market descriptions using sentence transformer
   - Encode aggregated social content clusters
   - Compute cosine similarity
   - Match if similarity > 0.65 threshold
5. Category Filtering: Only match social content to markets in relevant categories (e.g., crypto social data to crypto markets)
6. Manual Rules: Implement hardcoded matches for high-priority markets (e.g., major elections)
7. Store Matches: Save social_topic_id → market_id mappings in database

**Deliverables**:
- Market data fetching modules for Kalshi and Polymarket
- WebSocket/subscription handlers for real-time updates
- Semantic matching service with configurable thresholds
- Database schema for markets and matches
- API endpoints to view matched markets and override matches

#### Feature 4: Market Shift Prediction Engine

**Requirements**:
- Analyze correlation between sentiment changes and market price movements
- Generate predictions for probability shifts in matched markets
- Provide confidence levels for predictions based on signal strength
- Support multiple time horizons (1 hour, 6 hours, 24 hours)
- Track prediction accuracy for continuous improvement
- Display reasoning/explanation for each prediction

**Technical Specifications**:

**Prediction Algorithm** (Rule-Based MVP):
```python
def predict_market_shift(sentiment_data, market_data, time_horizon='6h'):
    # Calculate sentiment delta
    current_sentiment = sentiment_data['current_score']
    previous_sentiment = sentiment_data['previous_score']  # from time_horizon ago
    sentiment_delta = current_sentiment - previous_sentiment

    # Calculate volume factor
    current_volume = sentiment_data['mention_count']
    avg_volume = sentiment_data['historical_avg_volume']
    volume_factor = min(current_volume / avg_volume, 2.0)  # cap at 2x

    # Calculate cross-platform agreement
    platforms = ['twitter', 'reddit']
    sentiments = [sentiment_data[p]['score'] for p in platforms if p in sentiment_data]
    agreement = 1 - np.std(sentiments) if len(sentiments) > 1 else 0.5

    # Prediction formula
    base_shift = sentiment_delta * 10  # scale factor (e.g., 0.1 sentiment change = 1% prob shift)
    adjusted_shift = base_shift * volume_factor * agreement

    # Confidence calculation
    confidence = min(volume_factor * agreement, 1.0)
    confidence_level = 'high' if confidence > 0.7 else 'medium' if confidence > 0.4 else 'low'

    return {
        'predicted_shift': round(adjusted_shift, 2),  # percentage points
        'confidence': confidence_level,
        'reasoning': f"Sentiment changed {sentiment_delta:+.2f} with {volume_factor:.1f}x volume and {agreement:.0%} cross-platform agreement"
    }
```

**Machine Learning Enhancement** (Advanced):
- Collect historical data: [sentiment_score, volume, velocity, platform_agreement, time_of_day] → [actual_price_change_6h]
- Train regression model (XGBoost, Random Forest, or neural network)
- Features: Current sentiment, sentiment delta (1h, 6h, 24h), volume, velocity, cross-platform agreement, market liquidity, time to market close
- Target: Price change in next time horizon
- Validation: 80/20 train/test split, evaluate RMSE and MAE
- Deploy: Serve model predictions alongside rule-based predictions

**Accuracy Tracking**:
- Store predictions with timestamp
- After time horizon elapses, compare predicted shift with actual market price change
- Calculate metrics: Mean Absolute Error (MAE), Root Mean Square Error (RMSE), direction accuracy (% correct on up/down)
- Display on dashboard: "Prediction accuracy (24h): 68% directionally correct, MAE: 3.2%"

**Deliverables**:
- Prediction engine module with documented algorithm
- Historical data collection for backtesting
- Accuracy tracking service
- API endpoints to fetch predictions for markets
- Explanation generation for transparency

#### Feature 5: Verifiable On-Chain Computation Proofs

**Requirements**:
- Implement cryptographic proofs for sentiment analysis results on Base (Ethereum L2)
- Implement cryptographic proofs for sentiment analysis results on Solana
- Generate proofs for each analysis run (hourly or per-update)
- Submit proofs to blockchain for on-chain verification
- Provide public interface for users to verify historical analysis
- Display verification status on dashboard

**Technical Specifications**:

**Base Implementation** (using EigenLayer/commit-reveal):

1. **Smart Contract** (Solidity):
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SentimentOracle {
    struct SentimentRecord {
        bytes32 dataHash;      // Hash of input data
        int256 sentimentScore; // Score (-100 to +100)
        uint256 timestamp;
        address submitter;
        bool verified;
    }

    mapping(bytes32 => SentimentRecord) public records;

    event SentimentSubmitted(bytes32 indexed recordId, int256 score, uint256 timestamp);

    function submitSentiment(
        bytes32 recordId,
        bytes32 dataHash,
        int256 sentimentScore,
        bytes calldata proof  // ZK proof or signature
    ) external {
        // Verify proof (simplified - integrate EigenLayer verification)
        require(verifyProof(proof, dataHash, sentimentScore), "Invalid proof");

        records[recordId] = SentimentRecord({
            dataHash: dataHash,
            sentimentScore: sentimentScore,
            timestamp: block.timestamp,
            submitter: msg.sender,
            verified: true
        });

        emit SentimentSubmitted(recordId, sentimentScore, block.timestamp);
    }

    function verifyProof(bytes calldata proof, bytes32 dataHash, int256 score)
        internal pure returns (bool) {
        // Placeholder - integrate actual ZK verification or signature check
        return true;
    }
}
```

2. **Off-Chain Proof Generation**:
- After computing sentiment, create dataHash = keccak256(JSON of input posts)
- Generate proof (can start with simple signature, upgrade to ZK)
- Submit transaction to Base contract
- Listen for event confirmation

3. **Web3 Integration**:
- Use ethers.js or web3.js
- Connect to Base network (RPC: `https://mainnet.base.org`)
- Wallet: Use private key for automated submissions (secure with AWS KMS or similar)
- Gas management: Estimate gas, handle reorgs

**Solana Implementation** (using Proof-of-History anchoring):

1. **Solana Program** (Rust - simplified):
```rust
use anchor_lang::prelude::*;

#[program]
pub mod sentiment_oracle {
    use super::*;

    pub fn submit_sentiment(
        ctx: Context<SubmitSentiment>,
        data_hash: [u8; 32],
        sentiment_score: i16,
        proof: Vec<u8>
    ) -> Result<()> {
        let record = &mut ctx.accounts.sentiment_record;
        record.data_hash = data_hash;
        record.sentiment_score = sentiment_score;
        record.timestamp = Clock::get()?.unix_timestamp;
        record.verified = verify_proof(&proof, &data_hash, sentiment_score);
        Ok(())
    }
}

#[account]
pub struct SentimentRecord {
    pub data_hash: [u8; 32],
    pub sentiment_score: i16,
    pub timestamp: i64,
    pub verified: bool,
}
```

2. **Off-Chain Integration**:
- Use @solana/web3.js library
- Generate transaction with sentiment data
- Sign and submit to Solana
- Confirm via RPC polling

**MVP Simplification** (if full ZK is too complex):
- Use commit-reveal: First transaction commits hash, second reveals data
- Use digital signatures: Sign sentiment results with private key, verify on-chain
- Timestamp anchoring: Just store hash + timestamp on-chain to prove when analysis happened
- Upgrade to full ZK in later version

**Deliverables**:
- Smart contracts deployed on Base testnet and mainnet
- Solana program deployed on devnet and mainnet
- Off-chain proof generation service
- Web3 integration module for submitting proofs
- Public verification interface (web page showing on-chain records)
- Documentation on verification process for users

#### Feature 6: Real-Time Dashboard and User Interface

**Requirements**:
- Build responsive web dashboard accessible on desktop and mobile
- Display real-time sentiment scores and trends with charts
- Show matched prediction markets with current odds/prices
- Display market shift predictions with confidence levels
- Provide real-time alerts for significant sentiment changes or predicted shifts
- Include direct links to trade on Kalshi and Polymarket
- Show on-chain verification status for each analysis
- Support data export (CSV, JSON) for research purposes
- Implement user authentication for personalized watchlists (optional)

**Technical Specifications**:

**Frontend Stack**:
- **Framework**: React with TypeScript or Next.js (for SSR/SEO benefits)
- **UI Library**: Tailwind CSS for styling, shadcn/ui or Material-UI for components
- **Charts**: Recharts, Chart.js, or Plotly for time-series visualization
- **Real-Time Updates**: WebSocket connection to backend or Server-Sent Events (SSE)
- **State Management**: React Context API, Zustand, or Redux for complex state
- **Routing**: React Router or Next.js routing

**Dashboard Components**:

1. **Sentiment Overview Panel**:
   - Cards showing current sentiment for top topics (e.g., "2026 Election: +0.45 (Positive)")
   - Trend indicators (up/down arrows, percentage change from 24h ago)
   - Sparkline charts showing sentiment over last 7 days

2. **Market Matches Table**:
   - Columns: Market Title, Platform (Kalshi/Polymarket), Current Probability, Sentiment Score, Predicted Shift, Confidence, Trade Link
   - Sortable and filterable by category, platform, confidence
   - Color coding: Green for positive sentiment, red for negative, gray for neutral
   - Click row to expand details

3. **Detailed Market View**:
   - Full market description
   - Sentiment time-series chart (line graph)
   - Price/probability time-series chart (line graph, overlay with sentiment)
   - Prediction reasoning text
   - Social media sample posts (top 5 most engaged)
   - On-chain verification badge with link to blockchain explorer
   - "Trade Now" buttons linking to Kalshi/Polymarket market pages

4. **Alerts Panel**:
   - Real-time notifications: "Bitcoin sentiment jumped +15% in last hour! Matched markets may shift."
   - Alert history log
   - Customizable alert thresholds (e.g., notify if sentiment changes >10%)

5. **Verification Dashboard**:
   - List of recent on-chain proof submissions
   - Links to Base/Solana blockchain explorers
   - Verification status (pending, confirmed)
   - Public API for external verification

6. **Analytics/Research Tab**:
   - Historical prediction accuracy metrics
   - Downloadable datasets (sentiment time-series, market prices, prediction history)
   - Correlation analysis charts (sentiment vs. price)

**Real-Time Updates**:
- Backend WebSocket server pushes updates every 30-60 seconds
- Frontend connects on page load, listens for events: `sentiment_update`, `market_update`, `prediction_update`, `alert`
- Update UI components reactively without page refresh

**External Links**:
- Kalshi market: `https://kalshi.com/markets/{market_ticker}`
- Polymarket market: `https://polymarket.com/event/{event_slug}` (extract from API response)
- Base transaction: `https://basescan.org/tx/{tx_hash}`
- Solana transaction: `https://explorer.solana.com/tx/{tx_signature}`

**Responsive Design**:
- Desktop: Multi-column layout, detailed charts
- Tablet: Responsive grid, collapsible panels
- Mobile: Single column, tab navigation, simplified charts

**Deliverables**:
- Complete React/Next.js application
- Component library with storybook documentation
- WebSocket integration for real-time updates
- Responsive CSS with mobile-first approach
- Deployment on Vercel or similar platform
- User guide documentation

#### Feature 7: Alert System and Notifications

**Requirements**:
- Monitor sentiment changes and trigger alerts when thresholds exceeded
- Notify users of significant predicted market shifts
- Support multiple notification channels (in-app, email, webhook)
- Allow users to customize alert criteria
- Rate limiting to avoid alert fatigue
- Historical alert log

**Technical Specifications**:

**Alert Triggers**:
- Sentiment spike: >X% change in Y time window (e.g., >15% in 1 hour)
- Volume surge: Mention count >Zx historical average
- Prediction confidence: High-confidence prediction generated
- Market event: New market matched to tracked topic
- Verification: On-chain proof confirmed

**Notification Channels**:

1. **In-App**:
   - Toast notifications using react-toastify or similar
   - Badge counts on alert icon
   - Alert panel with unread indicators

2. **Email** (optional):
   - Use SendGrid, AWS SES, or Mailgun
   - Template: "Alert: Bitcoin sentiment surged +18% in last hour. Matched markets: [links]"
   - User preference: Immediate, digest (hourly/daily), or disabled

3. **Webhook** (for programmatic access):
   - User provides webhook URL
   - POST JSON payload with alert data
   - Useful for integrating with trading bots, Slack, Discord

**Implementation**:
- Background job (cron or event-driven) checks alert conditions every 1-5 minutes
- Query database for users with matching alert preferences
- Generate alert object: {type, severity, message, data, timestamp}
- Dispatch to notification services
- Store in database with user_id for history

**Rate Limiting**:
- Max 1 alert per topic per hour (configurable)
- Suppress duplicate alerts
- Priority system: High-confidence predictions get immediate alerts, low-confidence batched

**Deliverables**:
- Alert monitoring service
- Notification dispatch module
- Email templates
- Webhook documentation
- User settings UI for alert customization

#### Feature 8: Error Handling and Resilience

**Requirements**:
- Gracefully handle API failures (X, Reddit, Kalshi, Polymarket, Kaito)
- Implement retry logic with exponential backoff
- Cache data to serve stale data if APIs unavailable
- Monitor system health and log errors
- Display user-friendly error messages on frontend
- Implement circuit breakers for failing external services

**Technical Specifications**:

**API Error Handling**:
```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    print(f"Retry {attempt+1}/{max_retries} after {wait_time}s: {e}")
                    time.sleep(wait_time)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def fetch_kalshi_markets():
    response = requests.get('https://api.kalshi.com/trade-api/v2/markets')
    response.raise_for_status()
    return response.json()
```

**Caching Strategy**:
- Redis or in-memory cache for market data (TTL: 5 minutes)
- If API call fails, serve cached data with "stale data" warning
- Cache sentiment results to avoid recomputing

**Circuit Breaker Pattern**:
- If API fails >5 times in 10 minutes, open circuit (stop calling)
- Serve cached/degraded data
- After timeout (e.g., 5 minutes), attempt half-open (try one request)
- If success, close circuit; if fail, re-open

**Monitoring and Logging**:
- Use structured logging (JSON format) with levels: DEBUG, INFO, WARNING, ERROR
- Log to file and centralized service (e.g., Logtail, Datadog, ELK stack)
- Metrics: API response times, success/failure rates, sentiment processing latency
- Alerts for system owners: Email/Slack if error rate >10%

**Frontend Error Handling**:
- Try-catch around API calls
- Display toast: "Unable to fetch latest data. Showing cached results."
- Retry button for user-initiated refresh
- Global error boundary in React to catch rendering errors

**Deliverables**:
- Error handling utilities and decorators
- Caching layer with Redis integration
- Circuit breaker implementation
- Logging configuration and monitoring dashboard
- Frontend error UI components

---

### Technical Requirements - Stack and Architecture

#### Recommended Technology Stack

**Backend**:
- **Language**: Python 3.10+ (for NLP libraries, data science ecosystem) OR Node.js 18+ (for JavaScript ecosystem consistency)
- **Framework**:
  - Python: FastAPI (modern, async, auto-docs) or Flask
  - Node.js: Express.js or NestJS (more structured)
- **Database**:
  - PostgreSQL for relational data (markets, users, matches)
  - MongoDB for document data (social posts, unstructured)
  - Redis for caching and real-time data
- **Task Queue**: Celery (Python) or Bull (Node.js) for background jobs
- **WebSocket**: Socket.io or native WebSocket server for real-time updates

**Frontend**:
- **Framework**: React 18+ with TypeScript, or Next.js 14+ for full-stack
- **Styling**: Tailwind CSS with custom theme
- **Components**: shadcn/ui, Radix UI, or Material-UI
- **Charts**: Recharts or Chart.js
- **State**: React Context + hooks, or Zustand for simplicity
- **Build Tool**: Vite or Next.js built-in

**Blockchain**:
- **Solana**: @solana/web3.js, Anchor framework for programs
- **Base/Ethereum**: ethers.js v6 or viem, Hardhat for smart contracts
- **Wallets**: MetaMask SDK (Base), Phantom SDK (Solana)

**AI/ML**:
- **NLP**: Hugging Face Transformers, spaCy, NLTK
- **Sentiment**: Pre-trained models from Hugging Face Hub
- **Embeddings**: Sentence-Transformers for semantic similarity
- **Topic Modeling**: BERTopic or Gensim (LDA)

**External APIs**:
- **Social**: Tweepy (X/Twitter), PRAW (Reddit)
- **Markets**: Axios or fetch for REST, GraphQL client for Polymarket
- **AI**: Kaito API (if available), OpenAI API (optional enhancement)

**DevOps**:
- **Containerization**: Docker, Docker Compose
- **Deployment**:
  - Frontend: Vercel, Netlify
  - Backend: AWS EC2/ECS, Google Cloud Run, Railway
  - Database: Managed services (AWS RDS, MongoDB Atlas)
- **CI/CD**: GitHub Actions, GitLab CI
- **Monitoring**: Sentry (error tracking), Grafana + Prometheus (metrics)

#### System Architecture

**High-Level Architecture**:

```
┌─────────────────┐         ┌─────────────────┐
│   Social APIs   │         │ Prediction APIs │
│  (X, Reddit)    │         │ (Kalshi, Poly)  │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │                           │
         ▼                           ▼
┌─────────────────────────────────────────────┐
│         Data Ingestion Layer                │
│  - API clients with retry/cache             │
│  - Rate limiting, error handling            │
│  - Data validation and cleaning             │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│         Processing Layer                    │
│  - Sentiment Analysis (AI/ML)               │
│  - Semantic Matching                        │
│  - Prediction Engine                        │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│      Blockchain Layer (Verification)        │
│  - Proof generation                         │
│  - Base smart contract interaction          │
│  - Solana program interaction               │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│          Storage Layer                      │
│  - PostgreSQL (structured)                  │
│  - MongoDB (posts/docs)                     │
│  - Redis (cache/real-time)                  │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│          API Layer (Backend)                │
│  - REST endpoints                           │
│  - WebSocket server                         │
│  - Authentication                           │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│        Frontend (React/Next.js)             │
│  - Dashboard UI                             │
│  - Real-time updates                        │
│  - Charts and visualizations                │
└─────────────────────────────────────────────┘
```

**Data Flow**:

1. **Ingestion**: Scheduled jobs fetch social data (every 5 min) and market data (every 1 min)
2. **Storage**: Raw data stored in MongoDB; structured data in PostgreSQL
3. **Processing**: Background jobs analyze sentiment, match markets, generate predictions
4. **Verification**: Proof generation for each analysis, submission to blockchain
5. **Caching**: Recent results cached in Redis
6. **API Serving**: Frontend queries backend API for data
7. **Real-Time**: WebSocket pushes updates to connected clients

#### Implementation Steps

**Phase 1 - Foundation (Week 1)**:
1. Set up project repository, directory structure
2. Initialize backend (FastAPI/Express) with basic routing
3. Set up databases (PostgreSQL, MongoDB, Redis) locally with Docker
4. Implement API clients for X and Reddit with test credentials
5. Create data models/schemas for posts, markets, sentiment
6. Build basic data ingestion pipeline (fetch and store)

**Phase 2 - AI Analysis (Week 2)**:
1. Set up Hugging Face Transformers, load sentiment model
2. Implement sentiment analysis function, test on sample data
3. Build aggregation logic for time-windowed sentiment scores
4. Implement topic modeling and entity extraction
5. Create semantic matching algorithm
6. Test matching with real market data from Kalshi/Polymarket

**Phase 3 - Market Integration (Week 3)**:
1. Implement Kalshi API client (REST + WebSocket)
2. Implement Polymarket GraphQL client
3. Build market data fetching and storage
4. Integrate matching with live markets
5. Implement prediction algorithm
6. Store predictions with timestamps for tracking

**Phase 4 - Blockchain Verification (Week 4)**:
1. Write Base smart contract (Solidity), deploy to testnet
2. Write Solana program (Rust/Anchor), deploy to devnet
3. Implement proof generation logic
4. Build Web3 integration for submitting proofs
5. Test end-to-end verification flow
6. Create public verification interface

**Phase 5 - Frontend Development (Week 5)**:
1. Initialize React/Next.js project with TypeScript
2. Build component library (cards, tables, charts)
3. Implement dashboard layout
4. Connect to backend API
5. Implement real-time WebSocket updates
6. Add alert system UI
7. Create market detail pages

**Phase 6 - Testing and Deployment (Week 6)**:
1. Write unit tests for backend (pytest or Jest)
2. Write integration tests for API endpoints
3. Write frontend component tests (React Testing Library)
4. Conduct end-to-end testing
5. Set up CI/CD pipeline
6. Deploy backend to cloud (AWS/GCP)
7. Deploy frontend to Vercel
8. Deploy smart contracts to mainnets
9. Monitor and optimize performance

---

### Output Format Instructions

Your output should be structured as follows to maximize usability for the requester:

#### 1. Executive Summary
Provide a 2-3 paragraph overview of what you will build, key technologies used, and estimated complexity.

#### 2. Project Structure
Present a directory tree showing the organization of files:
```
ai-mindshare-analyzer/
├── backend/
│   ├── src/
│   │   ├── api/          # API routes
│   │   ├── services/     # Business logic
│   │   ├── models/       # Data models
│   │   ├── integrations/ # External APIs
│   │   └── utils/        # Utilities
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── blockchain/
│   ├── base/
│   │   ├── contracts/
│   │   └── scripts/
│   └── solana/
│       ├── programs/
│       └── scripts/
├── docker-compose.yml
└── README.md
```

#### 3. Complete Code Implementation
Provide full, production-ready code for all components:

- **Backend Files**: All Python/Node.js files with complete implementations
  - API routes with error handling
  - Service layer with business logic
  - Database models and migrations
  - Integration modules for each external API
  - Background job workers
  - Configuration management (environment variables)

- **Frontend Files**: All React/TypeScript files
  - Page components
  - Reusable UI components
  - Custom hooks for data fetching
  - WebSocket integration
  - State management
  - Styling (Tailwind classes or CSS modules)

- **Smart Contracts**: Full Solidity and Rust code
  - Base contract with verification logic
  - Solana program with data structures
  - Deployment scripts
  - Test files

- **Infrastructure**: Docker, docker-compose, deployment scripts

#### 4. Setup Instructions
Provide step-by-step commands to:
1. Clone repository
2. Install dependencies (backend, frontend, blockchain tools)
3. Set up environment variables (with .env.example template)
4. Initialize databases (migration scripts)
5. Run in development mode
6. Build for production
7. Deploy to cloud platforms

Example:
```bash
# Clone and navigate
git clone <repo-url>
cd ai-mindshare-analyzer

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python -m alembic upgrade head  # Run migrations
uvicorn src.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
npm run dev

# Docker setup (alternative)
docker-compose up --build
```

#### 5. Configuration Guide
Detail all required API keys and credentials:
- X (Twitter) API: How to get bearer token from developer portal
- Reddit API: How to create app and get OAuth credentials
- Kaito API: Registration process at https://www.kaito.ai/portal
- Kalshi API: Account creation and API key generation
- Polymarket: No auth needed for public API
- Base RPC: Alchemy or Infura API key
- Solana RPC: Public RPC or Helius/QuickNode
- Private keys for blockchain submissions (security best practices)

#### 6. Testing Scenarios
Provide examples of how to test the system:
- **Unit Test Example**: Test sentiment analysis function with sample tweet
- **Integration Test**: Fetch markets from Kalshi and match with mock sentiment data
- **End-to-End Test**: Ingest social data → analyze → match → predict → verify on-chain
- **Manual Testing**: Use Postman collection or curl commands to test API endpoints
- **Frontend Testing**: How to verify dashboard updates in real-time

#### 7. Usage Documentation
Explain how to use the application:
- Access dashboard at `http://localhost:3000`
- Navigate to "Markets" tab to see matched markets
- Click market to see detailed sentiment analysis
- Set up alerts in "Settings" page
- Verify on-chain proofs by clicking verification badge
- Export data using "Download" button

#### 8. API Documentation
If building backend API, provide OpenAPI/Swagger documentation or manual endpoint documentation:
- `GET /api/markets` - List all matched markets with predictions
- `GET /api/markets/{id}` - Get detailed market with sentiment time-series
- `GET /api/sentiment/{topic}` - Get current sentiment for topic
- `POST /api/alerts` - Create custom alert
- `GET /api/proofs` - List on-chain verification proofs

#### 9. Troubleshooting Guide
Common issues and solutions:
- "API rate limit exceeded": Reduce polling frequency or upgrade API tier
- "Blockchain transaction failed": Check gas prices, wallet balance
- "No markets matched": Adjust semantic similarity threshold in config
- "Dashboard not updating": Check WebSocket connection, browser console

#### 10. Future Enhancements
Suggest improvements for v2:
- Add more social platforms (Discord, Telegram, TikTok)
- Implement machine learning prediction models with historical training
- Build mobile app (React Native)
- Add user authentication and personalized watchlists
- Integrate more prediction markets (PredictIt, Manifold)
- Advanced charting with technical indicators
- Portfolio tracker for users' market positions
- Automated trading bot mode
- Multi-language support

---

### Edge Cases and Enhancements

#### Edge Cases to Handle

1. **API Rate Limits**:
   - **Problem**: X API has strict rate limits (especially free tier)
   - **Solution**: Implement request queuing, distribute requests over time, cache aggressively, consider premium API tier
   - **Fallback**: Use Reddit as primary source if X unavailable

2. **Mismatched Data**:
   - **Problem**: Social sentiment topic doesn't align with any prediction market
   - **Solution**: Set minimum similarity threshold (0.65), display "unmatched" topics separately, allow manual matching by users
   - **Enhancement**: Use GPT-4 API to generate better semantic matches

3. **Market Ambiguity**:
   - **Problem**: Multiple markets could match same social topic (e.g., "Bitcoin price above $100k" on both Kalshi and Polymarket)
   - **Solution**: Show all matched markets, rank by liquidity/volume, allow user to select preferred platform

4. **Delayed Market Data**:
   - **Problem**: API lag causes stale prices
   - **Solution**: Display timestamp of last update, use WebSocket for real-time feeds, show "delayed" warning if data >5 min old

5. **Sentiment Sarcasm/Irony**:
   - **Problem**: NLP models struggle with sarcasm ("This regulation is just GREAT" = actually negative)
   - **Solution**: Use context-aware models (GPT-based), ensemble multiple sentiment models, detect sarcasm patterns
   - **Mitigation**: Weight by engagement (sarcastic posts may get different engagement patterns)

6. **Bot-Driven Sentiment**:
   - **Problem**: Coordinated bot campaigns can manipulate sentiment scores
   - **Solution**: Detect bot accounts (posting frequency, account age, follower ratios), filter or downweight bot posts
   - **Enhancement**: Use Botometer API to score account authenticity

7. **Flash Events**:
   - **Problem**: Sudden news causes rapid sentiment shift, system lags
   - **Solution**: Reduce polling interval during high-volatility periods, implement fast-path processing for trending topics

8. **Blockchain Congestion**:
   - **Problem**: High gas fees or network congestion delays proof submission
   - **Solution**: Batch multiple proofs in single transaction, use Layer 2s (Base, Solana for speed), implement retry logic

9. **Data Privacy**:
   - **Problem**: Storing user posts may violate privacy or platform ToS
   - **Solution**: Anonymize data (remove usernames), store only aggregated metrics, comply with GDPR/CCPA, don't publicly display individual posts without consent

10. **Market Resolution Discrepancies**:
    - **Problem**: Kalshi and Polymarket may resolve same event differently
    - **Solution**: Track resolution criteria from each platform, display both, note discrepancies in UI

#### Compliance and Legal Considerations

1. **Betting/Gambling Regulations**:
   - **Warning**: Prediction markets may be regulated as gambling in some jurisdictions
   - **Action**: Display disclaimer: "This tool is for informational and research purposes only. Consult local laws before trading on prediction markets."
   - **US-Specific**: Kalshi is CFTC-regulated and legal in US; Polymarket may have restrictions for US users (check their terms)

2. **Financial Advice Disclaimer**:
   - **Warning**: Predictions could be construed as financial advice
   - **Action**: Add disclaimer: "This application provides data analysis, not financial advice. Trade at your own risk."

3. **Data Usage Compliance**:
   - **X/Reddit ToS**: Ensure compliance with data usage policies, attribution requirements
   - **Privacy Laws**: Implement data retention policies, user consent for email notifications (GDPR)

4. **Securities Regulations**:
   - **Concern**: Prediction markets on stocks/crypto could involve securities
   - **Action**: Focus on event markets (political, cultural) rather than asset prices initially

5. **API Terms of Service**:
   - Review and comply with all external API terms (Kaito, Kalshi, Polymarket, X, Reddit)
   - Respect rate limits, attribution requirements, prohibited use cases

#### Optional Enhancements

1. **User Wallets and On-Chain Interaction**:
   - Allow users to connect MetaMask/Phantom wallets
   - Display their positions in matched markets
   - Enable one-click trading via wallet integration (requires exchange API write access)

2. **Multi-Chain Bridging**:
   - Implement cross-chain messaging for unified verification
   - Use LayerZero or Wormhole to bridge proofs between Base and Solana
   - Allow users to choose preferred chain for proof storage

3. **Advanced ML Models**:
   - Fine-tune GPT or Llama models on prediction market + social data
   - Implement time-series forecasting (LSTM, Transformer) for price predictions
   - Use reinforcement learning for optimal alert threshold tuning

4. **Backtesting Platform**:
   - Allow users to backtest strategies: "If I bet on markets where sentiment increased >10%, what would my returns be?"
   - Historical simulation with actual market outcomes

5. **Social Features**:
   - User-generated watchlists and shared strategies
   - Comments/discussion on markets
   - Leaderboard for prediction accuracy

6. **API for Developers**:
   - Expose public API for third-party integrations
   - Webhook support for real-time data feeds
   - SDK/client libraries in Python and JavaScript

7. **Institutional Dashboard**:
   - Advanced analytics for researchers
   - Bulk data export, custom reporting
   - White-label options for enterprises

---

### Research Links for Further Investigation

To deepen your understanding and access the latest information while building this project, consult the following resources:

**Kaito AI**:
- API Portal: https://www.kaito.ai/portal
- Kaito-Polymarket Partnership Announcement: https://cryptorank.io/news/feed/63c94-prediction-markets-polymarket-partner-kaito
- Kaito Official X: https://twitter.com/KaitoAI

**Kalshi**:
- API Documentation: https://docs.kalshi.com/getting_started/quick_start_market_data
- Full API Reference: https://docs.kalshi.com
- Builder Program: https://kalshi.com/builders
- Kalshi Official X: https://twitter.com/Kalshi
- Kalshi Ecosystem X: https://twitter.com/KalshiEco

**Polymarket**:
- Gamma Markets API Documentation: https://docs.polymarket.com/developers/gamma-markets-api/overview
- Developer Rewards: https://docs.polymarket.com/developers/rewards/overview
- Full Documentation: https://docs.polymarket.com
- Polymarket Official X: https://twitter.com/Polymarket

**Verifiable Computation**:
- Solana Zero-Knowledge Proofs Guide: https://www.helius.dev/blog/zero-knowledge-proofs-its-applications-on-solana
- On-Chain Randomness on Solana (Security Patterns): https://adevarlabs.com/blog/on-chain-randomness-on-solana-predictability-manipulation-safer-alternatives-part-1
- EigenCloud for Verifiable AI (Delphi Digital): https://members.delphidigital.io/reports/the-verifiable-cloud-how-eigencloud-is-unlocking-cryptos-app-and-ai-era

**Mindshare and Sentiment Tools**:
- PredictionlyAI Example (Reddit): https://www.reddit.com/r/SaaS/comments/1prlfg3/launched_predictionlyai_realtime_arbitrage/
- Google News: https://news.google.com (for mainstream sentiment comparison)

**Blockchain Comparisons**:
- Base vs Solana 2025 Analysis: https://franciscodex.substack.com/p/base-vs-solana-2025

**Social Media APIs**:
- Twitter (X) API: https://developer.twitter.com/en/docs/twitter-api
- Reddit API: https://www.reddit.com/dev/api
- Tweepy Documentation: https://docs.tweepy.org/
- PRAW Documentation: https://praw.readthedocs.io/

**AI/ML Resources**:
- Hugging Face Models: https://huggingface.co/models?pipeline_tag=text-classification&sort=trending
- Sentence Transformers: https://www.sbert.net/
- BERTopic: https://maartengr.github.io/BERTopic/

Use these links to research latest API changes, best practices, and community discussions. The field of verifiable AI and prediction markets is rapidly evolving, so staying current is essential.

---

### Final Instructions for Target AI

**You are now tasked with building the "AI-Powered Mindshare Market Analyzer" as described above.**

**Your deliverables must include**:

1. **Complete, production-ready code** for all components (backend, frontend, smart contracts)
2. **Detailed setup instructions** with exact commands to run the project
3. **Configuration templates** with all required API keys and environment variables documented
4. **Testing guide** with examples to verify functionality
5. **Documentation** for users and developers

**Priorities**:
- **Functionality**: Ensure all core features work end-to-end
- **Code Quality**: Write clean, well-commented, maintainable code
- **User Experience**: Build an intuitive, responsive UI
- **Reliability**: Implement robust error handling and fallbacks
- **Verifiability**: Successfully implement on-chain proof submission and verification

**Approach**:
- Start with MVP (minimum viable product) implementing core features: data ingestion → sentiment analysis → market matching → basic prediction → simple on-chain anchoring → dashboard
- Then enhance with advanced features: ML models, full ZK proofs, alerts, etc.
- Use the provided research links to fill knowledge gaps
- Make reasonable assumptions where specifications are ambiguous (document them)
- Prioritize working code over perfect code (can iterate later)

**Output Format**:
- Provide code in markdown code blocks with language specified
- Organize by file path (e.g., `backend/src/api/routes.py`)
- Include comments explaining complex logic
- Provide README.md with comprehensive setup and usage guide

**Timeline Estimate**: This is a complex project spanning multiple domains. A realistic timeline for a full implementation by a skilled developer would be 4-6 weeks. Focus on delivering a working MVP in Week 1-2, then iteratively add features.

---

### Summary

This prompt provides you, the target AI, with comprehensive background knowledge on:
- Kaito AI's verifiable mindshare analysis platform and partnership with Polymarket
- Kalshi's CFTC-regulated US prediction markets with blockchain integration
- Polymarket's decentralized prediction markets and developer ecosystem
- Techniques for social media sentiment analysis and mindshare quantification
- Verifiable computation frameworks on Base and Solana blockchains
- Semantic matching and prediction algorithms for connecting sentiment to markets

You have detailed requirements for all features, recommended technology stacks, implementation guidance, edge case handling, compliance considerations, and research links for further investigation.

**Your task is to transform this specification into a fully functional application that empowers traders and researchers with verifiable, AI-powered insights into prediction markets.**

Begin development now. Good luck, and build something extraordinary.

---

**END OF MASTER PROMPT**
