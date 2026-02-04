#!/usr/bin/env python3
"""
Crypto Analysis Bot for Base Chain
DexScreener integration with risk scoring
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CryptoAnalyzer:
    def __init__(self):
        self.base_url = 'https://api.dexscreener.com/latest'
        self.min_liquidity = 50000
        
    async def scan_base_pairs(self) -> List[Dict[str, Any]]:
        try:
            async with aiohttp.ClientSession() as session:
                url = f'{self.base_url}/pairs/basesol'
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.filter_opportunities(data.get('pairs', []))
                    else:
                        return await self.scan_trending()
        except Exception as e:
            logger.error(f'Error: {e}')
            return await self.scan_trending()
    
    async def scan_trending(self) -> List[Dict[str, Any]]:
        try:
            async with aiohttp.ClientSession() as session:
                url = f'{self.base_url}/pairs/trending'
                async with session.get(url) as response:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    base_pairs = [p for p in pairs if p.get('chainId') == 'base']
                    return self.filter_opportunities(base_pairs)
        except Exception as e:
            logger.error(f'Trending scan error: {e}')
            return []
    
    def filter_opportunities(self, pairs: List[Dict]) -> List[Dict[str, Any]]:
        opportunities = []
        for pair in pairs:
            try:
                if not self.is_valid_pair(pair):
                    continue
                    
                liquidity = float(pair['liquidity']['usd'])
                volume_24h = float(pair['volume']['h24'])
                change_24h = float(pair['priceChange']['h24'])
                
                if abs(change_24h) > 10 and volume_24h > 10000:
                    risk_score = self.calculate_risk_score(pair)
                    opportunities.append({
                        'token': pair['baseToken']['symbol'],
                        'name': pair['baseToken'].get('name', ''),
                        'price': float(pair['priceUsd']),
                        'volume_24h': volume_24h,
                        'liquidity': liquidity,
                        'change_24h': change_24h,
                        'risk_score': risk_score,
                        'created_at': str(datetime.utcnow())
                    })
            except Exception as e:
                continue
                
        return sorted(opportunities, key=lambda x: abs(x['change_24h']), reverse=True)[:15]
    
    def is_valid_pair(self, pair: Dict) -> bool:
        try:
            if pair.get('chainId') != 'base':
                return False
            liquidity = float(pair['liquidity']['usd'])
            return liquidity >= self.min_liquidity
        except:
            return False
    
    def calculate_risk_score(self, pair: Dict) -> int:
        try:
            score = 3
            liquidity = float(pair['liquidity']['usd'])
            change_24h = abs(float(pair['priceChange']['h24']))
            
            if liquidity < 100000:
                score += 2
            elif liquidity < 500000:
                score += 1
                
            if change_24h > 200:
                score += 3
            elif change_24h > 100:
                score += 2
            elif change_24h > 50:
                score += 1
                
            return min(score, 10)
        except:
            return 8

async def main():
    analyzer = CryptoAnalyzer()
    
    logger.info('Starting Base chain analysis...')
    opportunities = await analyzer.scan_base_pairs()
    
    if opportunities:
        report = {
            'timestamp': str(datetime.utcnow()),
            'opportunities': opportunities,
            'total_found': len(opportunities)
        }
        
        filename = f'/root/crypto-analysis/reports/analysis_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.json'
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f'Analysis complete. Found {len(opportunities)} opportunities')
        for i, opp in enumerate(opportunities[:5]):
            logger.info(f'{i+1}. {opp[\"token\"]} - ${opp[\"price\"]:.6f} ({opp[\"change_24h\"]:.2f}%) - Risk: {opp[\"risk_score\"]}/10')
    else:
        logger.info('No opportunities found')

if __name__ == '__main__':
    asyncio.run(main())