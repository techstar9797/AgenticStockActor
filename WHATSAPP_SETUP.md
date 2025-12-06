# 📱 WhatsApp Notifications Setup Guide

## 🎯 Overview

Get **instant WhatsApp alerts** on your phone when trading signals change!

**Example**:
```
🚨 URGENT SIGNAL CHANGE: TSLA

🟡 Previous: HOLD
🟢 *NEW: BUY*

💰 Price: $378.50
💭 Sentiment: +0.72
🎯 Confidence: 85%

📝 Reason:
Strong positive sentiment from Trump's 
praise of Tesla's American manufacturing...

🚨 TRUMP IMPACT: HIGH
⚠️ TSLA DIRECTLY MENTIONED!
Trump Sentiment: +0.90
Policy: Domestic production support

🕐 14:00 UTC
```

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Free Twilio Account

1. **Sign up**: https://www.twilio.com/try-twilio
2. **Get $15 free credit** (enough for ~500 messages!)
3. **Note these credentials**:
   - Account SID (starts with `AC...`)
   - Auth Token
   - WhatsApp Sandbox Number

### Step 2: Activate WhatsApp Sandbox

1. Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. **Send WhatsApp message** to join:
   - Send: `join <your-code>` 
   - To: Twilio's WhatsApp number
   - From: Your WhatsApp number
3. **Confirm** you receive welcome message

### Step 3: Update Actor Input

Add to your actor input:

```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "YOUR_OPENAI_KEY",
  
  "whatsappNumber": "+15551234567",
  "twilioAccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "twilioAuthToken": "your_auth_token_here",
  "enableNotifications": true
}
```

### Step 4: Test It!

Run the actor and check your WhatsApp! 📱

---

## 📋 Detailed Setup Instructions

### Option 1: Twilio WhatsApp (Free Tier - Recommended)

**Best for**: Testing, MVP, personal use

**Limits**:
- ✅ Free $15 credit
- ✅ ~500 messages included
- ✅ Easy setup (5 minutes)
- ⚠️  Sandbox mode (join code required)
- ⚠️  Single phone number

**Steps**:

1. **Create Twilio Account**:
   - Visit: https://www.twilio.com/try-twilio
   - Sign up with email
   - Verify phone number
   - Get $15 free credit

2. **Get Credentials**:
   - Dashboard: https://console.twilio.com
   - Copy "Account SID" (AC...)
   - Click "Show" for Auth Token
   - Save both securely

3. **Activate WhatsApp Sandbox**:
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - See your sandbox number (e.g., +1 415 523 8886)
   - See your join code (e.g., "join <random-words>")

