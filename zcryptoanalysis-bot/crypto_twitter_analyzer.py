#!/usr/bin/env python3
"""
Twitter sentiment analyzer for small crypto accounts
Integrates with DexScreener data for Base chain analysis
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterAnalyzer:
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
        self.base_url = 'https://api.twitter.com/2'
        self.small_account_range = (100, 10000)  # 100-10k followers
        
    async def search_crypto_tweets(self, keywords: List[str], max_results: int = 100) -> List[Dict[str, Any]]:
        """Search for crypto tweets from small accounts"""
        headers = {'Authorization': f'Bearer {self.bearer_token}'}
        
        # Build query for Base chain crypto mentions
        query_terms = [
            'base chain', 'base crypto', 'base token', 'base launch',
            'new listing base', 'base dex', 'base trading'
        ]
        query = ' OR '.join(f'"{term}"' for term in query_terms)
        query += ' -is:retweet lang:en'
        
        url = f'{self.base_url}/tweets/search/recent'
        params = {
            'query': query,
            'max_results': max_results,
            'tweet.fields': 'created_at,author_id,public_metrics',
            'user.fields': 'public_metrics,verified',
            'expansions': 'author_id'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.filter_small_accounts(data)
                    else:
                        logger.error(f'Twitter API error: {response.status}')
                        return []
        except Exception as e:
            logger.error(f'Twitter search error: {e}')
            return []
    
    def filter_small_accounts(self, data: Dict) -> List[Dict[str, Any]]:
        """Filter tweets from small crypto accounts"""
        tweets = []
        users = {user['id']: user for user in data.get('includes', {}).get('users', [])}
        
        for tweet in data.get('data', []):
            author_id = tweet.get('author_id')
            if author_id in users:
                user = users[author_id]
                followers = user.get('public_metrics', {}).get('followers_count', 0)
                
                if self.small_account_range[0] <= followers <= self.small_account_range[1]:
                    sentiment = self.analyze_sentiment(tweet.get('text', ''))
                    urgency = self.detect_urgency(tweet.get('text', ''))
                    
                    tweets.append({
                        'id': tweet['id'],
                        'text': tweet['text'],
                        'author': user['username'],
                        'followers': followers,
                        'created_at': tweet['created_at'],
                        'sentiment': sentiment,
                        'urgency_score': urgency,
                        'verified': user.get('verified', False)
                    })
        
        return tweets
    
    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis"""
        bullish_words = ['buy', 'moon', 'gem', 'rocket', 'pump', 'bullish', 'alpha']
        bearish_words = ['sell', 'dump', 'bearish', 'rug', 'down', 'crash']
        
        text_lower = text.lower()
        bullish_count = sum(1 for word in bullish_words if word in text_lower)
        bearish_count = sum(1 for word in bearish_words if word in text_lower)
        
        if bullish_count > bearish_count:
            return 'bullish'
        elif bearish_count > bullish_count:
            return 'bearish'
        else:
            return 'neutral'
    
    def detect_urgency(self, text: str) -> int:
        """Detect urgency level 0-3"""
        urgency_words = [
            'now', 'quick', 'hurry', 'early', 'first', 'breaking',
            'just launched', 'new listing', 'fresh', 'opportunity'
        ]
        
        text_lower = text.lower()
        score = sum(2 if phrase in text_lower else 1 
                   for word in urgency_words 
                   for phrase in [word, word.replace(' ', '')])
        
        return min(score, 3)

class UnifiedAnalyzer:
    def __init__(self, twitter_token: str):
        self.twitter = TwitterAnalyzer(twitter_token)
        # DexScreener integration will be added
        
    async def combined_analysis(self) -> Dict[str, Any]:
        """Run both Twitter and DexScreener analysis"""
        twitter_signals = await self.twitter.search_crypto_tweets(['base', 'gem'])
        
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'twitter_signals': twitter_signals[:20],
            'total_signals': len(twitter_signals)
        }

if __name__ == '__main__':
    # Configuration
    TWITTER_BEARER_TOKEN = 'YOUR_TWITTER_BEARER_TOKEN'
    
    async def main():
        analyzer = UnifiedAnalyzer(TWITTER_BEARER_TOKEN)
        result = await analyzer.combined_analysis()
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())