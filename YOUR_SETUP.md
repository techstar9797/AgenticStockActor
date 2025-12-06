# 📱 YOUR WHATSAPP SETUP - Sachin Keswani

## ✅ Your Twilio Account Info

**Phone Number**: +1 (858) 699-8271  
**Twilio WhatsApp**: whatsapp:+14155238886  
**Account SID**: `AC38ed...` (see Twilio console)  
**Auth Token**: Get from https://console.twilio.com

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Join WhatsApp Sandbox

1. Open WhatsApp on your phone
2. **Send this message**:
   ```
   join <your-code>
   ```
   **To**: +1 (415) 523-8886 (Twilio WhatsApp number)
   
3. **Wait** for welcome message from Twilio
4. You're connected! ✅

### Step 2: Get Your Auth Token

1. Go to: https://console.twilio.com
2. Click **"Show"** next to Auth Token
3. **Copy** the token (starts with lowercase letters/numbers)

### Step 3: Update Apify Schedule

1. Go to: https://console.apify.com/schedules/7A6c15ixwldghb0bh
2. Click **"Edit"**
3. **Replace the input** with:

```json
{
  "tickers": ["AAPL", "TSLA", "NVDA"],
  "openaiApiKey": "YOUR_OPENAI_KEY",
  
  "whatsappNumber": "+18586998271",
  "twilioAccountSid": "YOUR_TWILIO_ACCOUNT_SID",
  "twilioAuthToken": "YOUR_TWILIO_AUTH_TOKEN",
  "enableNotifications": true,
  
  "maxNewsPerTicker": 20,
  "maxRedditPostsPerTicker": 50,
  "maxTrumpPosts": 20
}
```

4. **Replace** `"PASTE_YOUR_AUTH_TOKEN_HERE"` with your actual token
5. Click **"Save"**

---

## 🧪 Test It Right Now!

### Quick Test:

```bash
cd /Users/sachinkeswani/AgenticStockActor

# 1. Edit test_input_whatsapp.json and add your auth token
# 2. Run this:
apify call luxurious_gel/agentic-stock-actor --input-file=test_input_whatsapp.json
```

**Wait ~5 minutes**, then check your WhatsApp! 📱

---

## 📱 What You'll Receive

### First Run (Baseline):
- No WhatsApp messages (establishing baseline)
- Check console logs to verify it's working

### Second Run Onwards (When Signals Change):
```
🚨 URGENT SIGNAL CHANGE: AAPL

🟡 Previous: HOLD
🟢 *NEW: BUY*

💰 $182.50
💭 +0.68
🎯 85%

Strong positive sentiment from 
partnership while price dipped...

📱 TRUMP IMPACT: MEDIUM
Trump mentioned AI sector

Entry: Below $185
Stop: $175

🕐 14:00 UTC
```

---

## ⏰ When You'll Get Notified

### Your schedule runs every hour at:
```
12:00, 13:00, 14:00, 15:00, 16:00, etc. (CST)
```

### You get WhatsApp when:
- ✅ **BUY → SELL** (urgent: exit position!)
- ✅ **SELL → BUY** (urgent: buy opportunity!)
- ✅ **HOLD → BUY** (time to enter!)
- ✅ **HOLD → SELL** (time to exit!)
- ✅ **HOLD → WATCH** (escalating situation)
- ✅ **WATCH → BUY** (opportunity confirmed)
- ✅ **Trump mentions** your ticker (HIGH impact)

---

## 🔍 Find Your Auth Token

### Option 1: Twilio Console
1. Visit: https://console.twilio.com
2. See "Account Info" section on dashboard
3. Account SID: `AC38ed...` ✅ (from Twilio)
4. Auth Token: Click **"Show"** → Copy it

### Option 2: Account Settings
1. Go to: https://console.twilio.com/us1/account/keys-credentials/api-keys
2. Your "Live Credentials" section
3. Copy Auth Token

---

## ✅ Verification Checklist

Before going live:

- [ ] Joined WhatsApp sandbox (sent "join" message)
- [ ] Received welcome message from Twilio
- [ ] Copied Account SID from Twilio console
- [ ] Copied Auth Token from Twilio console
- [ ] Updated Apify schedule input
- [ ] Saved schedule
- [ ] Waiting for next hourly run

---

## 🎯 Expected Timeline

### Today:
```
15:30 - You set up WhatsApp ✅
16:00 - Next hourly run (baseline established)
17:00 - Second run (notifications active!)
        📱 If signal changed → WhatsApp sent!
```

### Ongoing:
- Every hour at `:00`
- WhatsApp when signals change
- Full AI analysis each time

---

## 📊 Your Current Watchlist

- ✅ **AAPL** (Apple Inc.)
- ✅ **TSLA** (Tesla Inc.)
- ✅ **NVDA** (NVIDIA Corp.)

**To add more**: Edit schedule input, add to `"tickers"` array

---

## 🔗 Your Personal Links

- **Apify Actor**: https://console.apify.com/actors/43ZTkpbPq0YKf3djc
- **Your Schedule**: https://console.apify.com/schedules/7A6c15ixwldghb0bh
- **Twilio Console**: https://console.twilio.com
- **GitHub Repo**: https://github.com/techstar9797/AgenticStockActor

---

## 💡 Pro Tips

### 1. **Test First**
Run actor manually once to verify WhatsApp works before relying on schedule

### 2. **Check Twilio Credit**
- $15 free credit
- ~500 WhatsApp messages
- Monitor at: https://console.twilio.com/us1/billing/usage

### 3. **Sandbox Limitations**
- Join code expires after 72 hours
- Re-join if stopped receiving messages
- Just send "join <code>" again

### 4. **Best Practices**
- Check WhatsApp for urgent signals (BUY/SELL)
- Review full details on Apify console
- Don't trade on low confidence (<70%)
- Always use stop-losses

---

## 🚨 Important Notes

### WhatsApp Format:
- ✅ Your number: `+18586998271` (correct format!)
- ✅ Includes country code (+1)
- ✅ No spaces or dashes

### Twilio Sandbox:
- ✅ Free tier perfect for personal use
- ✅ Works immediately after joining
- ⚠️ Join code expires after 3 days (just re-join)
- ⚠️ Sandbox branding in messages

### For Production:
- Upgrade to WhatsApp Business API
- No join code needed
- Unlimited messages
- Professional branding

---

## 🎉 You're Ready!

Once you add your Auth Token to the schedule:

- ✅ Actor runs every hour
- ✅ Analyzes AAPL, TSLA, NVDA
- ✅ Detects signal changes
- ✅ Sends WhatsApp to +1-858-699-8271
- ✅ You get instant mobile alerts! 📱

**Your edge in the market, delivered to your pocket! 🚀**

---

## 📞 Next Steps

1. **Get Auth Token**: https://console.twilio.com (click "Show")
2. **Update Schedule**: https://console.apify.com/schedules/7A6c15ixwldghb0bh
3. **Wait for next run**: Top of next hour
4. **Check WhatsApp**: Get your first alert! 📱

---

**Let's win this hackathon! 🏆**

