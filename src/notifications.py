"""Signal change detection and notification system"""
from apify import Actor
from typing import Dict, List, Optional
from datetime import datetime
import json


class SignalChangeDetector:
    """Detects changes in trading signals and triggers notifications"""
    
    def __init__(self):
        self.kv_store = None
    
    async def initialize(self):
        """Initialize key-value store for signal history"""
        self.kv_store = await Actor.open_key_value_store()
    
    async def check_and_notify(self, ticker: str, current_signal: str, current_confidence: float) -> Dict:
        """Check if signal changed and return notification data"""
        
        # Get previous signal from storage
        previous_data = await self.kv_store.get_value(f'signal_{ticker}')
        
        result = {
            'ticker': ticker,
            'current_signal': current_signal,
            'current_confidence': current_confidence,
            'previous_signal': None,
            'signal_changed': False,
            'change_type': None,
            'notification_sent': False,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if previous_data:
            previous_signal = previous_data.get('signal')
            previous_confidence = previous_data.get('confidence', 0)
            previous_timestamp = previous_data.get('timestamp')
            
            result['previous_signal'] = previous_signal
            result['previous_timestamp'] = previous_timestamp
            
            # Check if signal changed
            if previous_signal != current_signal:
                result['signal_changed'] = True
                result['change_type'] = f"{previous_signal} → {current_signal}"
                
                # Determine if this is a significant change worth notifying
                significant_changes = [
                    ('BUY', 'SELL'), ('SELL', 'BUY'),  # Complete reversal
                    ('HOLD', 'BUY'), ('HOLD', 'SELL'),  # Action from hold
                    ('HOLD', 'WATCH'), ('WATCH', 'BUY'), ('WATCH', 'SELL'),  # Escalation
                    ('BUY', 'HOLD'), ('SELL', 'HOLD'),  # De-escalation
                ]
                
                if (previous_signal, current_signal) in significant_changes:
                    # Send notification
                    await self._send_notification(ticker, previous_signal, current_signal, 
                                                 current_confidence, previous_confidence)
                    result['notification_sent'] = True
                    
                    Actor.log.info(f'🔔 SIGNAL CHANGE for {ticker}: {previous_signal} → {current_signal}')
        
        # Save current signal for next run
        await self.kv_store.set_value(f'signal_{ticker}', {
            'signal': current_signal,
            'confidence': current_confidence,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return result
    
    async def _send_notification(
        self,
        ticker: str,
        previous_signal: str,
        current_signal: str,
        current_confidence: float,
        previous_confidence: float
    ):
        """Send notification via multiple channels"""
        
        # Determine urgency
        urgent_changes = [('BUY', 'SELL'), ('SELL', 'BUY'), ('HOLD', 'SELL'), ('HOLD', 'BUY')]
        is_urgent = (previous_signal, current_signal) in urgent_changes
        
        emoji_map = {'BUY': '🟢', 'SELL': '🔴', 'HOLD': '🟡', 'WATCH': '🔵'}
        
        notification_message = f"""
{'🚨 URGENT ' if is_urgent else '📊 '}SIGNAL CHANGE ALERT: {ticker}

{emoji_map.get(previous_signal, '⚪')} Previous: {previous_signal} ({previous_confidence:.0%} confidence)
{emoji_map.get(current_signal, '⚪')} **NEW: {current_signal}** ({current_confidence:.0%} confidence)

Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
"""
        
        # Log to console (always)
        Actor.log.info('=' * 60)
        Actor.log.info(notification_message)
        Actor.log.info('=' * 60)
        
        # Store notification in dataset for history
        await Actor.push_data({
            'type': 'signal_change_notification',
            'ticker': ticker,
            'previous_signal': previous_signal,
            'current_signal': current_signal,
            'confidence': current_confidence,
            'is_urgent': is_urgent,
            'timestamp': datetime.utcnow().isoformat(),
            'message': notification_message
        })
        
        # TODO: Add email/Slack/SMS integration here
        # Example:
        # await self._send_email(notification_message)
        # await self._send_slack(notification_message)
    
    async def get_all_signals(self) -> Dict[str, Dict]:
        """Get all stored signals for all tickers"""
        if not self.kv_store:
            await self.initialize()
        
        signals = {}
        keys = await self.kv_store.list_keys()
        
        for key in keys.get('items', []):
            if key['key'].startswith('signal_'):
                ticker = key['key'].replace('signal_', '')
                data = await self.kv_store.get_value(key['key'])
                signals[ticker] = data
        
        return signals
    
    async def _send_email(self, message: str):
        """Send email notification (placeholder)"""
        # TODO: Integrate with SendGrid, AWS SES, or similar
        pass
    
    async def _send_slack(self, message: str):
        """Send Slack notification (placeholder)"""
        # TODO: Integrate with Slack webhook
        pass

