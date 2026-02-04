#!/usr/bin/env python3
"""
Crypto Analysis Bot for Base Chain
DexScreener integration with risk scoring
"""

import asyncio
import aiohttp
import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CryptoAnalyzer:
    def __init__(self):
        self.base_url = 'https://api.dexscreener.com/latest'
        self.min_liquidity = 50000
        
    async def scan_base_pairs(self) -> List[Dict[str, Any]]:
        """Scan Base chain for crypto opportunities"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f'{self.base_url}/pairs/trending'
                async with session.get(url) as response:
                    data = await response.json()
                    pairs = data.get('pairs', [])
                    base_pairs = [p for p in pairs if p.get('chainId') == 'base']
                    return self.filter_opportunities(base_pairs)
        except Exception as e:
            logger.error(f'Base scan error: {e}')
            return []
    
    def filter_opportunities(self, pairs: List[Dict]) -> List[Dict[str, Any]]:
        """Filter and score crypto opportunities"""
        opportunities = []
        
        for pair in pairs:
            try:
                if not self.is_valid_pair(pair):
                    continue
                    
                liquidity = float(pair['liquidity']['usd'])
                volume_24h = float(pair['volume']['h24'])
                change_24h = float(pair['priceChange']['h24'])
                
                # Focus on significant movers with good volume
                if abs(change_24h) > 5 and volume_24h > 10000:
                    risk_score = self.calculate_risk_score(pair)
                    
                    opportunities.append({
                        'token': pair['baseToken']['symbol'],
                        'name': pair['baseToken'].get('name', ''),
                        'price': float(pair['priceUsd']),
                        'volume_24h': volume_24h,
                        'liquidity': liquidity,
                        'change_24h': change_24h,
                        'risk_score': risk_score,
                        'risk_level': self.get_risk_level(risk_score),
                        'pair_address': pair.get('pairAddress', ''),
                        'created_at': str(datetime.utcnow())
                    })
            except Exception as e:
                logger.debug(f'Skipping invalid pair: {e}')
                continue
                
        return sorted(opportunities, key=lambda x: abs(x['change_24h']), reverse=True)[:20]
    
    def is_valid_pair(self, pair: Dict) -> bool:
        """Validate if pair meets basic criteria"""
        try:
            if pair.get('chainId') != 'base':
                return False
            if 'liquidity' not in pair or 'usd' not in pair['liquidity']:
                return False
            liquidity = float(pair['liquidity']['usd'])
            return liquidity >= self.min_liquidity
        except (KeyError, ValueError, TypeError):
            return False
    
    def calculate_risk_score(self, pair: Dict) -> int:
        """Calculate risk score 1-10 based on multiple factors"""
        try:
            score = 3  # Base score
            
            # Liquidity risk
            liquidity = float(pair['liquidity']['usd'])
            if liquidity < 100000:
                score += 3
            elif liquidity < 500000:
                score += 2
            elif liquidity < 1000000:
                score += 1
                
            # Volatility risk
            change_24h = abs(float(pair['priceChange']['h24']))
            if change_24h > 500:
                score += 4
            elif change_24h > 200:
                score += 3
            elif change_24h > 100:
                score += 2
            elif change_24h > 50:
                score += 1
                
            # Volume risk
            volume_24h = float(pair['volume']['h24'])
            if volume_24h < 50000:
                score += 2
            elif volume_24h < 100000:
                score += 1
                
            return min(score, 10)
        except:
            return 8
    
    def get_risk_level(self, score: int) -> str:
        """Convert risk score to human-readable level"""
        if score <= 3:
            return "Low"
        elif score <= 5:
            return "Medium"
        elif score <= 7:
            return "High"
        else:
            return "Extreme"
    
    async def run_analysis(self) -> Dict[str, Any]:
        """Run complete analysis and return results"""
        logger.info('🔍 Starting Base chain crypto analysis...')
        
        opportunities = await self.scan_base_pairs()
        
        if opportunities:
            report = {
                'timestamp': str(datetime.utcnow()),
                'opportunities': opportunities,
                'total_found': len(opportunities),
                'summary': {
                    'low_risk': len([o for o in opportunities if o['risk_score'] <= 3]),
                    'medium_risk': len([o for o in opportunities if 3 < o['risk_score'] <= 5]),
                    'high_risk': len([o for o in opportunities if o['risk_score'] > 5])
                }
            }
            
            # Save report
            reports_dir = '/tmp/crypto-reports'
            os.makedirs(reports_dir, exist_ok=True)
            filename = f"{reports_dir}/analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f'✅ Analysis complete. Found {len(opportunities)} opportunities')
            return report
        else:
            logger.info('ℹ️  No opportunities found')
            return {'timestamp': str(datetime.utcnow()), 'opportunities': [], 'total_found': 0}

async def main():
    """Main function for testing"""
    analyzer = CryptoAnalyzer()
    report = await analyzer.run_analysis()
    
    if report['opportunities']:
        print(f"\n🎯 Found {len(report['opportunities'])} Base chain opportunities:")
        for i, opp in enumerate(report['opportunities'][:5]):
            print(f"{i+1}. {opp['token']} - ${opp['price']:.8f} ({opp['change_24h']:+.2f}%) - Risk: {opp['risk_level']} ({opp['risk_score']}/10)")
            print(f"   💰 Liquidity: ${opp['liquidity']:,.0f} | 📊 Volume: ${opp['volume_24h']:,.0f}")
    
    return report

if __name__ == '__main__':
    asyncio.run(main())