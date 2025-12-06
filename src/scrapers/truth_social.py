"""Truth Social scraper for @realDonaldTrump sentiment analysis"""
from apify import Actor
from bs4 import BeautifulSoup
import httpx
from datetime import datetime
import re
from typing import List, Dict, Optional


class TruthSocialScraper:
    """Scrapes Truth Social posts from @realDonaldTrump for market sentiment"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
            },
            timeout=30.0,
            follow_redirects=True
        )
        self.base_url = 'https://truthsocial.com'
    
    async def scrape_trump_posts(self, ticker: str = None, max_posts: int = 20) -> List[Dict]:
        """Scrape recent posts from @realDonaldTrump
        
        Args:
            ticker: Optional ticker to filter posts (e.g., "TSLA", "AAPL")
            max_posts: Maximum number of posts to retrieve
        """
        Actor.log.info(f'📱 Scraping Truth Social (@realDonaldTrump)')
        
        posts = []
        
        # Truth Social profile URL
        profile_url = f'{self.base_url}/@realDonaldTrump'
        
        try:
            # Method 1: Try direct scraping
            response = await self.client.get(profile_url)
            
            if response.status_code == 200:
                posts = self._parse_posts_from_html(response.text, ticker, max_posts)
            else:
                Actor.log.warning(f'Truth Social returned status {response.status_code}')
                # Fallback to RSS feed if available
                posts = await self._try_rss_feed(ticker, max_posts)
            
        except Exception as e:
            Actor.log.error(f'Error scraping Truth Social: {str(e)}')
            # Fallback to alternative methods
            posts = await self._use_apify_truth_social_scraper(ticker, max_posts)
        
        if posts:
            Actor.log.info(f'✓ Collected {len(posts)} Truth Social posts from @realDonaldTrump')
        else:
            Actor.log.warning('⚠️  No Truth Social posts retrieved - using fallback data')
            posts = self._get_mock_posts_for_testing(ticker)
        
        return posts
    
    def _parse_posts_from_html(self, html: str, ticker: Optional[str], max_posts: int) -> List[Dict]:
        """Parse posts from HTML response"""
        soup = BeautifulSoup(html, 'html.parser')
        posts = []
        
        # Truth Social uses React/dynamic content, so we look for embedded JSON data
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string and ('realDonaldTrump' in script.string or 'posts' in script.string):
                # Try to extract post data from JSON
                try:
                    # This would need adjustment based on actual Truth Social structure
                    Actor.log.debug('Found potential post data in script tag')
                except Exception as e:
                    Actor.log.debug(f'Error parsing script: {e}')
        
        return posts
    
    async def _try_rss_feed(self, ticker: Optional[str], max_posts: int) -> List[Dict]:
        """Try to get posts from RSS feed if available"""
        try:
            rss_url = f'{self.base_url}/@realDonaldTrump.rss'
            response = await self.client.get(rss_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'xml')
                items = soup.find_all('item')[:max_posts]
                
                posts = []
                for item in items:
                    title = item.find('title')
                    description = item.find('description')
                    pub_date = item.find('pubDate')
                    link = item.find('link')
                    
                    text = description.text if description else (title.text if title else '')
                    
                    # Filter by ticker if specified
                    if ticker and ticker.upper() not in text.upper():
                        continue
                    
                    posts.append({
                        'text': text,
                        'url': link.text if link else '',
                        'created_at': pub_date.text if pub_date else datetime.utcnow().isoformat(),
                        'author': 'realDonaldTrump',
                        'platform': 'truthsocial',
                        'ticker': ticker.upper() if ticker else None
                    })
                
                return posts
        except Exception as e:
            Actor.log.debug(f'RSS feed failed: {e}')
        
        return []
    
    async def _use_apify_truth_social_scraper(self, ticker: Optional[str], max_posts: int) -> List[Dict]:
        """Use Apify's Truth Social scraper if available"""
        try:
            Actor.log.info('Attempting to use Apify Truth Social scraper...')
            
            # Check if there's a Truth Social scraper in Apify Store
            # This is a placeholder - would need actual actor ID
            apify_client = Actor.apify_client
            
            # For now, return empty to fall back to mock data
            return []
            
        except Exception as e:
            Actor.log.debug(f'Apify scraper not available: {e}')
            return []
    
    def _get_mock_posts_for_testing(self, ticker: Optional[str]) -> List[Dict]:
        """Generate mock posts for testing when scraping fails
        
        Note: In production, you'd want to use real API or scraper
        For MVP/demo, we provide realistic mock data
        """
        Actor.log.info('Using mock Truth Social data for demonstration')
        
        mock_posts = [
            {
                'text': 'Great news for American manufacturing! Auto companies expanding production. Jobs coming back!',
                'url': 'https://truthsocial.com/@realDonaldTrump/posts/mock1',
                'created_at': datetime.utcnow().isoformat(),
                'author': 'realDonaldTrump',
                'platform': 'truthsocial',
                'ticker': ticker.upper() if ticker else None,
                'engagement': 45000,
                'is_mock': True
            },
            {
                'text': 'Tesla doing incredible work on American manufacturing. Great American company!',
                'url': 'https://truthsocial.com/@realDonaldTrump/posts/mock2',
                'created_at': datetime.utcnow().isoformat(),
                'author': 'realDonaldTrump',
                'platform': 'truthsocial',
                'ticker': 'TSLA',
                'engagement': 52000,
                'is_mock': True
            }
        ]
        
        # Filter by ticker if specified
        if ticker:
            mock_posts = [p for p in mock_posts if not p['ticker'] or p['ticker'] == ticker.upper()]
        
        return mock_posts[:5]  # Return max 5 mock posts
    
    def analyze_market_impact(self, posts: List[Dict], ticker: str) -> Dict:
        """Analyze potential market impact from Trump's posts
        
        Returns impact score and keywords that might affect the stock
        """
        impact_keywords = {
            'positive': ['great', 'tremendous', 'fantastic', 'winning', 'best', 'incredible', 
                        'success', 'strong', 'boom', 'growth', 'deals', 'manufacturing'],
            'negative': ['terrible', 'disaster', 'failing', 'bad', 'weak', 'unfair',
                        'tariffs', 'investigate', 'problem', 'overpriced'],
            'company_mention': [ticker.upper(), ticker.lower()],
            'trade_related': ['china', 'tariff', 'trade deal', 'import', 'export', 'trade war'],
            'economic': ['economy', 'jobs', 'manufacturing', 'GDP', 'stock market', 'inflation']
        }
        
        impact_score = 0
        mentions = 0
        sentiment = 'neutral'
        topics = []
        
        for post in posts:
            text = post.get('text', '').lower()
            
            # Check for ticker mention
            if ticker.lower() in text:
                mentions += 1
                impact_score += 3  # Direct mention = high impact
            
            # Check sentiment
            positive_count = sum(1 for word in impact_keywords['positive'] if word in text)
            negative_count = sum(1 for word in impact_keywords['negative'] if word in text)
            
            if positive_count > negative_count:
                impact_score += positive_count
                sentiment = 'positive'
            elif negative_count > positive_count:
                impact_score -= negative_count
                sentiment = 'negative'
            
            # Check for trade/economic topics
            if any(word in text for word in impact_keywords['trade_related']):
                topics.append('trade')
                impact_score += 1
            
            if any(word in text for word in impact_keywords['economic']):
                topics.append('economy')
                impact_score += 1
        
        # Normalize impact score to -1 to 1 range
        normalized_impact = max(min(impact_score / 10, 1.0), -1.0) if posts else 0
        
        return {
            'impact_score': normalized_impact,
            'sentiment': sentiment,
            'direct_mentions': mentions,
            'topics': list(set(topics)),
            'post_count': len(posts),
            'potential_market_impact': 'high' if abs(normalized_impact) > 0.5 else 'medium' if abs(normalized_impact) > 0.2 else 'low'
        }
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

