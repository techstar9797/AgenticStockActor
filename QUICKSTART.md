# 🚀 Quick Start Guide - Agentic Stock Actor

## ✅ Your Actor is LIVE!

**Actor URL**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc

---

## 🎯 What Does It Do?

Your AI agent:
1. ✅ Scrapes **Yahoo Finance** for stock prices and news
2. ✅ Scrapes **Reddit** (r/wallstreetbets, r/stocks, etc.) for sentiment
3. ✅ Uses **GPT-4** to analyze sentiment and detect market-moving events
4. ✅ Generates **BUY/SELL/HOLD/WATCH** signals with reasoning

**Perfect for swing trading** - Find dips to buy and spikes to sell!

---

## 🏃 Run It Right Now (3 Ways)

### 1️⃣ Via Web Console (Click and Go!)

1. Visit: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
2. Click **"Start"**
3. Paste this input:
```json
{
  "tickers": ["AAPL", "TSLA"],
  "openaiApiKey": "YOUR_OPENAI_API_KEY_HERE"
}
```
4. Click **"Start"** and watch the magic! ✨

### 2️⃣ Via Command Line

```bash
apify call luxurious_gel/agentic-stock-actor --input test_input.json
```

### 3️⃣ Via API (Python)

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_API_TOKEN')

run = client.actor('luxurious_gel/agentic-stock-actor').call(run_input={
    'tickers': ['AAPL', 'NVDA', 'MSFT'],
    'openaiApiKey': 'YOUR_KEY'
})

# Get trading signals
results = client.dataset(run['defaultDatasetId']).list_items().items
for r in results:
    print(f"{r['ticker']}: {r['signal']} - {r['reasoning']}")
```

---

## 📊 What You'll Get

Each ticker returns:

```
🟢 AAPL: BUY (85% confidence)
   Price: $182.50 (-1.24%)
   Sentiment: +0.68 (very_positive)
   
   Reasoning: "Strong positive sentiment from AI partnership 
   announcement while price dipped 2% below recent high. 
   Excellent swing trade entry point."
   
   Key Catalysts:
   • AI partnership announcement
   • Price near support level  
   • High trading volume
   • Bullish Reddit sentiment
   
   Risk: MEDIUM
   Strategy: "Enter on next small dip. Set stop-loss at $175."
```

---

## ⏰ Set Up Daily Auto-Run (6am & 1pm)

1. Go to: https://console.apify.com/schedules
2. Click **"Create schedule"**
3. Set:
   - **Cron**: `0 6,13 * * *` (6am and 1pm daily)
   - **Actor**: `luxurious_gel/agentic-stock-actor`
   - **Input**: Your watchlist tickers
4. Save and you're done! 🎉

---

## 🎯 Hackathon Tips

### Make Your Demo Stand Out

1. **Run with Popular Stocks**:
   - AAPL, TSLA, NVDA, MSFT, AMZN, GOOGL
   - Meme stocks: GME, AMC (high Reddit activity!)

2. **Show Real Value**:
   - "Agent detected negative earnings news BEFORE price crashed"
   - "Found bullish sentiment divergence - BUY signal at dip"

3. **Create Screenshot/Video** showing:
   - Input: Your watchlist
   - Output: BUY/SELL signals with reasoning
   - Sentiment analysis breakdown
   - Market-moving events detected

### Key Differentiators

✅ **Real-time data** (not historical)  
✅ **AI-powered reasoning** (not just rules)  
✅ **Multi-source analysis** (news + social)  
✅ **Divergence detection** (sentiment vs. price)  
✅ **Actionable signals** (not just data dumps)  
✅ **Fully automated** (runs on schedule)  

---

## 📁 Project Structure

```
AgenticStockActor/
├── .actor/
│   ├── actor.json              # Actor config
│   └── input_schema.json       # Input validation
├── src/
│   ├── main.py                 # Main orchestrator
│   ├── scrapers/
│   │   ├── yahoo_finance.py    # Yahoo scraper
│   │   └── reddit.py           # Reddit scraper
│   └── analyzers/
│       ├── sentiment.py        # GPT-4 sentiment
│       └── trading_signal.py   # Signal generator
├── Dockerfile                  # Container config
├── requirements.txt            # Python deps
├── README.md                   # Full documentation
└── DEPLOYMENT.md              # Deployment guide
```

---

## 🔧 Customize Your Watchlist

Edit `test_input.json`:

```json
{
  "tickers": ["YOUR", "STOCKS", "HERE"],
  "subreddits": ["wallstreetbets", "stocks", "investing"],
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50
}
```

Then run:
```bash
apify call luxurious_gel/agentic-stock-actor --input test_input.json
```

---

## 🎥 Demo Script

**For your hackathon presentation:**

1. **Problem**: "Swing traders miss opportunities because they can't track news and sentiment for multiple stocks 24/7"

2. **Solution**: "Agentic Stock Actor - AI agent that monitors stocks and tells you WHEN to buy dips and sell spikes"

3. **Live Demo**:
   - Show Apify console
   - Run actor with 3-5 tickers
   - Show results appearing in real-time
   - Highlight a BUY signal with reasoning
   - Show sentiment breakdown

4. **Impact**: "Saved traders from FOMO buys by detecting negative sentiment before crashes"

5. **Tech**: "Built on Apify platform + GPT-4, fully automated and scalable"

---

## 📞 Quick Links

- **Run Actor**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
- **View Runs**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc#/runs
- **Create Schedule**: https://console.apify.com/schedules
- **API Docs**: https://docs.apify.com/api/v2

---

## 🏆 You're Ready to Win!

Your actor is:
- ✅ Deployed and working
- ✅ Using AI (GPT-4)
- ✅ Scraping real-time data
- ✅ Producing actionable insights
- ✅ Fully automated

**Now go create your demo and win that hackathon! 🚀**

---

*Built with ❤️ for the Apify 1M Challenge*

