"""
Agentic Stock Actor - Main Entry Point

AI-powered stock timing agent that:
1. Scrapes Yahoo Finance (price data + news)
2. Scrapes Reddit (sentiment from r/wallstreetbets, r/stocks, etc.)
3. Analyzes sentiment using OpenAI GPT-4
4. Generates BUY/SELL/HOLD/WATCH signals for swing trading

Built for Apify 1M Challenge Hackathon
"""
from apify import Actor
from datetime import datetime
import asyncio

from src.scrapers.yahoo_finance import YahooFinanceScraper
from src.scrapers.reddit import RedditScraper
from src.analyzers.sentiment import SentimentAnalyzer
from src.analyzers.trading_signal import TradingSignalGenerator
from src.notifications import SignalChangeDetector


async def analyze_ticker(
    ticker: str,
    yahoo_scraper: YahooFinanceScraper,
    reddit_scraper: RedditScraper,
    sentiment_analyzer: SentimentAnalyzer,
    signal_generator: TradingSignalGenerator,
    signal_detector: SignalChangeDetector,
    config: dict
) -> dict:
    """Run complete analysis pipeline for a single ticker"""
    
    Actor.log.info(f'\n{"="*60}')
    Actor.log.info(f'📈 ANALYZING: {ticker}')
    Actor.log.info(f'{"="*60}')
    
    # Step 1: Scrape Yahoo Finance
    yahoo_data = await yahoo_scraper.scrape_ticker(
        ticker,
        max_news=config.get('max_news', 20)
    )
    
    if not yahoo_data:
        Actor.log.error(f'Failed to get Yahoo Finance data for {ticker}')
        return None
    
    price_data = yahoo_data['price_data']
    news_articles = yahoo_data['news_articles']
    
    # Step 2: Scrape Reddit
    reddit_posts = await reddit_scraper.scrape_ticker(
        ticker,
        subreddits=config.get('subreddits', ['wallstreetbets', 'stocks']),
        max_posts=config.get('max_reddit_posts', 50)
    )
    
    # Step 3: Analyze Sentiment
    news_sentiment = sentiment_analyzer.analyze_news_sentiment(news_articles)
    reddit_sentiment = sentiment_analyzer.analyze_reddit_sentiment(reddit_posts)
    
    overall_sentiment = sentiment_analyzer.synthesize_sentiment(
        ticker,
        news_sentiment,
        reddit_sentiment
    )
    
    # Step 4: Generate Trading Signal
    trading_signal = signal_generator.generate_signal(
        ticker,
        price_data,
        overall_sentiment
    )
    
    # Step 5: Check for signal changes and send notifications
    change_info = await signal_detector.check_and_notify(
        ticker,
        trading_signal['signal'],
        trading_signal['confidence']
    )
    
    # Compile complete analysis result
    result = {
        'ticker': ticker,
        'timestamp': datetime.utcnow().isoformat(),
        
        # Trading Signal (main output)
        'signal': trading_signal['signal'],
        'confidence': trading_signal['confidence'],
        'reasoning': trading_signal['reasoning'],
        'key_catalysts': trading_signal['key_catalysts'],
        'risk_level': trading_signal['risk_level'],
        'entry_strategy': trading_signal['entry_strategy'],
        
        # Price Context
        'current_price': price_data['last_price'],
        'price_change': price_data.get('price_change', 0),
        'percent_change': price_data.get('percent_change', 0),
        'position_52w': trading_signal['position_52w'],
        'volume_ratio': trading_signal['volume_ratio'],
        
        # Sentiment Context
        'sentiment_score': overall_sentiment['overall_sentiment'],
        'sentiment_label': overall_sentiment['sentiment_label'],
        'news_sentiment': overall_sentiment['news_sentiment'],
        'reddit_sentiment': overall_sentiment['reddit_sentiment'],
        'community_mood': overall_sentiment['community_mood'],
        
        # Market-Moving Events
        'market_moving_events': overall_sentiment.get('market_moving_events', []),
        'key_topics': overall_sentiment.get('key_topics', []),
        
        # Data Counts
        'news_count': len(news_articles),
        'reddit_posts_count': len(reddit_posts),
        
        # Signal Change Info
        'signal_changed': change_info['signal_changed'],
        'previous_signal': change_info['previous_signal'],
        'change_type': change_info['change_type'],
        'notification_sent': change_info['notification_sent'],
        
        # Full Data (optional, for debugging)
        'price_data': price_data,
        'top_news': news_articles[:5],  # Top 5 articles
        'top_reddit_posts': sorted(
            reddit_posts, 
            key=lambda x: x.get('score', 0), 
            reverse=True
        )[:5]  # Top 5 posts by score
    }
    
    # Log detailed summary
    Actor.log.info(f'\n{"="*60}')
    Actor.log.info(f'📊 ANALYSIS COMPLETE FOR {ticker}')
    Actor.log.info(f'{"="*60}')
    Actor.log.info(f'\n🎯 TRADING SIGNAL:')
    signal_emoji = {'BUY': '🟢', 'SELL': '🔴', 'HOLD': '🟡', 'WATCH': '🔵'}
    Actor.log.info(f'   {signal_emoji.get(result["signal"], "⚪")} {result["signal"]} (Confidence: {result["confidence"]:.0%})')
    Actor.log.info(f'\n💰 PRICE DATA:')
    Actor.log.info(f'   Current: ${result["current_price"]:.2f}')
    Actor.log.info(f'   Change: {result["price_change"]:+.2f} ({result["percent_change"]:+.2%})')
    Actor.log.info(f'   52W Position: {result["position_52w"]:.1%}')
    Actor.log.info(f'\n💭 SENTIMENT:')
    Actor.log.info(f'   Overall: {result["sentiment_score"]:+.2f} ({result["sentiment_label"].upper()})')
    Actor.log.info(f'   News: {result["news_sentiment"]:+.2f}')
    Actor.log.info(f'   Reddit: {result["reddit_sentiment"]:+.2f}')
    Actor.log.info(f'   Community: {result["community_mood"].upper()}')
    Actor.log.info(f'\n📝 REASONING:')
    Actor.log.info(f'   {result["reasoning"]}')
    if result['key_catalysts']:
        Actor.log.info(f'\n🔑 KEY CATALYSTS:')
        for catalyst in result['key_catalysts']:
            Actor.log.info(f'   • {catalyst}')
    if result['market_moving_events']:
        Actor.log.info(f'\n⚠️  MARKET-MOVING EVENTS:')
        for event in result['market_moving_events']:
            Actor.log.info(f'   • {event}')
    Actor.log.info(f'\n⚖️  RISK LEVEL: {result["risk_level"].upper()}')
    Actor.log.info(f'\n💡 ENTRY STRATEGY:')
    Actor.log.info(f'   {result["entry_strategy"]}')
    Actor.log.info(f'\n{"="*60}\n')
    
    return result


