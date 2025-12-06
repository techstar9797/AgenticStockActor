# 🎯 Agentic Stock Actor

**AI-Powered Stock Timing Agent with WhatsApp Notifications**

Built for the [Apify 1M Challenge Hackathon](https://apify.notion.site/apify-1m-challenge-hackathon)

[![Deployed on Apify](https://img.shields.io/badge/Apify-Deployed-brightgreen)](https://console.apify.com/actors/43ZTkpbPq0YKf3djc)
[![Running Hourly](https://img.shields.io/badge/Schedule-Hourly-blue)](https://console.apify.com/schedules/7A6c15ixwldghb0bh)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![OpenAI GPT-4](https://img.shields.io/badge/AI-GPT--4-purple)](https://openai.com/)

---

## 🏆 Overview

Agentic Stock Actor is an **AI-powered trading assistant** that helps swing traders time their entries and exits by analyzing real-time data from **4 sources**:

- **📊 Yahoo Finance**: Stock prices, market data, and financial news
- **💬 Reddit**: Community sentiment from r/wallstreetbets, r/stocks, r/investing, r/StockMarket
- **📱 Truth Social**: @realDonaldTrump posts for political risk analysis
- **🤖 GPT-4**: Advanced sentiment analysis and trading signal generation

The actor identifies **buy opportunities on dips** and **sell signals on spikes** by detecting divergences between price action and sentiment. **Get instant WhatsApp alerts** when trading signals change!

---

## ✨ Unique Features

### 🆕 What Makes This Special:

1. **📱 WhatsApp Notifications** - Get instant mobile alerts when signals change
2. **🇺🇸 Trump Sentiment Analysis** - Track @realDonaldTrump for market-moving posts
3. **🤖 AI-Powered Reasoning** - GPT-4 explains every signal with detailed analysis
4. **🔔 Signal Change Detection** - Automatic notifications for BUY→SELL, HOLD→WATCH, etc.
5. **⏰ Fully Automated** - Runs every hour, 24/7 on Apify platform

---

## 🚀 Quick Start (5 Minutes)

### 1. Run on Apify Console

1. Visit: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
2. Click **"Start"**
3. Configure input:

```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "YOUR_OPENAI_KEY",
  "whatsappNumber": "+15551234567",
  "twilioAccountSid": "ACxxxxx...",
  "twilioAuthToken": "your_token",
  "enableNotifications": true
}
```

4. Get instant WhatsApp alerts! 📱

### 2. Set Up WhatsApp (Optional)

1. Free Twilio account: https://www.twilio.com/try-twilio ($15 free credit)
2. Activate WhatsApp sandbox (5 minutes)
3. Add credentials to actor input
4. Receive instant mobile notifications!

**Full guide**: See [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)

---

## 📊 What You Get

### Trading Signals:

```
🟢 BUY Signal - AAPL (85% confidence)

💰 Price: $182.50 (-1.2%)
💭 Sentiment: +0.68 (very positive)

📝 AI Reasoning:
"Strong positive sentiment from AI partnership announcement 
while price dipped 2% below recent high. Excellent swing 
trade entry point."

🔑 Key Catalysts:
• AI partnership announcement
• Price near support level ($180)
• High volume (2.3x average)
• Positive Reddit sentiment (+0.65)

📱 TRUMP IMPACT: MEDIUM
Trump mentioned AI sector positively (+0.40 sentiment)

⚖️ Risk: MEDIUM

💡 Entry Strategy:
"Enter below $185. Set stop-loss at $175. Target $200."

🕐 14:00 UTC
```

### WhatsApp Notification:

```
🚨 URGENT SIGNAL CHANGE: AAPL

🟡 Previous: HOLD
🟢 *NEW: BUY*

💰 $182.50
💭 +0.68
🎯 85%

Strong positive sentiment from 
partnership while price dipped...

🕐 14:00 UTC
```

---

## 🎯 Features

### Data Collection (4 Sources):
- ✅ **Yahoo Finance**: Real-time prices, news, market data
- ✅ **Reddit**: 4 major investing subreddits (25M+ members)
- ✅ **Truth Social**: @realDonaldTrump political sentiment
- ✅ **OpenAI GPT-4**: AI analysis and reasoning

### AI Analysis:
- ✅ **Sentiment Scoring**: -1 (very negative) to +1 (very positive)
- ✅ **Market-Moving Events**: Earnings, partnerships, FDA approvals, tariffs
- ✅ **Trump Impact**: Political risk quantification (0x to 2.0x weight)
- ✅ **Divergence Detection**: Sentiment vs. price mismatches
- ✅ **Technical Indicators**: 52-week position, volume ratios

### Trading Signals:
- ✅ **4 Signal Types**: BUY, SELL, HOLD, WATCH
- ✅ **Confidence Scores**: 0-100% certainty
- ✅ **Risk Assessment**: Low, Medium, High
- ✅ **Entry Strategies**: Specific price levels and tactics
- ✅ **AI Reasoning**: Detailed explanations

### Notifications:
- ✅ **WhatsApp**: Instant mobile alerts (via Twilio)
- ✅ **Signal Changes**: BUY→SELL, HOLD→WATCH, etc.
- ✅ **Trump Alerts**: When ticker is mentioned
- ✅ **Console Logs**: Real-time logging
- ✅ **Dataset History**: All notifications saved

### Automation:
- ✅ **Hourly Schedule**: Runs every hour automatically
- ✅ **Signal Tracking**: Stores history in key-value store
- ✅ **Change Detection**: Compares with previous run
- ✅ **Auto-Notifications**: Sends alerts automatically

---

## 📖 How It Works

```
Every Hour:
┌────────────────────────────────────────────┐
│ 1. Scrape Yahoo Finance                   │
│    • Prices, news, market data             │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│ 2. Scrape Reddit (4 subreddits)           │
│    • Posts, scores, comments               │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│ 3. Scrape Truth Social (@realDonaldTrump) │
│    • Recent posts, ticker mentions         │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│ 4. AI Sentiment Analysis (GPT-4)          │
│    • News: -1 to +1                        │
│    • Reddit: Community mood                │
│    • Trump: Political impact (0x to 2.0x)  │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│ 5. Generate Trading Signal (GPT-4)        │
│    • BUY/SELL/HOLD/WATCH                   │
│    • Confidence + Reasoning                │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│ 6. Detect Signal Changes                  │
│    • Compare with previous run             │
│    • Identify significant changes          │
└────────────────────────────────────────────┘
                    ↓
┌────────────────────────────────────────────┐
│ 7. Send WhatsApp Notification 📱          │
│    • If signal changed                     │
│    • Instant mobile alert                  │
└────────────────────────────────────────────┘
```

---

## 🎮 Usage

### Basic (News Only):

```json
{
  "tickers": ["AAPL", "TSLA"],
  "openaiApiKey": "YOUR_KEY"
}
```

### Advanced (With WhatsApp):

```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "YOUR_OPENAI_KEY",
  
  "whatsappNumber": "+15551234567",
  "twilioAccountSid": "ACxxxxx...",
  "twilioAuthToken": "your_token",
  "enableNotifications": true,
  
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50,
  "maxTrumpPosts": 20,
  "subreddits": ["wallstreetbets", "stocks", "investing", "StockMarket"]
}
```

---

## 📱 WhatsApp Notifications

Get **instant mobile alerts** when trading signals change!

### Example Message:

```
🚨 URGENT: TSLA

🟡→🟢 HOLD to BUY

💰 $378.50
🎯 90% confidence

📱 TRUMP MENTIONED TSLA!
"Tesla doing incredible work..."

Buy below $380
Stop: $365
Target: $420

🕐 13:00 UTC
```

### Setup (5 Minutes):

1. **Get Twilio account**: https://www.twilio.com/try-twilio (FREE $15 credit)
2. **Activate WhatsApp**: Send "join your-code" to Twilio's number
3. **Add to input**: Phone number + Twilio credentials
4. **Done!** Receive instant alerts 📱

**Full guide**: [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)

---

## 🇺🇸 Trump Sentiment Analysis

**Unique Feature**: Track @realDonaldTrump's Truth Social posts for market impact!

### Why It Matters:

- 📈 Trump's posts can move markets **immediately**
- 💥 Tariff announcements: Direct company impact
- 🎯 Company mentions: Significant price swings
- 📊 Policy changes: Industry-wide effects

### Impact Levels:

| Level | Weight | Example |
|-------|--------|---------|
| **HIGH** | 2.0x | "Tesla doing incredible work!" → BUY boost |
| **MEDIUM** | 0.7x | "Tariffs on auto parts" → Industry impact |
| **LOW** | 0.3x | "Manufacturing booming" → General positive |

### Example:

```
📱 TRUMP IMPACT ALERT

🚨 TSLA DIRECTLY MENTIONED!
Impact: HIGH (2.0x weight)
Sentiment: +0.90 (very positive)

Post: "Tesla doing incredible work on American 
manufacturing. Great American company!"

Market Prediction: Strong positive reaction expected
Original sentiment: +0.45 → Trump-adjusted: +0.78

Signal: WATCH → BUY
```

**Full guide**: [TRUTH_SOCIAL_INTEGRATION.md](TRUTH_SOCIAL_INTEGRATION.md)

---

## 📊 Output Format

```json
{
  "ticker": "AAPL",
  "signal": "BUY",
  "confidence": 0.85,
  "reasoning": "Strong positive sentiment...",
  "key_catalysts": ["Partnership", "Price dip", "High volume"],
  "risk_level": "medium",
  "entry_strategy": "Enter below $185. Stop: $175. Target: $200.",
  
  "current_price": 182.50,
  "percent_change": -0.0124,
  "position_52w": 0.73,
  "volume_ratio": 2.3,
  
  "sentiment_score": 0.68,
  "news_sentiment": 0.75,
  "reddit_sentiment": 0.58,
  "trump_sentiment": 0.40,
  "trump_impact_level": "medium",
  "trump_mentioned_ticker": false,
  
  "market_moving_events": ["partnership", "product launch"],
  "trump_themes": ["AI", "Manufacturing"],
  
  "signal_changed": true,
  "previous_signal": "HOLD",
  "notification_sent": true
}
```

---

## ⏰ Automation

### Hourly Schedule (Active):

- **Frequency**: Every hour (`:00`)
- **Timezone**: America/Chicago (CST)
- **Tickers**: AAPL, TSLA, NVDA
- **Status**: ✅ ENABLED

**Schedule URL**: https://console.apify.com/schedules/7A6c15ixwldghb0bh

---

## 🎯 Use Cases

### For Swing Traders:
- ✅ Buy dips with positive sentiment
- ✅ Sell spikes with negative sentiment
- ✅ Get WhatsApp alerts for signal changes
- ✅ Know when Trump affects your stocks

### For Risk Management:
- ✅ Trump tariff early warnings
- ✅ Policy change detection
- ✅ Sentiment shift alerts
- ✅ Political risk quantification

### For Portfolio Monitoring:
- ✅ Track multiple tickers (3+)
- ✅ Hourly automated analysis
- ✅ Mobile notifications
- ✅ Zero manual effort

---

## 🛠️ Tech Stack

- **Apify Platform**: Actor framework, scheduling, storage
- **Python 3.11**: Core logic
- **OpenAI GPT-4**: Sentiment analysis and signal generation
- **BeautifulSoup + httpx**: Web scraping
- **Twilio**: WhatsApp notifications

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[WHATSAPP_SETUP.md](WHATSAPP_SETUP.md)** - Configure mobile notifications
- **[TRUTH_SOCIAL_INTEGRATION.md](TRUTH_SOCIAL_INTEGRATION.md)** - Trump sentiment analysis
- **[NOTIFICATIONS_COMPLETE.md](NOTIFICATIONS_COMPLETE.md)** - Full notification guide
- **[COMPLETE_FEATURES.md](COMPLETE_FEATURES.md)** - All features explained
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment instructions
- **[SCHEDULE_SETUP.md](SCHEDULE_SETUP.md)** - Scheduling guide

---

## 🏆 Hackathon Highlights

### Innovation:
- 🥇 **First** trading agent with Trump sentiment analysis
- 🥇 **First** to combine News + Reddit + Truth Social
- 🥇 **WhatsApp** instant notifications for traders

### Technical Excellence:
- ✅ Clean, modular architecture
- ✅ Apify-native implementation
- ✅ Fault-tolerant with fallbacks
- ✅ Production-ready code

### Business Value:
- ✅ Solves real problem (market timing)
- ✅ Saves trader time (automated)
- ✅ Provides trading edge (early signals)
- ✅ Quantifies political risk (Trump factor)

---

## 📊 Reddit Communities

Analyzes sentiment from **4 major investing subreddits** (25M+ combined members):

1. **r/wallstreetbets** (15M+) - Meme stocks, options, YOLO plays
2. **r/stocks** (5M+) - General stock discussion, DD
3. **r/investing** (2M+) - Long-term investing, fundamentals
4. **r/StockMarket** (2M+) - Daily market discussion, TA

---

## 📅 Scheduling

**Current schedule** (Hourly):
- Cron: `0 * * * *`
- Timezone: America/Chicago (CST)
- Status: ✅ ENABLED

**Alternative schedules**:
```bash
# Market hours only (9am-4pm Mon-Fri)
0 9-16 * * 1-5

# Twice daily (6am & 1pm)
0 6,13 * * *

# Every 2 hours
0 */2 * * *
```

**Edit schedule**: https://console.apify.com/schedules/7A6c15ixwldghb0bh

---

## 💰 Cost

### Per Run (3 tickers):
- Apify compute: ~$0.02 (4-5 min on 4GB memory)
- OpenAI API: ~$0.01 (GPT-4 calls)
- WhatsApp: FREE (Twilio $15 credit)
- **Total**: ~$0.03 per run

### Monthly:
- **24/7 Hourly**: ~$22/month
- **Market hours only**: ~$5/month
- **Twice daily**: ~$2/month

---

## 🔒 Security

- ✅ API keys stored as encrypted secrets
- ✅ WhatsApp credentials protected
- ✅ No sensitive data logged
- ✅ Follows Apify security best practices

---

## 📝 Example Use Case

**Morning routine**:
```
06:00 - Actor runs, analyzes overnight news
06:04 - Signal change detected: NVDA HOLD → BUY
06:05 - 📱 WhatsApp notification received
07:00 - Review reasoning on Apify console
09:30 - Market opens, execute BUY order
        Entry: $135, Target: $155, Stop: $128
16:00 - Actor runs again
16:04 - Signal change: NVDA BUY → SELL
16:05 - 📱 WhatsApp: "Take profits!"
16:10 - Sell at $154 (+14% gain!)
```

---

## 🏆 Built For

**Apify 1M Challenge Hackathon**

**Key Differentiators**:
1. Only agent tracking Trump for trading
2. Multi-source intelligence (4 sources)
3. WhatsApp mobile notifications
4. AI-powered with reasoning
5. Fully automated on Apify

---

## 🔗 Links

- **Apify Actor**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
- **Schedule**: https://console.apify.com/schedules/7A6c15ixwldghb0bh
- **GitHub**: https://github.com/techstar9797/AgenticStockActor
- **Apify 1M Challenge**: https://apify.notion.site/apify-1m-challenge-hackathon

---

## 🤝 Credits

**Built by**: Sachin Keswani  
**Email**: sachin.news@gmail.com  
**Hackathon**: Apify 1M Challenge  
**Date**: December 2025  

---

## 📄 License

MIT License - See LICENSE file

---

**Made with ❤️ for swing traders everywhere. Get WhatsApp alerts and never miss a trade! 🚀📱**
