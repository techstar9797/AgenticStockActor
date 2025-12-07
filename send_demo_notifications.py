#!/usr/bin/env python3
"""
Standalone demo script - Send all signal change scenarios to WhatsApp
Run this to demonstrate all possible signal transitions for hackathon!
"""
import asyncio
import httpx

# Your Twilio credentials - Replace with yours
ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"  # e.g., "AC38ed..."
AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"  # From Twilio console
FROM_NUMBER = "whatsapp:+14155238886"  # Twilio WhatsApp sandbox number
TO_NUMBER = "whatsapp:+YOUR_PHONE_NUMBER"  # Your WhatsApp number


async def send_whatsapp(message: str, scenario_name: str):
    """Send a WhatsApp message via Twilio"""
    url = f'https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json'
    
    data = {
        'From': FROM_NUMBER,
        'To': TO_NUMBER,
        'Body': message
    }
    
    try:
        async with httpx.AsyncClient(auth=(ACCOUNT_SID, AUTH_TOKEN), timeout=30.0) as client:
            response = await client.post(url, data=data)
            
            if response.status_code in [200, 201]:
                print(f"✅ {scenario_name}")
                return True
            else:
                print(f"❌ {scenario_name}: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ {scenario_name}: {str(e)}")
        return False


async def main():
    print("🎬 DEMO: Sending 8 Signal Change Scenarios to WhatsApp")
    print(f"📱 Target: {TO_NUMBER}\n")
    
    scenarios = [
        (
            "1. HOLD → BUY (Buy the Dip)",
            """🟢 BUY SIGNAL: AAPL

From: HOLD → BUY
Confidence: 85%

💰 $275.50 (-1.2%)
💭 +0.68
🎯 85%

📝 Reason:
Price dipped 3% while positive 
sentiment on AI partnership news. 
Classic buy-the-dip opportunity 
with strong fundamentals.

Entry: Below $278
Stop: $268
Target: $295

🕐 Demo Time"""
        ),
        (
            "2. WATCH → SELL (Risk Confirmed)",
            """🔴 SELL SIGNAL: MSFT

From: WATCH → SELL
Confidence: 78%

💰 $442.30 (-2.5%)
💭 -0.55
🎯 78%

📝 Reason:
Negative news on regulatory 
investigation confirmed. Sentiment 
turned negative. Exit position to 
avoid further downside.

Exit: Current price
Avoid: Holding through inquiry

🕐 Demo Time"""
        ),
        (
            "3. BUY → SELL (Emergency Exit)",
            """🚨 URGENT: NVDA

From: BUY → SELL
Confidence: 90%

💰 $188.75 (+1.2%)
💭 -0.62
🎯 90%

📝 COMPLETE REVERSAL!
Earnings miss + negative guidance.
Exit all positions immediately.

Sentiment shift: +0.75 → -0.62
Price: Take any profits available
Risk: HIGH

🕐 Demo Time"""
        ),
        (
            "4. HOLD → SELL (Take Profits)",
            """🔴 SELL SIGNAL: GOOGL

From: HOLD → SELL
Confidence: 72%

💰 $195.80 (+0.8%)
💭 -0.45
🎯 72%

📝 Reason:
Negative legal ruling combined 
with profit-taking. Price at 
resistance. Good time to exit.

Exit: $195-196 range
Re-entry: Wait for $185

🕐 Demo Time"""
        ),
        (
            "5. WATCH → BUY (Entry Confirmed)",
            """🟢 BUY SIGNAL: META

From: WATCH → BUY
Confidence: 88%

💰 $612.40 (+2.3%)
💭 +0.75
🎯 88%

📝 OPPORTUNITY CONFIRMED!
Strong earnings beat exceeded 
expectations. Positive sentiment 
validated. High conviction entry.

Entry: Current to $615
Stop: $595
Target: $650

🕐 Demo Time"""
        ),
        (
            "6. HOLD → WATCH (Escalating)",
            """🔵 WATCH SIGNAL: AMZN

From: HOLD → WATCH
Confidence: 65%

💰 $218.90 (+0.5%)
💭 +0.52
🎯 65%

📝 Reason:
Growing positive sentiment on 
cloud growth. Not quite BUY yet 
but monitor closely for entry.

Watch for: Volume increase
Entry trigger: Above $220

🕐 Demo Time"""
        ),
        (
            "7. Trump Direct Mention",
            """🚨 URGENT: TSLA

From: HOLD → BUY
Confidence: 92%

💰 $455.00 (+1.8%)
💭 +0.84
🎯 92%

📝 Reason:
Strong positive sentiment...

📱 TRUMP IMPACT: HIGH
🚨 TSLA DIRECTLY MENTIONED!
Trump Sentiment: +0.95

Post: "Tesla doing incredible 
work on American manufacturing. 
Great American company!"

Policy: Domestic production support
Market Impact: Strong positive

Entry: Below $460
Target: $495

🕐 Demo Time"""
        ),
        (
            "8. Trump Tariff Alert",
            """🚨 URGENT: AAPL

From: BUY → SELL
Confidence: 95%

💰 $278.00 (-1.5%)
💭 -0.68
🎯 95%

📝 COMPLETE REVERSAL!

📱 TRUMP IMPACT: HIGH
⚠️ TARIFF ANNOUNCEMENT!
Trump Sentiment: -0.85

Post: "25% tariffs on Chinese 
electronics effective immediately!"

Impact: Apple produces in China
Cost increase expected

Exit: IMMEDIATELY
Avoid: Holding through tariffs

🕐 Demo Time"""
        )
    ]
    
    for name, message in scenarios:
        success = await send_whatsapp(message, name)
        await asyncio.sleep(2)  # Rate limiting
    
    print(f"\n🎉 Demo complete! Check WhatsApp: {TO_NUMBER}")
    print(f"\nSent {len(scenarios)} different signal change examples!")
    print("\nNow you can show:")
    print("1. HOLD → BUY (buy dip)")
    print("2. WATCH → SELL (risk confirmed)")
    print("3. BUY → SELL (reversal)")
    print("4. HOLD → SELL (take profits)")
    print("5. WATCH → BUY (entry confirmed)")
    print("6. HOLD → WATCH (escalating)")
    print("7. Trump direct mention")
    print("8. Trump tariff alert")


if __name__ == '__main__':
    asyncio.run(main())

