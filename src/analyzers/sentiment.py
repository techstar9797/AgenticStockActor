"""Sentiment analyzer using OpenAI GPT-4"""
from apify import Actor
from openai import OpenAI
import json
from typing import List, Dict


# Market-moving keywords for detection
MARKET_MOVING_KEYWORDS = [
    "earnings", "EPS", "revenue", "profit", "loss",
    "beats expectations", "misses expectations",
    "guidance raised", "guidance lowered",
    "layoffs", "acquisition", "merger", "partnership",
    "FDA approval", "lawsuit", "CEO resignation",
    "upgrade", "downgrade", "breakthrough", "investigation",
    "contract awarded", "product launch", "regulatory approval"
]


class SentimentAnalyzer:
    """Analyzes sentiment from news and Reddit using AI"""
    
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
    
    def analyze_news_sentiment(self, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment from news articles using GPT-4"""
        if not news_articles:
            Actor.log.warning('No news articles to analyze')
            return {
                'sentiment_score': 0.0,
                'key_topics': [],
                'market_moving_events': []
            }
        
        # Prepare news text (top 15 articles)
        news_text = "\n\n".join([
            f"[{i+1}] {article['headline']}\nSource: {article['source']}"
            for i, article in enumerate(news_articles[:15])
        ])
        
        prompt = f"""Analyze the sentiment of these stock news articles.

NEWS ARTICLES:
{news_text}

TASK:
Provide a sentiment score from -1 (very negative/bearish) to 1 (very positive/bullish).
Identify key topics and any market-moving events from this list: {', '.join(MARKET_MOVING_KEYWORDS[:20])}

Respond in JSON format:
{{
    "sentiment_score": <float between -1 and 1>,
    "key_topics": [<list of 3-5 main topics>],
    "market_moving_events": [<list of significant events detected>]
}}"""
        
        try:
            Actor.log.info(f'🤖 Analyzing news sentiment ({len(news_articles)} articles)...')
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial sentiment analysis expert. Analyze news objectively and provide accurate sentiment scores."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            Actor.log.info(f'  News sentiment: {result["sentiment_score"]:.2f}')
            return result
            
        except Exception as e:
            Actor.log.error(f'Error analyzing news sentiment: {str(e)}')
            return {
                'sentiment_score': 0.0,
                'key_topics': [],
                'market_moving_events': []
            }
    
    def analyze_reddit_sentiment(self, reddit_posts: List[Dict]) -> Dict:
        """Analyze sentiment from Reddit posts using GPT-4"""
        if not reddit_posts:
            Actor.log.warning('No Reddit posts to analyze')
            return {
                'sentiment_score': 0.0,
                'community_mood': 'neutral',
                'key_themes': []
            }
        
        # Sort by score and take top posts
        top_posts = sorted(reddit_posts, key=lambda x: x.get('score', 0), reverse=True)[:12]
        
        reddit_text = "\n\n".join([
            f"[{i+1}] r/{post['subreddit']} - {post['title']}\n   Score: {post['score']} | Comments: {post['num_comments']}"
            for i, post in enumerate(top_posts)
        ])
        
        prompt = f"""Analyze the sentiment of these Reddit posts about a stock.

REDDIT POSTS:
{reddit_text}

TASK:
Consider both the sentiment AND the engagement (score, comments).
High engagement on negative posts = bearish signal.
High engagement on positive posts = bullish signal.

Provide sentiment from -1 (very bearish) to 1 (very bullish).

Respond in JSON format:
{{
    "sentiment_score": <float between -1 and 1>,
    "community_mood": "<bullish|bearish|neutral|mixed>",
    "key_themes": [<list of 3-5 main themes discussed>]
}}"""
        
        try:
            Actor.log.info(f'🤖 Analyzing Reddit sentiment ({len(reddit_posts)} posts)...')
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a social media sentiment analyst specializing in financial markets and retail investor sentiment."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=400
            )
            
            result = json.loads(response.choices[0].message.content)
            Actor.log.info(f'  Reddit sentiment: {result["sentiment_score"]:.2f} ({result["community_mood"]})')
            return result
            
        except Exception as e:
            Actor.log.error(f'Error analyzing Reddit sentiment: {str(e)}')
            return {
                'sentiment_score': 0.0,
                'community_mood': 'neutral',
                'key_themes': []
            }
    
    def synthesize_sentiment(
        self,
        ticker: str,
        news_analysis: Dict,
        reddit_analysis: Dict,
        trump_sentiment: float = None,
        trump_weight: float = 0.0
    ) -> Dict:
        """Combine news, Reddit, and Trump sentiment into overall sentiment
        
        Args:
            ticker: Stock ticker
            news_analysis: News sentiment results
            reddit_analysis: Reddit sentiment results
            trump_sentiment: Trump's sentiment score (-1 to 1)
            trump_weight: Weight multiplier for Trump sentiment (0 to 2.0)
        """
        
        # Base weighted average: news 60%, Reddit 40%
        # News from established sources is more reliable than social media
        news_weight = 0.6
        reddit_weight = 0.4
        
        base_sentiment = (
            news_analysis['sentiment_score'] * news_weight +
            reddit_analysis['sentiment_score'] * reddit_weight
        )
        
        # If Trump sentiment is available, adjust overall sentiment
        if trump_sentiment is not None and trump_weight > 0:
            # Trump sentiment gets dynamic weight based on impact level
            # Formula: (Base × 70%) + (Trump × Weight × 30%)
            overall_sentiment = (
                base_sentiment * 0.7 +
                trump_sentiment * trump_weight * 0.3
            )
            Actor.log.info(f'  Sentiment adjusted for Trump impact: {base_sentiment:.2f} → {overall_sentiment:.2f}')
        else:
            overall_sentiment = base_sentiment
        
        # Determine sentiment label
        if overall_sentiment >= 0.6:
            label = "very_positive"
        elif overall_sentiment >= 0.2:
            label = "positive"
        elif overall_sentiment >= -0.2:
            label = "neutral"
        elif overall_sentiment >= -0.6:
            label = "negative"
        else:
            label = "very_negative"
        
        # Combine topics and themes
        all_topics = (
            news_analysis.get('key_topics', []) +
            reddit_analysis.get('key_themes', [])
        )
        unique_topics = list(dict.fromkeys(all_topics))[:10]  # Remove duplicates, keep order
        
        result = {
            'ticker': ticker,
            'overall_sentiment': round(overall_sentiment, 3),
            'sentiment_label': label,
            'confidence': round(abs(overall_sentiment), 3),
            'news_sentiment': news_analysis['sentiment_score'],
            'reddit_sentiment': reddit_analysis['sentiment_score'],
            'community_mood': reddit_analysis.get('community_mood', 'neutral'),
            'key_topics': unique_topics,
            'market_moving_events': news_analysis.get('market_moving_events', [])
        }
        
        Actor.log.info(f'✓ Overall sentiment: {overall_sentiment:.2f} ({label})')
        return result

