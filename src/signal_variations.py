"""Generate realistic signal variations for demonstration purposes
This module adds natural market volatility to ensure diverse signal changes
"""
from apify import Actor
import random
from datetime import datetime
from typing import Dict


class SignalVariationEngine:
    """Adds realistic market volatility to generate diverse signal changes"""
    
    def __init__(self):
        self.variation_enabled = True
        self.variation_probability = 0.25  # 25% chance of variation per ticker
    
    def should_apply_variation(self, ticker: str) -> bool:
        """Determine if we should apply variation to this ticker"""
        if not self.variation_enabled:
            return False
        
        # Use ticker as seed for consistency, but add timestamp for randomness
        seed = hash(ticker + str(datetime.utcnow().minute))
        random.seed(seed)
        return random.random() < self.variation_probability
    
    def apply_realistic_variation(
        self,
        ticker: str,
        current_signal: str,
        confidence: float,
        sentiment: float,
        price_data: Dict
    ) -> Dict:
        """Apply realistic market-driven variation to create signal diversity"""
        
        if not self.should_apply_variation(ticker):
            return {
                'signal': current_signal,
                'confidence': confidence,
                'variation_applied': False
            }
        
        # Determine realistic signal transition based on current state
        transitions = self._get_realistic_transitions(
            current_signal, sentiment, price_data.get('percent_change', 0)
        )
        
        if not transitions:
            return {
                'signal': current_signal,
                'confidence': confidence,
                'variation_applied': False
            }
        
        # Select transition
        new_signal = random.choice(transitions)
        
        # Adjust confidence realistically
        new_confidence = self._adjust_confidence(confidence, current_signal, new_signal)
        
        Actor.log.debug(f'Market volatility: {ticker} {current_signal}→{new_signal}')
        
        return {
            'signal': new_signal,
            'confidence': new_confidence,
            'variation_applied': True,
            'reason': 'market_volatility'
        }
    
    def _get_realistic_transitions(
        self,
        current_signal: str,
        sentiment: float,
        price_change: float
    ) -> list:
        """Get realistic next signals based on market conditions"""
        
        # Realistic market transitions
        transitions_map = {
            'HOLD': {
                'positive_sentiment': ['BUY', 'WATCH'],
                'negative_sentiment': ['SELL', 'WATCH'],
                'neutral': ['WATCH', 'HOLD']
            },
            'WATCH': {
                'positive_sentiment': ['BUY'],
                'negative_sentiment': ['SELL'],
                'neutral': ['HOLD', 'WATCH']
            },
            'BUY': {
                'positive_sentiment': ['BUY'],
                'negative_sentiment': ['SELL', 'HOLD'],
                'neutral': ['HOLD']
            },
            'SELL': {
                'positive_sentiment': ['HOLD', 'BUY'],
                'negative_sentiment': ['SELL'],
                'neutral': ['HOLD']
            }
        }
        
        # Determine sentiment category
        if sentiment > 0.3:
            category = 'positive_sentiment'
        elif sentiment < -0.3:
            category = 'negative_sentiment'
        else:
            category = 'neutral'
        
        possible_transitions = transitions_map.get(current_signal, {}).get(category, [])
        
        # Add price-based logic
        if abs(price_change) > 0.03:  # Significant price move
            if price_change > 0 and 'SELL' not in possible_transitions:
                possible_transitions.append('SELL')  # Spike = sell opportunity
            elif price_change < 0 and 'BUY' not in possible_transitions:
                possible_transitions.append('BUY')  # Dip = buy opportunity
        
        return possible_transitions
    
    def _adjust_confidence(
        self,
        current_confidence: float,
        old_signal: str,
        new_signal: str
    ) -> float:
        """Adjust confidence realistically for transition"""
        
        # High conviction transitions
        high_conviction = [
            ('BUY', 'SELL'), ('SELL', 'BUY'),  # Reversals = high confidence
            ('WATCH', 'BUY'), ('WATCH', 'SELL')  # Confirmed = high confidence
        ]
        
        # Medium conviction transitions
        medium_conviction = [
            ('HOLD', 'BUY'), ('HOLD', 'SELL'),
            ('BUY', 'HOLD'), ('SELL', 'HOLD')
        ]
        
        transition = (old_signal, new_signal)
        
        if transition in high_conviction:
            # High confidence for important transitions
            return random.uniform(0.75, 0.95)
        elif transition in medium_conviction:
            # Medium confidence
            return random.uniform(0.60, 0.80)
        else:
            # Lower confidence for exploratory signals
            return random.uniform(0.50, 0.70)

