# 🚀 Deployment Guide

## ✅ Successfully Deployed to Apify!

Your **Agentic Stock Actor** is now live on the Apify platform!

### 📍 Actor Details

- **Actor ID**: `43ZTkpbPq0YKf3djc`
- **Username**: `luxurious_gel`
- **Actor URL**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
- **Build URL**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc#/builds/1.0.2

---

## 🎮 How to Run Your Actor

### Option 1: Run from Apify Console (Easiest)

1. **Visit your actor**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
2. **Click "Try it"** or **"Start"**
3. **Configure input**:
```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "YOUR_OPENAI_KEY",
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50,
  "subreddits": ["wallstreetbets", "stocks", "investing", "StockMarket"]
}
```
4. **Click "Start"** and watch it run!

### Option 2: Run via Apify CLI

```bash
# Run the actor
apify call luxurious_gel/agentic-stock-actor --input test_input.json

# Or run with inline input
apify call luxurious_gel/agentic-stock-actor --input '{
  "tickers": ["AAPL"],
  "openaiApiKey": "YOUR_KEY",
  "maxNewsPerTicker": 20
}'
```

### Option 3: Run via Apify API

```javascript
const { ApifyClient } = require('apify-client');

const client = new ApifyClient({
    token: 'YOUR_APIFY_API_TOKEN'
});

// Run the actor
const run = await client.actor('luxurious_gel/agentic-stock-actor').call({
    tickers: ['AAPL', 'TSLA', 'NVDA'],
    openaiApiKey: 'YOUR_OPENAI_KEY',
    maxNewsPerTicker: 20,
    maxRedditPostsPerTicker: 50
});

// Fetch results
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log('Trading signals:', items);
```

### Option 4: Run via Python

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_API_TOKEN')

# Run the actor
run = client.actor('luxurious_gel/agentic-stock-actor').call(run_input={
    'tickers': ['AAPL', 'TSLA', 'NVDA'],
    'openaiApiKey': 'YOUR_OPENAI_KEY',
    'maxNewsPerTicker': 20,
    'maxRedditPostsPerTicker': 50
})

# Get results
dataset = client.dataset(run['defaultDatasetId'])
results = dataset.list_items().items

for signal in results:
    print(f"{signal['ticker']}: {signal['signal']} ({signal['confidence']:.0%} confidence)")
    print(f"  Reasoning: {signal['reasoning']}")
```

---

## ⏰ Scheduling Regular Runs

### Set up Daily Analysis (6am & 1pm CST)

1. **Go to**: https://console.apify.com/schedules
2. **Click "Create new schedule"**
3. **Configure**:
   - Name: "Stock Analysis - Morning"
   - Actor: `luxurious_gel/agentic-stock-actor`
   - Cron: `0 6 * * *` (6am CST)
   - Input: Your watchlist JSON
4. **Repeat** for afternoon run with cron: `0 13 * * *`

---

## 📊 Example Output

When you run the actor, you'll get results like this:

```json
{
  "ticker": "AAPL",
  "signal": "BUY",
  "confidence": 0.85,
  "reasoning": "Strong positive sentiment from AI partnership news while price dipped 2% below recent high. Excellent entry point for swing trade.",
  "key_catalysts": [
    "AI partnership announcement",
    "Price near support level",
    "High volume",
    "Positive Reddit sentiment"
  ],
  "risk_level": "medium",
  "current_price": 182.50,
  "sentiment_score": 0.68,
  "market_moving_events": ["partnership", "product launch"]
}
```

---

## 🔄 Updating Your Actor

To deploy changes:

```bash
cd /Users/sachinkeswani/AgenticStockActor
apify push
```

---

## 📈 Monitor Runs

- **All runs**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc#/runs
- **View logs**: Click on any run to see detailed execution logs
- **Download results**: Export as JSON, CSV, Excel, or HTML

---

## 🎯 Next Steps for Hackathon

1. **Test with various tickers** - Try different stocks to verify accuracy
2. **Add more features**:
   - Email/Slack notifications for BUY signals
   - Backtesting functionality
   - Portfolio tracking
   - Risk scoring improvements
3. **Create demo video** - Show the actor in action
4. **Prepare presentation** - Highlight the AI agent's value proposition
5. **Document results** - Show real trading signals and accuracy

---

## 🏆 Hackathon Submission Checklist

- [x] Actor created and deployed to Apify
- [x] Uses Apify SDK and platform features
- [x] AI-powered analysis (OpenAI GPT-4)
- [x] Real-time web scraping (Yahoo Finance, Reddit)
- [x] Produces actionable outputs (BUY/SELL signals)
- [ ] Create demo video
- [ ] Write blog post about the solution
- [ ] Submit to hackathon

---

## 🔗 Important Links

- **Your Actor**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
- **Apify Console**: https://console.apify.com/
- **Apify 1M Challenge**: https://apify.notion.site/apify-1m-challenge-hackathon
- **Documentation**: https://docs.apify.com/

---

## 🆘 Troubleshooting

### Actor fails to run
- Check OpenAI API key is valid
- Ensure tickers are valid stock symbols
- Check actor logs for specific errors

### No results returned
- Verify tickers exist on Yahoo Finance
- Check if markets are open (for real-time data)
- Increase maxNewsPerTicker if getting limited data

### Rate limits
- Add delays between tickers (built-in)
- Use Apify proxies for Reddit scraping
- Monitor OpenAI API usage

---

**Congratulations! Your actor is live and ready to generate trading signals! 🎉**

