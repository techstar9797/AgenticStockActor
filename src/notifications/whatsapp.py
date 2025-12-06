"""WhatsApp notification sender using Twilio API"""
from apify import Actor
from typing import Dict, Optional
import httpx
from datetime import datetime


class WhatsAppNotifier:
    """Send trading signal notifications via WhatsApp using Twilio"""
    
    def __init__(self, account_sid: str = None, auth_token: str = None, from_number: str = None):
        """
        Initialize WhatsApp notifier
        
        Args:
            account_sid: Twilio Account SID
            auth_token: Twilio Auth Token
            from_number: Twilio WhatsApp number (format: whatsapp:+14155238886)
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number or "whatsapp:+14155238886"  # Twilio sandbox default
        self.enabled = bool(account_sid and auth_token)
        
        if self.enabled:
            self.client = httpx.AsyncClient(
                auth=(account_sid, auth_token),
                timeout=30.0
            )
            Actor.log.info('✅ WhatsApp notifications enabled')
        else:
            self.client = None
            Actor.log.info('⚠️  WhatsApp notifications disabled (no credentials)')
    
    async def send_signal_change_alert(
        self,
        to_number: str,
        ticker: str,
        previous_signal: str,
        current_signal: str,
        confidence: float,
        price: float,
        sentiment: float,
        reasoning: str,
        trump_impact: Optional[Dict] = None
    ) -> bool:
        """Send WhatsApp message for signal change"""
        
        if not self.enabled:
            Actor.log.debug('WhatsApp disabled, skipping notification')
            return False
        
        # Build message
        message = self._format_message(
            ticker, previous_signal, current_signal, confidence,
            price, sentiment, reasoning, trump_impact
        )
        
        # Send via Twilio
        success = await self._send_twilio_message(to_number, message)
        
        if success:
            Actor.log.info(f'✅ WhatsApp sent to {to_number}: {ticker} {previous_signal}→{current_signal}')
        else:
            Actor.log.error(f'❌ Failed to send WhatsApp to {to_number}')
        
        return success
    
    def _format_message(
        self,
        ticker: str,
        previous_signal: str,
        current_signal: str,
        confidence: float,
        price: float,
        sentiment: float,
        reasoning: str,
        trump_impact: Optional[Dict]
    ) -> str:
        """Format WhatsApp message with emojis and structure"""
        
        # Signal emojis
        signal_emoji = {
            'BUY': '🟢',
            'SELL': '🔴',
            'HOLD': '🟡',
            'WATCH': '🔵'
        }
        
        # Determine urgency
        urgent = (previous_signal, current_signal) in [
            ('BUY', 'SELL'), ('SELL', 'BUY'),
            ('HOLD', 'BUY'), ('HOLD', 'SELL')
        ]
        
        # Build message
        header = '🚨 URGENT' if urgent else '📊'
        
        message = f"""{header} SIGNAL CHANGE: {ticker}

{signal_emoji.get(previous_signal, '⚪')} Previous: {previous_signal}
{signal_emoji.get(current_signal, '⚪')} *NEW: {current_signal}*

💰 Price: ${price:.2f}
💭 Sentiment: {sentiment:+.2f}
🎯 Confidence: {confidence:.0%}

📝 Reason:
{reasoning[:200]}{'...' if len(reasoning) > 200 else ''}"""
        
        # Add Trump impact if significant
        if trump_impact and trump_impact.get('impact_level') not in ['none', None]:
            trump_emoji = '🚨' if trump_impact.get('ticker_mentioned') else '📱'
            message += f"""

{trump_emoji} TRUMP IMPACT: {trump_impact['impact_level'].upper()}"""
            
            if trump_impact.get('ticker_mentioned'):
                message += f"\n⚠️ {ticker} DIRECTLY MENTIONED!"
            
            if trump_impact.get('sentiment_score'):
                message += f"\nTrump Sentiment: {trump_impact['sentiment_score']:+.2f}"
            
            # Add first policy implication if exists
            if trump_impact.get('policy_implications'):
                policy = trump_impact['policy_implications'][0]
                message += f"\nPolicy: {policy[:80]}"
        
        # Add timestamp
        message += f"""

🕐 {datetime.utcnow().strftime('%H:%M UTC')}"""
        
        return message
    
    async def _send_twilio_message(self, to_number: str, message: str) -> bool:
        """Send message via Twilio WhatsApp API"""
        
        if not self.client:
            return False
        
        # Ensure number has whatsapp: prefix
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        # Twilio API endpoint
        url = f'https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json'
        
        data = {
            'From': self.from_number,
            'To': to_number,
            'Body': message
        }
        
        try:
            response = await self.client.post(url, data=data)
            
            if response.status_code in [200, 201]:
                Actor.log.info('✅ WhatsApp message sent successfully')
                return True
            else:
                Actor.log.error(f'Twilio error: {response.status_code} - {response.text}')
                return False
                
        except Exception as e:
            Actor.log.error(f'Error sending WhatsApp: {str(e)}')
            return False
    
    async def send_daily_summary(
        self,
        to_number: str,
        signals: Dict[str, Dict],
        changes_count: int
    ) -> bool:
        """Send daily summary of all signals"""
        
        if not self.enabled:
            return False
        
        message = f"""📊 DAILY STOCK SUMMARY

Changes today: {changes_count}

"""
        
        # Add each ticker
        for ticker, signal_data in signals.items():
            emoji = {'BUY': '🟢', 'SELL': '🔴', 'HOLD': '🟡', 'WATCH': '🔵'}
            signal = signal_data['signal']
            confidence = signal_data['confidence']
            
            message += f"{emoji.get(signal, '⚪')} {ticker}: {signal} ({confidence:.0%})\n"
        
        message += f"""
🕐 {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}

View details: console.apify.com"""
        
        return await self._send_twilio_message(to_number, message)
    
    async def close(self):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()