async def main():
    """Main actor entry point"""
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        
        tickers = actor_input.get('tickers', [])
        openai_api_key = actor_input.get('openaiApiKey')
        
        if not tickers:
            Actor.log.error('❌ No tickers provided in input')
            return
        
        if not openai_api_key:
            Actor.log.error('❌ OpenAI API key is required')
            return
        
        # Configuration
        config = {
            'max_news': actor_input.get('maxNewsPerTicker', 20),
            'max_reddit_posts': actor_input.get('maxRedditPostsPerTicker', 50),
            'subreddits': actor_input.get('subreddits', [
                'wallstreetbets',
                'stocks',
                'investing',
                'StockMarket'
            ]),
            'enable_notifications': actor_input.get('enableNotifications', False)
        }
        
        # Log startup
        Actor.log.info('\n' + '='*60)
        Actor.log.info('🚀 AGENTIC STOCK ACTOR')
        Actor.log.info('   AI-Powered Trading Signal Generator')
        Actor.log.info('='*60)
        Actor.log.info(f'Tickers to analyze: {", ".join(tickers)}')
        Actor.log.info(f'Subreddits: {", ".join(config["subreddits"])}')
        Actor.log.info(f'Max news per ticker: {config["max_news"]}')
        Actor.log.info(f'Max Reddit posts per ticker: {config["max_reddit_posts"]}')
        Actor.log.info('='*60 + '\n')
        
        # Initialize components
        yahoo_scraper = YahooFinanceScraper()
        reddit_scraper = RedditScraper()
        sentiment_analyzer = SentimentAnalyzer(openai_api_key)
        signal_generator = TradingSignalGenerator(openai_api_key)
        signal_detector = SignalChangeDetector()
        await signal_detector.initialize()
        
        # Process each ticker
        results = []
        for i, ticker in enumerate(tickers, 1):
            Actor.log.info(f'\n[{i}/{len(tickers)}] Processing {ticker}...')
            
            try:
                result = await analyze_ticker(
                    ticker,
                    yahoo_scraper,
                    reddit_scraper,
                    sentiment_analyzer,
                    signal_generator,
                    signal_detector,
                    config
                )
                
                if result:
                    # Push to dataset
                    await Actor.push_data(result)
                    results.append(result)
                    Actor.log.info(f'✅ {ticker} analysis complete!')
                else:
                    Actor.log.warning(f'⚠️  {ticker} analysis failed')
                
            except Exception as e:
                Actor.log.error(f'❌ Error analyzing {ticker}: {str(e)}')
                continue
        
        # Cleanup
        await yahoo_scraper.close()
        await reddit_scraper.close()
        
        # Final summary
        Actor.log.info('\n' + '='*60)
        Actor.log.info('📊 FINAL SUMMARY')
        Actor.log.info('='*60)
        
        buy_signals = [r for r in results if r['signal'] == 'BUY']
        sell_signals = [r for r in results if r['signal'] == 'SELL']
        hold_signals = [r for r in results if r['signal'] == 'HOLD']
        watch_signals = [r for r in results if r['signal'] == 'WATCH']
        
        Actor.log.info(f'Total analyzed: {len(results)}/{len(tickers)}')
        Actor.log.info(f'🟢 BUY signals: {len(buy_signals)}')
        Actor.log.info(f'🔴 SELL signals: {len(sell_signals)}')
        Actor.log.info(f'🟡 HOLD signals: {len(hold_signals)}')
        Actor.log.info(f'🔵 WATCH signals: {len(watch_signals)}')
        
        if buy_signals:
            Actor.log.info(f'\n🟢 BUY OPPORTUNITIES:')
            for r in buy_signals:
                Actor.log.info(f'   {r["ticker"]}: ${r["current_price"]:.2f} ({r["confidence"]:.0%} confidence)')
        
        if sell_signals:
            Actor.log.info(f'\n🔴 SELL RECOMMENDATIONS:')
            for r in sell_signals:
                Actor.log.info(f'   {r["ticker"]}: ${r["current_price"]:.2f} ({r["confidence"]:.0%} confidence)')
        
        # Show signal change summary
        Actor.log.info('\n' + '='*60)
        Actor.log.info('📊 SIGNAL CHANGE SUMMARY')
        Actor.log.info('='*60)
        
        changes = [r for r in results if r.get('signal_changed')]
        if changes:
            Actor.log.info(f'Signals changed: {len(changes)}/{len(results)}')
            for r in changes:
                Actor.log.info(f'  {r["ticker"]}: {r["change_type"]} {"🔔" if r["notification_sent"] else ""}')
        else:
            Actor.log.info('No signal changes detected')
        
        Actor.log.info('\n' + '='*60)
        Actor.log.info('✅ AGENTIC STOCK ACTOR COMPLETED!')
        Actor.log.info('='*60 + '\n')


if __name__ == '__main__':
    asyncio.run(main())

