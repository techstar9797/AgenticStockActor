"""Trump sentiment analyzer - analyzes impact of @realDonaldTrump posts on stocks"""
from apify import Actor
from openai import OpenAI
import json
from typing import List, Dict


class TrumpSentimentAnalyzer:
    """Analyzes sentiment and market impact from Trump's Truth Social posts"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
    
    def analyze_trump_impact(self, posts: List[Dict], ticker: str) -> Dict:
        """Analyze Trump's posts for market impact on specific ticker using GPT-4"""
        
        if not posts:
            Actor.log.warning('No Trump posts to analyze')
            return {
                'sentiment_score': 0.0,
                'impact_level': 'none',
                'key_themes': [],
                'ticker_mentioned': False
            }
        
        # Prepare posts text
        posts_text = "\n\n".join([
            f"Post {i+1}: {post.get('text', '')}\nEngagement: {post.get('engagement', 'N/A')}"
            for i, post in enumerate(posts[:10])
        ])
        
        prompt = f"""Analyze these recent posts from @realDonaldTrump on Truth Social for their potential impact on {ticker} stock.

POSTS:
{posts_text}

ANALYSIS TASK:
You are a political economy analyst specializing in how political statements affect stock markets.
Analyze these posts for:

1. Direct or indirect mentions of {ticker} or its industry
2. Sentiment toward the company/sector (positive/negative/neutral)
3. Policy implications (tariffs, regulations, trade deals)
4. Potential market impact (high/medium/low/none)
5. Key themes that could affect stock price

Historical context:
- Trump's posts about companies can cause immediate market reactions
- Tariff announcements typically negative for affected companies
- Praise for American manufacturing typically positive
- Trade deal announcements can be highly impactful

Respond in JSON format:
{{
    "sentiment_score": <float from -1 (very negative) to 1 (very positive)>,
    "impact_level": "<none|low|medium|high>",
    "ticker_mentioned": <true|false>,
    "key_themes": [<list of 3-5 main themes>],
    "policy_implications": [<any policy changes that could affect the stock>],
    "market_reaction_prediction": "<brief prediction of likely market reaction>",
    "confidence": <0.0 to 1.0>
}}"""
        
        try:
            Actor.log.info(f'🤖 Analyzing Trump posts impact on {ticker} using GPT-4...')
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert political economy analyst who specializes in analyzing how political statements, especially from Donald Trump, affect stock markets. You understand tariffs, trade policy, and market psychology."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=600
            )
            
            result = json.loads(response.choices[0].message.content)
            
            Actor.log.info(f'  Trump Impact: {result["impact_level"].upper()} ({result["sentiment_score"]:+.2f})')
            if result.get('ticker_mentioned'):
                Actor.log.info(f'  ⚠️  {ticker} directly mentioned in posts!')
            
            return result
            
        except Exception as e:
            Actor.log.error(f'Error analyzing Trump posts: {str(e)}')
            return {
                'sentiment_score': 0.0,
                'impact_level': 'none',
                'ticker_mentioned': False,
                'key_themes': [],
                'policy_implications': [],
                'market_reaction_prediction': 'Unable to analyze',
                'confidence': 0.0
            }
    
    def get_trump_weight(self, impact_level: str, ticker_mentioned: bool) -> float:
        """Calculate how much weight Trump's sentiment should have in overall analysis
        
        Returns a multiplier (0.0 to 2.0) for Trump sentiment weight
        """
        weights = {
            'none': 0.0,
            'low': 0.3,
            'medium': 0.7,
            'high': 1.5
        }
        
        base_weight = weights.get(impact_level, 0.0)
        
        # Double the weight if ticker is directly mentioned
        if ticker_mentioned:
            base_weight *= 2.0
        
        # Cap at 2.0
        return min(base_weight, 2.0)

