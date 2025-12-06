"""Yahoo Finance scraper for stock data and news"""
from apify import Actor
from bs4 import BeautifulSoup
import httpx
from datetime import datetime
import re
import json
from typing import Dict, List, Optional


class YahooFinanceScraper:
    """Scrapes stock price data and news from Yahoo Finance"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            },
            timeout=30.0,
            follow_redirects=True
        )
    
    async def scrape_ticker(self, ticker: str, max_news: int = 20) -> Optional[Dict]:
        """Scrape complete data for a single ticker"""
        Actor.log.info(f'📊 Scraping Yahoo Finance for {ticker}')
        
        # Try API first (more reliable)
        price_data = await self._get_price_from_api(ticker)
        
        # Fallback to HTML scraping if API fails
        if not price_data or price_data.get('last_price', 0) == 0:
            url = f'https://finance.yahoo.com/quote/{ticker}'
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                price_data = self._extract_price_data(soup, ticker)
            except Exception as e:
                Actor.log.error(f'Error scraping HTML for {ticker}: {str(e)}')
                price_data = {'ticker': ticker, 'error': str(e)}
        
        # Extract news
        news_articles = await self._extract_news(ticker, max_news)
        
        return {
            'ticker': ticker.upper(),
            'timestamp': datetime.utcnow().isoformat(),
            'price_data': price_data,
            'news_articles': news_articles,
            'source': 'yahoo_finance'
        }
    
    async def _get_price_from_api(self, ticker: str) -> Optional[Dict]:
        """Get price data from Yahoo Finance query API"""
        try:
            # Yahoo Finance v10 API
            url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}'
            params = {
                'modules': 'price,summaryDetail'
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data_json = response.json()
            
            result = data_json.get('quoteSummary', {}).get('result', [])
            if not result:
                return None
            
            quote_data = result[0]
            price_info = quote_data.get('price', {})
            summary = quote_data.get('summaryDetail', {})
            
            data = {
                'ticker': ticker.upper(),
                'company_name': price_info.get('longName', price_info.get('shortName', ticker)),
                'last_price': float(price_info.get('regularMarketPrice', {}).get('raw', 0)),
                'price_change': float(price_info.get('regularMarketChange', {}).get('raw', 0)),
                'percent_change': float(price_info.get('regularMarketChangePercent', {}).get('raw', 0)) / 100,
                'previous_close': float(price_info.get('regularMarketPreviousClose', {}).get('raw', 0)),
                'open_price': float(price_info.get('regularMarketOpen', {}).get('raw', 0)),
                'day_range_low': float(price_info.get('regularMarketDayLow', {}).get('raw', 0)),
                'day_range_high': float(price_info.get('regularMarketDayHigh', {}).get('raw', 0)),
                'volume': int(price_info.get('regularMarketVolume', {}).get('raw', 0)),
                'range_52w_low': float(summary.get('fiftyTwoWeekLow', {}).get('raw', 0)),
                'range_52w_high': float(summary.get('fiftyTwoWeekHigh', {}).get('raw', 0)),
                'avg_volume': int(summary.get('averageDailyVolume10Day', {}).get('raw', 0)),
                'market_cap': price_info.get('marketCap', {}).get('fmt', 'N/A')
            }
            
            if data['last_price'] > 0:
                Actor.log.info(f'✓ Price data (API): ${data["last_price"]:.2f} ({data["percent_change"]:+.2%})')
                return data
            
            return None
            
        except Exception as e:
            Actor.log.debug(f'API fetch failed: {str(e)}')
            return None
    
    def _extract_price_data(self, soup: BeautifulSoup, ticker: str) -> Dict:
        """Extract price and market data from Yahoo Finance page - multiple methods"""
        try:
            data = {
                'ticker': ticker.upper(),
                'company_name': ticker,
                'last_price': 0.0,
                'price_change': 0.0,
                'percent_change': 0.0,
                'previous_close': 0.0,
                'open_price': 0.0,
                'day_range_low': 0.0,
                'day_range_high': 0.0,
                'range_52w_low': 0.0,
                'range_52w_high': 0.0,
                'volume': 0,
                'avg_volume': 0,
                'market_cap': 'N/A'
            }
            
            # Method 1: Look for specific script with quote data
            scripts = soup.find_all('script')
            for script in scripts:
                if not script.string:
                    continue
                    
                # Look for the data structure
                if '"StreamDataStore"' in script.string or 'QuoteSummaryStore' in script.string:
                    try:
                        # Find JSON object
                        script_text = script.string
                        
                        # Try to find and extract the JSON
                        if 'root.App.main' in script_text:
                            start = script_text.find('root.App.main') + len('root.App.main')
                            script_text = script_text[start:].strip()
                            if script_text.startswith('='):
                                script_text = script_text[1:].strip()
                        
                        # Find the JSON boundaries more carefully
                        brace_count = 0
                        start_idx = -1
                        end_idx = -1
                        
                        for i, char in enumerate(script_text):
                            if char == '{':
                                if start_idx == -1:
                                    start_idx = i
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0 and start_idx != -1:
                                    end_idx = i + 1
                                    break
                        
                        if start_idx != -1 and end_idx != -1:
                            json_str = script_text[start_idx:end_idx]
                            json_data = json.loads(json_str)
                            
                            # Navigate through the data structure
                            stores = (json_data.get('context', {})
                                    .get('dispatcher', {})
                                    .get('stores', {}))
                            
                            quote_store = stores.get('QuoteSummaryStore', {})
                            stream_store = stores.get('StreamDataStore', {})
                            
                            # Try QuoteSummaryStore first
                            if quote_store:
                                price_info = quote_store.get('price', {})
                                if price_info:
                                    data['company_name'] = price_info.get('longName', price_info.get('shortName', ticker))
                                    data['last_price'] = float(price_info.get('regularMarketPrice', {}).get('raw', 0))
                                    data['price_change'] = float(price_info.get('regularMarketChange', {}).get('raw', 0))
                                    data['percent_change'] = float(price_info.get('regularMarketChangePercent', {}).get('raw', 0)) / 100
                                    data['previous_close'] = float(price_info.get('regularMarketPreviousClose', {}).get('raw', 0))
                                    data['open_price'] = float(price_info.get('regularMarketOpen', {}).get('raw', 0))
                                    data['day_range_low'] = float(price_info.get('regularMarketDayLow', {}).get('raw', 0))
                                    data['day_range_high'] = float(price_info.get('regularMarketDayHigh', {}).get('raw', 0))
                                    data['volume'] = int(price_info.get('regularMarketVolume', {}).get('raw', 0))
                                    data['market_cap'] = price_info.get('marketCap', {}).get('fmt', 'N/A')
                                
                                summary = quote_store.get('summaryDetail', {})
                                if summary:
                                    data['range_52w_low'] = float(summary.get('fiftyTwoWeekLow', {}).get('raw', 0))
                                    data['range_52w_high'] = float(summary.get('fiftyTwoWeekHigh', {}).get('raw', 0))
                                    data['avg_volume'] = int(summary.get('averageDailyVolume10Day', {}).get('raw', 0))
                                
                                if data['last_price'] > 0:
                                    Actor.log.info(f'✓ Price data: ${data["last_price"]:.2f} ({data["percent_change"]:+.2%})')
                                    return data
                    
                    except (json.JSONDecodeError, KeyError, ValueError, IndexError) as e:
                        Actor.log.debug(f'Error parsing embedded JSON: {e}')
                        continue
            
            # Method 2: Fallback to fin-streamer elements
            price_elem = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
            if price_elem and price_elem.get('data-value'):
                data['last_price'] = float(price_elem['data-value'])
            
            # Get company name from h1
            h1 = soup.find('h1')
            if h1:
                data['company_name'] = h1.text.strip()
            
            # Extract all fin-streamer data
            for elem in soup.find_all('fin-streamer'):
                field = elem.get('data-field')
                value = elem.get('data-value') or elem.get('value')
                
                if not field or not value:
                    continue
                
                try:
                    if field == 'regularMarketPrice':
                        data['last_price'] = float(value)
                    elif field == 'regularMarketChange':
                        data['price_change'] = float(value)
                    elif field == 'regularMarketChangePercent':
                        data['percent_change'] = float(value) / 100
                    elif field == 'regularMarketPreviousClose':
                        data['previous_close'] = float(value)
                    elif field == 'regularMarketOpen':
                        data['open_price'] = float(value)
                    elif field == 'regularMarketDayLow':
                        data['day_range_low'] = float(value)
                    elif field == 'regularMarketDayHigh':
                        data['day_range_high'] = float(value)
                    elif field == 'fiftyTwoWeekLow':
                        data['range_52w_low'] = float(value)
                    elif field == 'fiftyTwoWeekHigh':
                        data['range_52w_high'] = float(value)
                    elif field == 'regularMarketVolume':
                        data['volume'] = int(float(value))
                    elif field == 'averageDailyVolume3Month':
                        data['avg_volume'] = int(float(value))
                    elif field == 'marketCap':
                        data['market_cap'] = value
                except (ValueError, TypeError) as e:
                    Actor.log.debug(f'Error parsing {field}: {e}')
            
            if data['last_price'] > 0:
                Actor.log.info(f'✓ Price data: ${data["last_price"]:.2f} ({data["percent_change"]:+.2%})')
            else:
                Actor.log.warning(f'⚠️  Could not extract price for {ticker}')
            
            return data
            
        except Exception as e:
            Actor.log.error(f'Error extracting price data: {str(e)}')
            return {
                'ticker': ticker,
                'company_name': ticker,
                'last_price': 0.0,
                'error': str(e)
            }
    
    async def _extract_news(self, ticker: str, max_news: int) -> List[Dict]:
        """Extract news articles for ticker"""
        news_url = f'https://finance.yahoo.com/quote/{ticker}/news'
        
        try:
            response = await self.client.get(news_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = []
            
            # Find news stream items
            news_items = soup.find_all('li', class_=re.compile('stream-item|js-stream-content'))
            
            for item in news_items[:max_news]:
                try:
                    # Extract headline
                    headline_elem = item.find('h3') or item.find('a')
                    if not headline_elem:
                        continue
                    
                    headline = headline_elem.text.strip()
                    if not headline:
                        continue
                    
                    # Extract link
                    link_elem = item.find('a', href=True)
                    url = link_elem['href'] if link_elem else ''
                    if url and not url.startswith('http'):
                        url = f'https://finance.yahoo.com{url}'
                    
                    # Extract source
                    source_elem = item.find('div', class_=re.compile('provider|source'))
                    source = source_elem.text.strip() if source_elem else 'Yahoo Finance'
                    
                    # Extract time
                    time_elem = item.find('time')
                    published_at = None
                    if time_elem:
                        published_at = time_elem.get('datetime')
                    
                    if not published_at:
                        published_at = datetime.utcnow().isoformat()
                    
                    articles.append({
                        'headline': headline,
                        'url': url,
                        'source': source,
                        'published_at': published_at,
                        'ticker': ticker.upper()
                    })
                    
                except Exception as e:
                    Actor.log.debug(f'Error parsing news item: {str(e)}')
                    continue
            
            Actor.log.info(f'✓ Found {len(articles)} news articles for {ticker}')
            return articles
            
        except Exception as e:
            Actor.log.error(f'Error extracting news: {str(e)}')
            return []
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

