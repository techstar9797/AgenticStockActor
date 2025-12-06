# 🎯 Agentic Stock Actor

**AI-Powered Stock Timing Agent for Swing Trading**

Built for the [Apify 1M Challenge Hackathon](https://apify.notion.site/apify-1m-challenge-hackathon)

## 🏆 Overview

Agentic Stock Actor is an AI-powered trading assistant that helps swing traders time their entries and exits by analyzing real-time data from multiple sources:

- **📊 Yahoo Finance**: Stock prices, market data, and financial news
- **💬 Reddit**: Community sentiment from r/wallstreetbets, r/stocks, r/investing
- **🤖 GPT-4**: Advanced sentiment analysis and trading signal generation

The actor identifies **buy opportunities on dips** and **sell signals on spikes** by detecting divergences between price action and sentiment.

## 🚀 Features

### Data Collection
- Real-time stock price data from Yahoo Finance
- Latest financial news and market-moving events
- Reddit posts and community sentiment from investing subreddits
- Engagement metrics (scores, comments, volume)

### AI Analysis
- **Sentiment Analysis**: GPT-4 analyzes news headlines and Reddit discussions
- **Market-Moving Event Detection**: Identifies earnings, acquisitions, FDA approvals, etc.
- **Technical Indicators**: 52-week positioning, volume ratios
- **Divergence Detection**: Finds mismatches between sentiment and price

### Trading Signals
- **🟢 BUY**: Strong buy opportunity (e.g., positive sentiment + price dip)
- **🔴 SELL**: Sell recommendation (e.g., negative news + price spike)
- **🟡 HOLD**: Wait for clearer signals
- **🔵 WATCH**: Interesting setup, needs confirmation

Each signal includes:
- Confidence score (0-100%)
- Detailed reasoning
- Key catalysts
- Risk level (low/medium/high)
- Entry/exit strategy

## 📖 How It Works

```
┌─────────────────────────────────────────────────────────┐
│  INPUT: Stock Tickers (e.g., AAPL, TSLA, NVDA)         │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Scrape Yahoo Finance                          │
│  • Current price, 52-week range, volume                │
│  • Latest news articles                                │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Scrape Reddit                                 │
│  • Posts mentioning ticker                             │
│  • Scores, comments, engagement                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: AI Sentiment Analysis (GPT-4)                 │
│  • News sentiment (-1 to +1)                           │
│  • Reddit sentiment (-1 to +1)                         │
│  • Overall sentiment (60% news, 40% Reddit)            │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: Generate Trading Signal (GPT-4)               │
│  • Analyzes price + sentiment                          │
│  • Detects divergences                                 │
│  • Provides BUY/SELL/HOLD/WATCH                        │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│  OUTPUT: Trading Signals with Reasoning                │
└─────────────────────────────────────────────────────────┘
```

## 🎮 Usage

### On Apify Platform

1. **Go to**: [Apify Console](https://console.apify.com/)
2. **Find**: "Agentic Stock Actor"
3. **Configure Input**:
```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "sk-...",
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50,
  "subreddits": ["wallstreetbets", "stocks", "investing", "StockMarket"]
}
```
4. **Run** and view results!

### Via Apify API

```javascript
const { ApifyClient } = require('apify-client');

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

const run = await client.actor('YOUR_USERNAME/agentic-stock-actor').call({
  tickers: ['AAPL', 'MSFT', 'GOOGL'],
  openaiApiKey: 'sk-...',
  maxNewsPerTicker: 20
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### Schedule Regular Runs

Set up Apify Schedules to run at:
- **6:00 AM CST** (before market open)
- **1:00 PM CST** (mid-day check)

## 📊 Output Format

```json
{
  "ticker": "AAPL",
  "timestamp": "2024-12-06T12:00:00Z",
  
  "signal": "BUY",
  "confidence": 0.85,
  "reasoning": "Strong positive sentiment from partnership news while price dipped 3% below recent high. High volume suggests institutional buying. Good entry point for swing trade.",
  "key_catalysts": [
    "Major partnership announcement",
    "Price near support level",
    "Unusually high volume",
    "Positive Reddit sentiment"
  ],
  "risk_level": "medium",
  "entry_strategy": "Consider entering on next small dip. Set stop-loss at $175.",
  
  "current_price": 182.50,
  "price_change": -2.30,
  "percent_change": -0.0124,
  "position_52w": 0.73,
  
  "sentiment_score": 0.68,
  "sentiment_label": "very_positive",
  "news_sentiment": 0.75,
  "reddit_sentiment": 0.58,
  "community_mood": "bullish",
  
  "market_moving_events": ["partnership", "product launch"],
  "key_topics": ["AI", "partnership", "revenue growth"],
  
  "news_count": 15,
  "reddit_posts_count": 42
}
```

## 🎯 Use Cases

### For Swing Traders
- Identify dip-buying opportunities
- Know when to take profits
- Avoid FOMO by seeing real sentiment
- Get early warnings of trend changes

### For Portfolio Managers
- Monitor multiple tickers efficiently
- Get AI-powered insights on holdings
- Detect market-moving events quickly
- Automate daily market research

### For Researchers
- Analyze correlation between sentiment and price
- Study social media impact on stocks
- Backtest trading strategies
- Collect historical sentiment data

## 🛠️ Tech Stack

- **Apify SDK**: Actor framework and infrastructure
- **BeautifulSoup + httpx**: Web scraping
- **OpenAI GPT-4**: Sentiment analysis and signal generation
- **Python 3.11**: Core logic

## 📅 Scheduling

For automated daily analysis:

1. Go to [Apify Schedules](https://console.apify.com/schedules)
2. Create new schedule
3. Set cron: `0 6,13 * * *` (6am and 1pm daily CST)
4. Configure actor input
5. Enable notifications (optional)

## 🔒 Security

- API keys are stored securely as secrets
- OpenAI key never logged or exposed
- No data persistence (runs are stateless)
- Follow Apify security best practices

## 📝 License

MIT License - Built for Apify 1M Challenge Hackathon

## 🤝 Contributing

Built by: Sachin Keswani
Hackathon: Apify 1M Challenge
Date: December 2024

## 🔗 Links

- [Apify 1M Challenge](https://apify.notion.site/apify-1m-challenge-hackathon)
- [Apify Platform](https://apify.com)
- [Actor Documentation](https://docs.apify.com/platform/actors)

---

**Made with ❤️ for swing traders everywhere**

