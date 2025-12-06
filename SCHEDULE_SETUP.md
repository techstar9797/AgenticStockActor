# ⏰ Setting Up Hourly Schedule

## Method 1: Via Apify Console (Easiest)

1. **Go to Apify Schedules**: https://console.apify.com/schedules

2. **Click "Create new schedule"**

3. **Configure the schedule**:
   - **Name**: `Agentic Stock Actor - Hourly`
   - **Description**: `Runs every hour to check stock signals and notify on changes`
   - **Cron expression**: `0 * * * *` (every hour on the hour)
   - **Timezone**: `America/Chicago` (CST)

4. **Select Actor**:
   - Actor: `luxurious_gel/agentic-stock-actor`
   - Build: `latest`

5. **Input**:
```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "YOUR_OPENAI_API_KEY_HERE",
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50,
  "subreddits": ["wallstreetbets", "stocks", "investing", "StockMarket"]
}
```

6. **Click "Save"**

---

## Method 2: Via Apify API

```bash
curl https://api.apify.com/v2/schedules \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_APIFY_API_TOKEN" \
  -d '{
    "name": "Agentic Stock Actor - Hourly",
    "isEnabled": true,
    "isExclusive": false,
    "cronExpression": "0 * * * *",
    "timezone": "America/Chicago",
    "actions": [{
      "type": "RUN_ACTOR",
      "actorId": "luxurious_gel/agentic-stock-actor",
      "input": {
        "tickers": ["AAPL", "TSLA", "NVDA"],
        "openaiApiKey": "YOUR_KEY_HERE",
        "maxNewsPerTicker": 20
      }
    }]
  }'
```

---

## Method 3: Via Apify CLI

```bash
# Create schedule.json file first
cat > schedule.json << 'EOF'
{
  "name": "Agentic Stock Actor - Hourly",
  "isEnabled": true,
  "cronExpression": "0 * * * *",
  "timezone": "America/Chicago",
  "actions": [{
    "type": "RUN_ACTOR",
    "actorId": "luxurious_gel/agentic-stock-actor",
    "input": {
      "tickers": ["AAPL", "TSLA", "NVDA"],
      "openaiApiKey": "sk-proj-...",
      "maxNewsPerTicker": 20,
      "maxRedditPostsPerTicker": 50
    }
  }]
}
EOF

# Then create the schedule
apify schedules create < schedule.json
```

---

## Cron Expressions

| Schedule | Cron Expression | Description |
|----------|----------------|-------------|
| **Every hour** | `0 * * * *` | Top of every hour |
| **Every 2 hours** | `0 */2 * * *` | Every 2 hours |
| **Market hours only** | `0 9-16 * * 1-5` | 9am-4pm Mon-Fri (CST) |
| **Pre-market + Market** | `0 6-16 * * 1-5` | 6am-4pm Mon-Fri |
| **Twice daily** | `0 6,13 * * *` | 6am and 1pm daily |

---

## 🔔 How Notifications Work

### First Run
- Actor stores initial signals in key-value store
- No notifications sent (baseline established)

### Subsequent Runs (Every Hour)
- Actor compares new signals vs. stored signals
- **Notification triggers**:
  - `BUY → SELL` or `SELL → BUY` (reversals) 🚨
  - `HOLD → BUY` or `HOLD → SELL` (action signals)
  - `HOLD → WATCH` (escalation)
  - `WATCH → BUY` or `WATCH → SELL`

### Example Notification
```
🚨 URGENT SIGNAL CHANGE ALERT: AAPL

🟡 Previous: HOLD (65% confidence)
🟢 **NEW: BUY** (85% confidence)

Time: 2025-12-06 14:00 UTC
```

---

## Monitor Your Schedule

- **View all runs**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc/runs
- **View schedules**: https://console.apify.com/schedules
- **Notifications history**: Check dataset for `type: "signal_change_notification"`

---

## Cost Estimation

**Per run** (3 tickers):
- Compute: ~$0.02 (4-5 min runtime on 4GB memory)
- API calls: ~$0.01 (OpenAI GPT-4)
- **Total**: ~$0.03 per run

**Hourly** (24 runs/day):
- Daily: $0.72
- Monthly: ~$22

**Optimized** (market hours only, 9am-4pm Mon-Fri):
- ~40 runs/week
- Monthly: ~$5

---

## Recommended Settings

For production use, I recommend:

1. **Market Hours Only**:
   ```
   Cron: 0 9-16 * * 1-5
   Timezone: America/New_York
   ```

2. **Morning + Afternoon Checks**:
   ```
   Cron: 0 6,9,12,15 * * 1-5
   ```

3. **Test Mode** (every hour):
   ```
   Cron: 0 * * * *
   ```

---

## Next Steps

1. ✅ Create schedule via console
2. ✅ Test with 1-2 runs
3. ✅ Monitor signal changes
4. 🔧 Fix Yahoo Finance price extraction
5. 📧 Add email/Slack notifications (optional)

**Schedule URL**: https://console.apify.com/schedules

