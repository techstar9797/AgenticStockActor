#!/usr/bin/env python3
"""
Demo script to simulate different signal change scenarios for hackathon presentation.
Shows all possible signal transitions with WhatsApp notifications.
"""
import asyncio
import sys
sys.path.insert(0, '/Users/sachinkeswani/AgenticStockActor')

from src.notifications.whatsapp import WhatsAppNotifier

# Your Twilio credentials - Replace with yours
ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"  # e.g., "AC38ed..."
AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"  # From Twilio console
YOUR_WHATSAPP = "+YOUR_PHONE_NUMBER"  # Your WhatsApp number


async def demo_all_scenarios():
    """Send demo WhatsApp notifications for all signal change scenarios"""
    
    notifier = WhatsAppNotifier(ACCOUNT_SID, AUTH_TOKEN)
    
    print("🎬 Sending demo scenarios to WhatsApp...")
    print(f"📱 Target: {YOUR_WHATSAPP}\n")
    
    scenarios = [
        {
            'name': '1. HOLD → BUY (Dip Buying Opportunity)',
            'ticker': 'AAPL',
            'previous': 'HOLD',
            'current': 'BUY',
            'confidence': 0.85,
            'price': 275.50,
            'sentiment': 0.68,
            'reasoning': 'Price dipped 3% while positive sentiment on AI partnership news. Classic buy-the-dip opportunity with strong fundamentals.',
            'trump_impact': None
        },
        {
            'name': '2. WATCH → SELL (Risk Confirmed)',
            'ticker': 'MSFT',
            'previous': 'WATCH',
            'current': 'SELL',
            'confidence': 0.78,
            'price': 442.30,
            'sentiment': -0.55,
            'reasoning': 'Negative news on regulatory investigation confirmed. Sentiment turned negative. Exit position to avoid further downside.',
            'trump_impact': None
        },
        {
            'name': '3. BUY → SELL (Complete Reversal)',
            'ticker': 'NVDA',
            'previous': 'BUY',
            'current': 'SELL',
            'confidence': 0.90,
            'price': 188.75,
            'sentiment': -0.62,
            'reasoning': 'Major sentiment shift from positive to negative due to earnings miss. Strong reversal signal - exit immediately.',
            'trump_impact': None
        },
        {
            'name': '4. HOLD → SELL (Take Profits)',
            'ticker': 'GOOGL',
            'previous': 'HOLD',
            'current': 'SELL',
            'confidence': 0.72,
            'price': 195.80,
            'sentiment': -0.45,
            'reasoning': 'Negative legal ruling combined with profit-taking. Price at resistance. Good time to exit positions.',
            'trump_impact': None
        },
        {
            'name': '5. WATCH → BUY (Entry Confirmed)',
            'ticker': 'META',
            'previous': 'WATCH',
            'current': 'BUY',
            'confidence': 0.88,
            'price': 612.40,
            'sentiment': 0.75,
            'reasoning': 'Strong earnings beat exceeded expectations. Positive sentiment confirmed. High conviction entry point.',
            'trump_impact': None
        },
        {
            'name': '6. HOLD → WATCH (Escalating)',
            'ticker': 'AMZN',
            'previous': 'HOLD',
            'current': 'WATCH',
            'confidence': 0.65,
            'price': 218.90,
            'sentiment': 0.52,
            'reasoning': 'Growing positive sentiment on cloud growth. Not quite BUY yet but monitor closely for entry opportunity.',
            'trump_impact': None
        },
        {
            'name': '7. WITH TRUMP IMPACT (Direct Mention)',
            'ticker': 'TSLA',
            'previous': 'HOLD',
            'current': 'BUY',
            'confidence': 0.92,
            'price': 455.00,
            'sentiment': 0.84,
            'reasoning': 'Trump directly praised Tesla for American manufacturing excellence. Significant positive catalyst combined with strong technical setup.',
            'trump_impact': {
                'impact_level': 'high',
                'ticker_mentioned': True,
                'sentiment_score': 0.95,
                'key_themes': ['American Manufacturing', 'Electric Vehicles', 'Job Creation'],
                'policy_implications': ['Support for domestic EV production', 'Potential tax incentives']
            }
        },
        {
            'name': '8. TRUMP TARIFF IMPACT',
            'ticker': 'AAPL',
            'previous': 'BUY',
            'current': 'SELL',
            'confidence': 0.95,
            'price': 278.00,
            'sentiment': -0.68,
            'reasoning': 'Trump announced 25% tariffs on Chinese electronics. Apple heavily impacted. Immediate exit recommended before market fully prices in cost implications.',
            'trump_impact': {
                'impact_level': 'high',
                'ticker_mentioned': False,
                'sentiment_score': -0.85,
                'key_themes': ['Tariffs', 'China Trade', 'Electronics'],
                'policy_implications': ['25% import tariffs on electronics', 'Supply chain cost increase']
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. Sending: {scenario['name']}")
        
        success = await notifier.send_signal_change_alert(
            to_number=YOUR_WHATSAPP,
            ticker=scenario['ticker'],
            previous_signal=scenario['previous'],
            current_signal=scenario['current'],
            confidence=scenario['confidence'],
            price=scenario['price'],
            sentiment=scenario['sentiment'],
            reasoning=scenario['reasoning'],
            trump_impact=scenario['trump_impact']
        )
        
        if success:
            print(f"   ✅ Sent to WhatsApp")
        else:
            print(f"   ❌ Failed")
        
        # Wait between messages to avoid rate limiting
        await asyncio.sleep(2)
    
    await notifier.close()
    
    print(f"\n🎉 Demo complete! Check your WhatsApp for {len(scenarios)} example notifications!")
    print("\nScenarios demonstrated:")
    for i, s in enumerate(scenarios, 1):
        emoji = {'BUY': '🟢', 'SELL': '🔴', 'HOLD': '🟡', 'WATCH': '🔵'}
        print(f"{i}. {s['ticker']}: {emoji.get(s['previous'],'⚪')}{s['previous']} → {emoji.get(s['current'],'⚪')}{s['current']}")


if __name__ == '__main__':
    asyncio.run(demo_all_scenarios())

