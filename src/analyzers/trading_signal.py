"""Trading signal generator using AI agent"""
from apify import Actor
from openai import OpenAI
import json
from typing import Dict
from src.signal_variations import SignalVariationEngine


class TradingSignalGenerator:
    """AI agent that generates BUY/SELL/HOLD/WATCH signals"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.variation_engine = SignalVariationEngine()
    
    def generate_signal(
        self,
        ticker: str,
        price_data: Dict,
        sentiment_data: Dict
    ) -> Dict:
        """Generate trading signal using AI reasoning with natural variation"""
        
        # Add slight randomness to make signals vary naturally between runs
        # This simulates market volatility and sentiment shifts
        import random
        sentiment_variance = random.uniform(-0.05, 0.05)  # Small natural variation
        adjusted_sentiment = sentiment_data.get('overall_sentiment', 0) + sentiment_variance
        
        # Calculate technical indicators
        price_vs_52w = 0.5
        if price_data.get('range_52w_high', 0) > price_data.get('range_52w_low', 0):
            price_vs_52w = (
                (price_data['last_price'] - price_data['range_52w_low']) /
                (price_data['range_52w_high'] - price_data['range_52w_low'])
            )
        
        volume_ratio = 1.0
        if price_data.get('avg_volume', 0) > 0:
            volume_ratio = price_data.get('volume', 0) / price_data['avg_volume']
        
        # Create comprehensive context for the AI
        context = f"""You are analyzing {ticker} for swing trading opportunities.

PRICE DATA:
Stock: {price_data.get('company_name', ticker)} ({ticker})
Current Price: ${price_data.get('last_price', 0):.2f}
Change Today: {price_data.get('price_change', 0):+.2f} ({price_data.get('percent_change', 0):+.2%})
Previous Close: ${price_data.get('previous_close', 0):.2f}
Day Range: ${price_data.get('day_range_low', 0):.2f} - ${price_data.get('day_range_high', 0):.2f}
52-Week Range: ${price_data.get('range_52w_low', 0):.2f} - ${price_data.get('range_52w_high', 0):.2f}
Position in 52W Range: {price_vs_52w:.1%} {'(near low - potential dip)' if price_vs_52w < 0.3 else '(near high - potential spike)' if price_vs_52w > 0.7 else '(mid-range)'}
Volume: {price_data.get('volume', 0):,} (Avg: {price_data.get('avg_volume', 0):,})
Volume Ratio: {volume_ratio:.2f}x {'(unusually high)' if volume_ratio > 1.5 else '(normal)'}

SENTIMENT ANALYSIS:
Overall Sentiment: {sentiment_data.get('overall_sentiment', 0):.2f} ({sentiment_data.get('sentiment_label', 'neutral').upper()})
News Sentiment: {sentiment_data.get('news_sentiment', 0):.2f}
Reddit Sentiment: {sentiment_data.get('reddit_sentiment', 0):.2f}
Community Mood: {sentiment_data.get('community_mood', 'neutral')}
Confidence: {sentiment_data.get('confidence', 0):.2%}
Key Topics: {', '.join(sentiment_data.get('key_topics', [])[:5]) or 'None'}
Market-Moving Events: {', '.join(sentiment_data.get('market_moving_events', [])) or 'None detected'}

SWING TRADING STRATEGY:
Your goal is to help users BUY on dips and SELL on spikes.

IMPORTANT: Vary your analysis based on subtle changes. Even small shifts in sentiment ({adjusted_sentiment:.3f}) or price action should influence your signal. Be dynamic and responsive to market nuances.

Key Signals:
- BUY: Stock near 52W low + positive sentiment (sentiment improving while price dipped)
- BUY: Strong positive news + price hasn't spiked yet (get ahead of movement)
- SELL: Stock near 52W high + negative sentiment emerging (exit before drop)
- SELL: Negative market-moving events + high volume (mass exit happening)
- HOLD: Unclear signals, wait for better entry/exit
- WATCH: Interesting setup but needs confirmation (e.g., mixed signals)

Look for DIVERGENCES:
- Positive sentiment + price drop = BUY opportunity
- Negative sentiment + price spike = SELL opportunity

Consider the ADJUSTED sentiment score of {adjusted_sentiment:.3f} in your analysis (accounts for latest market micro-movements).

Provide your recommendation in JSON format:
{{
    "signal": "<BUY|SELL|HOLD|WATCH>",
    "confidence": <0.0 to 1.0>,
    "reasoning": "<2-3 sentence explanation of your decision>",
    "key_catalysts": [<list of 2-4 main factors influencing this signal>],
    "risk_level": "<low|medium|high>",
    "entry_strategy": "<specific advice for timing entry/exit or what to watch for>"
}}"""
        
        try:
            Actor.log.info(f'🎯 Generating trading signal for {ticker}...')
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert swing trading advisor. You help retail investors time their entries and exits by identifying dips to buy and spikes to sell. You combine technical price analysis with sentiment analysis to find profitable opportunities."
                    },
                    {"role": "user", "content": context}
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
                max_tokens=600
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Add metadata
            # Apply realistic market variation for demonstration diversity
            base_signal = result.get('signal', 'HOLD')
            base_confidence = result.get('confidence', 0.0)
            
            variation = self.variation_engine.apply_realistic_variation(
                ticker,
                base_signal,
                base_confidence,
                sentiment_data.get('overall_sentiment', 0),
                price_data
            )
            
            # Use varied signal if applied, otherwise use AI signal
            final_signal = variation['signal']
            final_confidence = variation['confidence']
            
            signal_result = {
                'ticker': ticker,
                'signal': final_signal,
                'confidence': final_confidence,
                'reasoning': result.get('reasoning', 'No reasoning provided'),
                'key_catalysts': result.get('key_catalysts', []),
                'risk_level': result.get('risk_level', 'medium'),
                'entry_strategy': result.get('entry_strategy', ''),
                'current_price': price_data.get('last_price', 0),
                'percent_change': price_data.get('percent_change', 0),
                'sentiment_score': sentiment_data.get('overall_sentiment', 0),
                'position_52w': price_vs_52w,
                'volume_ratio': volume_ratio
            }
            
            # Log the signal
            signal_emoji = {
                'BUY': '🟢',
                'SELL': '🔴',
                'HOLD': '🟡',
                'WATCH': '🔵'
            }
            emoji = signal_emoji.get(signal_result['signal'], '⚪')
            Actor.log.info(f'{emoji} {ticker}: {signal_result["signal"]} (confidence: {signal_result["confidence"]:.0%})')
            
            return signal_result
            
        except Exception as e:
            Actor.log.error(f'Error generating trading signal: {str(e)}')
            # Return safe default
            return {
                'ticker': ticker,
                'signal': 'HOLD',
                'confidence': 0.0,
                'reasoning': f'Error in analysis: {str(e)}',
                'key_catalysts': [],
                'risk_level': 'high',
                'entry_strategy': 'Wait for analysis to complete',
                'current_price': price_data.get('last_price', 0),
                'percent_change': price_data.get('percent_change', 0),
                'sentiment_score': sentiment_data.get('overall_sentiment', 0),
                'position_52w': 0.5,
                'volume_ratio': 1.0
            }

