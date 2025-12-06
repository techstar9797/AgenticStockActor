"""Reddit scraper for stock sentiment from investing subreddits"""
from apify import Actor
from bs4 import BeautifulSoup
import httpx
from datetime import datetime
import re
import asyncio
from typing import List, Dict


class RedditScraper:
    """Scrapes Reddit posts mentioning stock tickers using Apify proxies"""
    
    def __init__(self):
        # Will be initialized with proxy later
        self.client = None
        self.use_apify_scraper = True  # Prefer Apify's Reddit scraper
    
    async def scrape_ticker(
        self, 
        ticker: str, 
        subreddits: List[str],
        max_posts: int = 50
    ) -> List[Dict]:
        """Scrape posts mentioning ticker from multiple subreddits"""
        Actor.log.info(f'💬 Scraping Reddit for ${ticker}')
        
        # For MVP, return mock data to avoid Reddit 403 errors
        # TODO: Implement proper Reddit scraping with API or paid scraper
        Actor.log.info(f'⚠️  Reddit scraping temporarily disabled (403 errors). Using news-only sentiment.')
        return []
        
        # Commented out for MVP
        # # Try using Apify's Reddit scraper first
        # if self.use_apify_scraper:
        #     try:
        #         posts = await self._scrape_with_apify_actor(ticker, subreddits, max_posts)
        #         if posts:
        #             Actor.log.info(f'✓ Collected {len(posts)} Reddit posts for {ticker} (via Apify scraper)')
        #             return posts
        #     except Exception as e:
        #         Actor.log.warning(f'Apify Reddit scraper failed: {str(e)}, falling back to direct scraping')
        #
        # # Fallback to direct scraping with proxies
        # return await self._scrape_direct(ticker, subreddits, max_posts)
    
    async def _scrape_with_apify_actor(
        self,
        ticker: str,
        subreddits: List[str],
        max_posts: int
    ) -> List[Dict]:
        """Use Apify's Reddit scraper actor"""
        all_posts = []
        posts_per_subreddit = max(10, max_posts // len(subreddits))
        
        for subreddit in subreddits:
            try:
                # Call Apify's Reddit scraper
                run_input = {
                    'searchPosts': {
                        'subreddit': subreddit,
                        'searchTerms': [ticker, f'${ticker}'],
                        'sort': 'hot',
                        'time': 'week'
                    },
                    'maxItems': posts_per_subreddit,
                    'proxy': {
                        'useApifyProxy': True
                    }
                }
                
                # Run the scraper using Apify client
                apify_client = Actor.apify_client
                run = await apify_client.actor('trudax/reddit-scraper').call(
                    run_input=run_input,
                    memory_mbytes=256,
                    timeout_secs=120
                )
                
                if not run:
                    continue
                
                # Get dataset items
                dataset_client = Actor.apify_client.dataset(run['defaultDatasetId'])
                
                async for item in dataset_client.iterate_items():
                    try:
                        post = {
                            'title': item.get('title', ''),
                            'url': item.get('url', ''),
                            'subreddit': subreddit,
                            'author': item.get('author', ''),
                            'score': int(item.get('score', 0)),
                            'num_comments': int(item.get('numComments', 0)),
                            'created_at': item.get('createdAt', datetime.utcnow().isoformat()),
                            'text': item.get('selftext'),
                            'ticker': ticker.upper()
                        }
                        all_posts.append(post)
                    except Exception as e:
                        Actor.log.debug(f'Error parsing Reddit item: {e}')
                        continue
                
                Actor.log.info(f'  r/{subreddit}: {len([p for p in all_posts if p["subreddit"] == subreddit])} posts')
                
            except Exception as e:
                Actor.log.warning(f'Error with Apify Reddit scraper for r/{subreddit}: {e}')
                continue
        
        # Sort by score and limit
        all_posts.sort(key=lambda x: x.get('score', 0), reverse=True)
        return all_posts[:max_posts]
    
    async def _scrape_direct(
        self,
        ticker: str,
        subreddits: List[str],
        max_posts: int
    ) -> List[Dict]:
        """Direct scraping with Apify proxies as fallback"""
        # Get Apify proxy configuration
        try:
            proxy_config = await Actor.create_proxy_configuration()
            proxy_url = await proxy_config.new_url() if proxy_config else None
        except:
            proxy_url = None
        
        #Initialize HTTP client with proxy (httpx 0.28 syntax)
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            proxy=proxy_url,  # httpx 0.28 uses 'proxy' not 'proxies'
            timeout=30.0,
            follow_redirects=True
        )
        
        all_posts = []
        posts_per_subreddit = max(10, max_posts // len(subreddits))
        
        for subreddit in subreddits:
            posts = await self._scrape_subreddit(subreddit, ticker, posts_per_subreddit)
            all_posts.extend(posts)
            await asyncio.sleep(2)  # Be respectful
        
        # Sort by score and limit
        all_posts.sort(key=lambda x: x.get('score', 0), reverse=True)
        all_posts = all_posts[:max_posts]
        
        Actor.log.info(f'✓ Collected {len(all_posts)} Reddit posts for {ticker}')
        return all_posts
    
    async def _scrape_subreddit(
        self, 
        subreddit: str, 
        ticker: str, 
        max_posts: int
    ) -> List[Dict]:
        """Scrape posts from a single subreddit"""
        if not self.client:
            Actor.log.warning('HTTP client not initialized')
            return []
        
        # Use old Reddit for easier scraping
        url = f'https://old.reddit.com/r/{subreddit}/search?q={ticker}&restrict_sr=1&sort=hot'
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            posts = []
            post_elements = soup.find_all('div', class_='thing', limit=max_posts * 2)
            
            for post_elem in post_elements:
                if len(posts) >= max_posts:
                    break
                
                try:
                    # Extract post data
                    title_elem = post_elem.find('a', class_='title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    
                    # Check if ticker mentioned (case-insensitive)
                    ticker_pattern = r'\b' + re.escape(ticker) + r'\b'
                    if not re.search(ticker_pattern, title, re.IGNORECASE):
                        # Check if it's in a stock symbol format like $TICKER
                        if f'${ticker.upper()}' not in title.upper():
                            continue
                    
                    post_url = title_elem.get('href', '')
                    if post_url and not post_url.startswith('http'):
                        post_url = f'https://reddit.com{post_url}'
                    
                    # Extract score
                    score_elem = post_elem.find('div', class_='score')
                    score = 0
                    if score_elem:
                        score_text = score_elem.get('title', score_elem.text)
                        try:
                            score = int(score_text.replace(',', ''))
                        except (ValueError, AttributeError):
                            # Try unvoted or hidden scores
                            if score_elem.text and score_elem.text.isdigit():
                                score = int(score_elem.text)
                    
                    # Extract author
                    author_elem = post_elem.find('a', class_='author')
                    author = author_elem.text if author_elem else '[deleted]'
                    
                    # Extract comment count
                    comments_elem = post_elem.find('a', class_='comments')
                    num_comments = 0
                    if comments_elem:
                        comments_text = comments_elem.text
                        match = re.search(r'(\d+)', comments_text.replace(',', ''))
                        if match:
                            num_comments = int(match.group(1))
                    
                    # Extract timestamp
                    time_elem = post_elem.find('time')
                    created_at = datetime.utcnow().isoformat()
                    if time_elem and time_elem.get('datetime'):
                        created_at = time_elem['datetime']
                    
                    # Get post text if available
                    text_elem = post_elem.find('div', class_='usertext-body')
                    text = text_elem.text.strip() if text_elem else None
                    
                    posts.append({
                        'title': title,
                        'url': post_url,
                        'subreddit': subreddit,
                        'author': author,
                        'score': score,
                        'num_comments': num_comments,
                        'created_at': created_at,
                        'text': text,
                        'ticker': ticker.upper()
                    })
                    
                except Exception as e:
                    Actor.log.debug(f'Error parsing post: {str(e)}')
                    continue
            
            Actor.log.info(f'  r/{subreddit}: {len(posts)} posts')
            return posts
            
        except Exception as e:
            Actor.log.error(f'Error scraping r/{subreddit}: {str(e)}')
            return []
    
    async def close(self):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()

