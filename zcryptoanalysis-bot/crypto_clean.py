#!/usr/bin/env python3
# Simple crypto scanner for Base chain
import asyncio
import aiohttp
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoScanner:
    async def scan(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://api.dexscreener.com/latest/pairs/trending'
                async with session.get(url) as response:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    
                    base_pairs = [p for p in pairs if p.get('chainId') == 'base']
                    
                    results = []
                    for pair in base_pairs:
                        try:
                            if float(pair['liquidity']['usd']) >= 50000:
                                results.append({
                                    'token': pair['baseToken']['symbol'],
                                    'price': float(pair['priceUsd']),
                                    'volume': float(pair['volume']['h24']),
                                    'liquidity': float(pair['liquidity']['usd']),
                                    'change': float(pair['priceChange']['h24'])
                                })
                        except:
                            continue
                    
                    return sorted(results, key=lambda x: abs(x['change']), reverse=True)[:10]
        except Exception as e:
            logger.error(f'Scan failed: {e}')
            return []

async def main():
    scanner = CryptoScanner()
    results = await scanner.scan()
    
    if results:
        filename = f'analysis_{datetime.now().strftime(\"%Y%m%d_%H%M%S\")}.json'
        with open(f'/root/crypto-analysis/reports/{filename}', 'w') as f:
            json.dump({'tokens': results, 'count': len(results)}, f, indent=2)
        
        print(f'Found {len(results)} Base tokens')
        for token in results[:3]:
            print(f'{token[\"token\"]}: ${token[\"price\"]:.6f} ({token[\"change\"]:.2f}%)')
    else:
        print('No Base tokens found')

if __name__ == '__main__':
    asyncio.run(main())