4. **Join from Your Phone**:
   - Open WhatsApp
   - Send message: `join <your-code>`
   - To: Twilio's sandbox number
   - Receive: Welcome message (you're connected!)

5. **Test Connection**:
   - Click "Send a test message" in Twilio console
   - Receive on your phone (confirms it works!)

6. **Add to Actor**:
   - Go to: https://console.apify.com/schedules/7A6c15ixwldghb0bh
   - Edit input
   - Add WhatsApp fields
   - Save

### Option 2: WhatsApp Business API (Production)

**Best for**: Production, multiple users, business use

**Benefits**:
- ✅ Official WhatsApp Business account
- ✅ Unlimited messages
- ✅ Multiple recipients
- ✅ Rich media support
- ⚠️  Requires business verification
- ⚠️  More complex setup

**Steps**:

1. **Apply for WhatsApp Business API**:
   - Via: Facebook Business Manager
   - Or: Through providers like Twilio, MessageBird

2. **Get Verified**:
   - Submit business documents
   - Verify phone number
   - Wait for approval (1-2 weeks)

3. **Get API Credentials**:
   - Access Token
   - Phone Number ID
   - Business Account ID

4. **Update Actor** (requires code modification for Business API)

---

## 🔧 Configuration

### Input Schema:

```json
{
  "whatsappNumber": "+15551234567",
  "twilioAccountSid": "ACxxxxx...",
  "twilioAuthToken": "your_token",
  "enableNotifications": true
}
```

### Multiple Recipients (Future):

```json
{
  "whatsappNumbers": [
    "+15551111111",
    "+15552222222"
  ]
}
```

---

## 📱 Message Format

### Signal Change Alert:

```
🚨 URGENT SIGNAL CHANGE: AAPL

🟡 Previous: HOLD (65% confidence)
🟢 *NEW: BUY* (85% confidence)

💰 Price: $182.50
💭 Sentiment: +0.68
🎯 Confidence: 85%

📝 Reason:
Strong positive sentiment from AI partnership
announcement while price dipped 2% below recent
high. Excellent swing trade entry point.

🕐 14:00 UTC
```

### With Trump Impact:

```
🚨 URGENT SIGNAL CHANGE: TSLA

🟡 Previous: HOLD
🟢 *NEW: BUY*

💰 Price: $378.50
💭 Sentiment: +0.72
🎯 Confidence: 90%

📝 Reason:
Strong positive sentiment from Trump's praise...

📱 TRUMP IMPACT: HIGH
🚨 TSLA DIRECTLY MENTIONED!
Trump Sentiment: +0.90
Policy: Domestic production support

🕐 13:00 UTC
```

### Daily Summary (Optional):

```
📊 DAILY STOCK SUMMARY

Changes today: 3

🟢 AAPL: BUY (85%)
🔴 TSLA: SELL (78%)
🟡 NVDA: HOLD (60%)

🕐 2025-12-06 16:00 UTC

View details: console.apify.com
```

---

## 💰 Cost

### Twilio Pricing:

- **Sandbox (Free tier)**: FREE with $15 credit
  - ~500 messages included
  - Perfect for personal use

- **Production (WhatsApp Business API)**:
  - User-initiated: FREE
  - Business-initiated: $0.005-0.01 per message
  - ~$0.50/month for hourly notifications

### Your Expected Costs:

**Hourly schedule** (24 runs/day):
- ~3-6 signal changes per day
- ~100-180 WhatsApp messages/month
- **Cost**: FREE (within $15 credit)

**After free credit**:
- ~$0.50-1.00/month

---

## 🔔 What You'll Receive

### High-Priority (Immediate):
- `BUY → SELL` (exit now!)
- `SELL → BUY` (buy now!)
- `HOLD → BUY` (enter position!)
- `HOLD → SELL` (exit position!)

### Medium Priority:
- `HOLD → WATCH` (monitor closely)
- `WATCH → BUY` (entry confirmed)
- `WATCH → SELL` (risk confirmed)

### Trump Alerts:
- Direct ticker mention (HIGH priority)
- Tariff announcements
- Policy implications
- Trade deal news

---

## 🎯 Example Use Cases

### Use Case 1: Morning Trader

**Setup**:
- Hourly notifications enabled
- Check phone before market open

**Workflow**:
```
06:00 - Wake up, check WhatsApp
        📱 "AAPL: HOLD → BUY"
        
07:00 - Review reasoning on Apify console
        
09:30 - Market opens, execute BUY order
        
Throughout day - Get alerts as signals change
```

### Use Case 2: Busy Professional

**Setup**:
- Only urgent notifications
- Check periodically

**Workflow**:
```
Only receive messages for BUY/SELL signals
Don't need HOLD/WATCH updates
Quick glance during breaks
```

### Use Case 3: Trump Watcher

**Setup**:
- All notifications
- Focus on Trump impact

**Workflow**:
```
Get alerted when Trump mentions stocks
Quick reaction before market catches up
Exit before tariff impact materializes
```

---

## 🔧 Troubleshooting

### Not Receiving Messages:

**Check 1**: Twilio credentials correct?
- Go to: https://console.twilio.com
- Verify Account SID and Auth Token
- Try test message in Twilio console

**Check 2**: Joined WhatsApp sandbox?
- Send: `join <code>` to Twilio's number
- Receive welcome message
- If not received, re-join

**Check 3**: Phone number format?
- Must include country code
- Format: `+15551234567` (with +)
- No spaces, dashes, or parentheses

**Check 4**: Actor input correct?
- Go to schedule input
- Verify all 3 fields:
  - `whatsappNumber`
  - `twilioAccountSid`
  - `twilioAuthToken`

**Check 5**: Notifications enabled?
- `enableNotifications: true`

**Check 6**: Signals actually changed?
- No changes = no notifications (normal!)

### Messages Delayed:

- **Cause**: Twilio queue or network delay
- **Normal**: 5-30 seconds delivery time
- **Solution**: No action needed

### Error in Logs:

```
❌ WhatsApp notification failed: <error>
```

**Solutions**:
1. Check Twilio account balance
2. Verify credentials
3. Check phone number format
4. Re-join sandbox if expired

---

## 🎨 Customization

### Modify Message Format:

Edit `src/notifications/whatsapp.py`:

```python
def _format_message(...):
    # Customize your message format
    message = f"""
🔔 {ticker} ALERT!

Signal: {current_signal}
Price: ${price}
Confidence: {confidence:.0%}

{reasoning[:150]}
"""
    return message
```

### Add Media (Images/Charts):

```python
# Send with image
data = {
    'From': self.from_number,
    'To': to_number,
    'Body': message,
    'MediaUrl': 'https://your-chart-url.com/chart.png'
}
```

---

## 📊 Advanced Features

### 1. Quiet Hours (Future Enhancement)

```python
# Don't send between 11 PM - 7 AM
from datetime import time

quiet_start = time(23, 0)  # 11 PM
quiet_end = time(7, 0)     # 7 AM

if not (quiet_start <= current_time <= quiet_end):
    await send_whatsapp(...)
```

### 2. Importance Filtering

```python
# Only send if confidence > 70%
if confidence >= 0.70:
    await send_whatsapp(...)
```

### 3. Batch Daily Summary

```python
# Send once daily at 4 PM with all changes
await whatsapp.send_daily_summary(
    to_number="+15551234567",
    signals=all_signals,
    changes_count=len(changes)
)
```

---

## 🎯 Testing Your Setup

### Test Message Command:

```bash
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/YOUR_ACCOUNT_SID/Messages.json" \
  --data-urlencode "From=whatsapp:+14155238886" \
  --data-urlencode "To=whatsapp:+15551234567" \
  --data-urlencode "Body=🚀 Test from Agentic Stock Actor!" \
  -u YOUR_ACCOUNT_SID:YOUR_AUTH_TOKEN
```

### Test via Actor:

1. Update schedule input with WhatsApp credentials
2. Wait for next hourly run
3. Manually change a signal (for testing):
   - Edit key-value store
   - Force a signal change
4. Next run will send notification

---

## 💡 Best Practices

### Do's:
- ✅ Test with Twilio sandbox first
- ✅ Keep credentials secure (use Apify secrets)
- ✅ Monitor Twilio usage dashboard
- ✅ Set up billing alerts
- ✅ Save important notifications

### Don'ts:
- ❌ Don't share Twilio credentials
- ❌ Don't spam (respect rate limits)
- ❌ Don't send to unverified numbers (production)
- ❌ Don't exceed free tier without budget

---

## 📈 Message Examples by Scenario

### BUY Signal Alert:

```
🟢 BUY SIGNAL: AAPL

From: HOLD → BUY
Confidence: 85%

💰 $182.50 (-1.2%)
💭 Sentiment: +0.68

AI says: "Price dipped while sentiment 
improved. Classic buy opportunity!"

Entry: Below $185
Stop: $175
Target: $200

🕐 14:00 UTC
```

### SELL Signal Alert:

```
🔴 SELL SIGNAL: TSLA

From: BUY → SELL
Confidence: 90%

💰 $420.00 (+3.5%)
💭 Sentiment: -0.45

AI says: "Price spiked but sentiment 
turned negative. Take profits now."

Exit: Current price
Avoid: Holding through correction

🕐 11:00 UTC
```

### Trump Impact Alert:

```
🚨 TRUMP ALERT: NVDA

Signal: WATCH → BUY

📱 Trump posted about AI:
"AI is the future! American companies
leading the charge!"

Impact: MEDIUM (0.7x weight)
Sentiment boost: +0.30

Combined with positive earnings:
WATCH → BUY (75% confidence)

🕐 15:00 UTC
```

---

## 🔐 Security

### Storing Credentials Securely:

**Option 1**: Apify Secrets (Recommended)
1. Go to: https://console.apify.com/account/integrations
2. Create new secret
3. Reference in input: `SECRET_NAME`

**Option 2**: Environment Variables
```json
{
  "twilioAccountSid": "{{TWILIO_SID}}",
  "twilioAuthToken": "{{TWILIO_TOKEN}}"
}
```

**Option 3**: Actor Input (Encrypted)
- Mark fields as `isSecret: true` in schema
- Apify encrypts automatically

---

## 📞 Phone Number Format

### Correct Formats:

✅ `+15551234567` (US)
✅ `+442012345678` (UK)
✅ `+919876543210` (India)
✅ `+4915123456789` (Germany)

### Incorrect Formats:

❌ `15551234567` (missing +)
❌ `+1 555 123 4567` (has spaces)
❌ `+1-555-123-4567` (has dashes)
❌ `(555) 123-4567` (no country code)

---

## 🌍 International Support

### Twilio WhatsApp is available in:

- 🇺🇸 United States
- 🇬🇧 United Kingdom
- 🇨🇦 Canada
- 🇦🇺 Australia
- 🇮🇳 India
- 🇩🇪 Germany
- 🇫🇷 France
- 🇧🇷 Brazil
- And 180+ more countries!

**Check availability**: https://www.twilio.com/guidelines/whatsapp

---

## 🎓 Advanced Configuration

### Send to Multiple Numbers:

Edit `src/notifications/whatsapp.py`:

```python
async def send_to_multiple(self, numbers: List[str], message: str):
    """Send to multiple WhatsApp numbers"""
    for number in numbers:
        await self._send_twilio_message(number, message)
        await asyncio.sleep(1)  # Rate limiting
```

### Custom Message Templates:

```python
def _format_buy_signal(self, data):
    return f"""🟢 BUY {data['ticker']}!
    
Entry: ${data['price']:.2f}
Target: ${data['target']:.2f}
Stop: ${data['stop']:.2f}

{data['reasoning'][:100]}"""

def _format_sell_signal(self, data):
    return f"""🔴 SELL {data['ticker']}!
    
Exit: ${data['price']:.2f}
Profit: {data['profit_pct']:.1%}

{data['reasoning'][:100]}"""
```

---

## 📊 Monitoring

### Track WhatsApp Usage:

**Twilio Dashboard**:
- Messages sent: https://console.twilio.com/us1/monitor/logs/messages
- Usage & costs: https://console.twilio.com/us1/billing/usage
- Error logs: https://console.twilio.com/us1/monitor/logs/debugger

### Actor Logs:

Look for:
```
✅ WhatsApp sent to +15551234567: AAPL HOLD→BUY
```

Or:
```
❌ Failed to send WhatsApp to +15551234567
```

---

## 🚨 Limitations & Workarounds

### Twilio Sandbox Limitations:

**Limitation**: Join code expires after 72 hours
**Workaround**: Re-send join message every 3 days

**Limitation**: Only approved numbers receive messages
**Workaround**: Each recipient must join sandbox

**Limitation**: Sandbox branding in messages
**Workaround**: Upgrade to WhatsApp Business API

### Message Length:

**Limit**: 1,600 characters per message
**Solution**: Truncate reasoning to 200 chars

### Rate Limits:

**Limit**: 1 message per second
**Solution**: Built-in delays between messages

---

## 🎯 Example Actor Input (Complete)

```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  
  "openaiApiKey": "sk-proj-...",
  
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50,
  "maxTrumpPosts": 20,
  
  "subreddits": [
    "wallstreetbets",
    "stocks",
    "investing",
    "StockMarket"
  ],
  
  "whatsappNumber": "+15551234567",
  "twilioAccountSid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "twilioAuthToken": "your_auth_token_here",
  "enableNotifications": true
}
```

---

## ✅ Verification Checklist

Before going live:

- [ ] Twilio account created
- [ ] $15 free credit received
- [ ] Account SID copied
- [ ] Auth Token copied
- [ ] WhatsApp sandbox activated
- [ ] Join code sent from your phone
- [ ] Welcome message received
- [ ] Test message sent successfully
- [ ] Credentials added to actor input
- [ ] `enableNotifications: true`
- [ ] Phone number format verified (+country code)
- [ ] Schedule updated with new input
- [ ] Test run completed
- [ ] WhatsApp notification received! 📱

---

## 🎬 Demo for Hackathon

### Show This Flow:

1. **Setup**: "I added my WhatsApp number to the actor"
2. **Run**: "Actor analyzes stocks every hour"
3. **Change**: "AAPL signal changed from HOLD to BUY"
4. **Notification**: *Show WhatsApp message on phone screen*
5. **Action**: "I got instant alert and made the trade!"

### Key Points:

- ✅ **Instant**: Notifications within seconds
- ✅ **Mobile**: Always have your phone
- ✅ **Rich**: Emoji formatting, clear structure
- ✅ **Actionable**: Price, confidence, reasoning included
- ✅ **Trump Factor**: Political risk quantified

---

## 🚀 Future Enhancements

### Phase 2:
- [ ] Rich media (charts, graphs)
- [ ] Interactive buttons ("Buy", "Ignore")
- [ ] Location-based (only during market hours)
- [ ] Group notifications (share with friends)
- [ ] Custom alert preferences per ticker

### Phase 3:
- [ ] Two-way communication ("What's AAPL status?")
- [ ] Voice messages (AI-generated summary)
- [ ] Video clips (chart analysis)
- [ ] Live chat with AI agent

---

## 🎉 You're All Set!

Once configured, you'll receive:

- 📱 **Instant WhatsApp alerts** when signals change
- 🚨 **Urgent notifications** for BUY→SELL reversals
- 📊 **Trump impact** included in messages
- 💡 **AI reasoning** for every signal
- 🎯 **Entry strategies** right on your phone

**Never miss a trading opportunity again! 🚀**

---

## 📞 Quick Links

- **Twilio Signup**: https://www.twilio.com/try-twilio
- **Twilio Console**: https://console.twilio.com
- **WhatsApp Sandbox**: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
- **Twilio Docs**: https://www.twilio.com/docs/whatsapp
- **Your Schedule**: https://console.apify.com/schedules/7A6c15ixwldghb0bh

---

**Built for**: Apify 1M Challenge Hackathon  
**Feature**: WhatsApp Notifications  
**Status**: ✅ IMPLEMENTED & READY  
**Next**: Configure your Twilio account and start receiving alerts!

