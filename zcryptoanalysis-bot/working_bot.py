#!/usr/bin/env python3
"""
Zcryptoanalysis Bot - Working Version
Uses requests for better HTTP handling
"""

import json
import requests
from datetime import datetime
import os

class ZcryptoAnalyzer:
    def __init__(self):
        self.base_url = 'https://api.dexscreener.com/latest'
        self.min_liquidity = 50000
        
    def get_base_tokens(self):
        """Get trending tokens on Base chain"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Try trending endpoint
            response = requests.get(f'{self.base_url}/pairs/trending', headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            pairs = data.get('pairs', [])
            
            # Filter for Base chain
            base_pairs = [p for p in pairs if p.get('chainId') == 'base']
            return base_pairs
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            return []
    
    def analyze_opportunities(self, pairs):
        """Analyze and score opportunities"""
        opportunities = []
        
        for pair in pairs:
            try:
                if not self.is_valid_pair(pair):
                    continue
                
                # Extract data
                token = pair['baseToken']['symbol']
                name = pair['baseToken'].get('name', token)
                price = float(pair['priceUsd'])
                liquidity = float(pair['liquidity']['usd'])
                volume_24h = float(pair['volume']['h24'])
                change_24h = float(pair['priceChange']['h24'])
                
                # Filter criteria
                if abs(change_24h) >= 5 and volume_24h >= 10000:
                    # Risk scoring
                    risk_score = self.calculate_risk(liquidity, volume_24h, abs(change_24h))
                    
                    opportunities.append({
                        'token': token,
                        'name': name,
                        'price': price,
                        'change_24h': change_24h,
                        'liquidity': liquidity,
                        'volume_24h': volume_24h,
                        'risk_score': risk_score,
                        'risk_level': self.get_risk_level(risk_score),
                        'timestamp': str(datetime.utcnow())
                    })
                    
            except Exception as e:
                continue
        
        return sorted(opportunities, key=lambda x: abs(x['change_24h']), reverse=True)
    
    def is_valid_pair(self, pair):
        """Validate pair data"""
        required = ['chainId', 'liquidity', 'volume', 'priceChange', 'baseToken']
        if not all(k in pair for k in required):
            return False
        
        try:
            liquidity = float(pair['liquidity']['usd'])
            return pair['chainId'] == 'base' and liquidity >= self.min_liquidity
        except:
            return False
    
    def calculate_risk(self, liquidity, volume, price_change):
        """Calculate risk score 1-10"""
        score = 3  # Base score
        
        # Liquidity risk
        if liquidity < 100000:
            score += 3
        elif liquidity < 500000:
            score += 2
        elif liquidity < 1000000:
            score += 1
        
        # Volatility risk
        if price_change > 200:
            score += 4
        elif price_change > 100:
            score += 3
        elif price_change > 50:
            score += 2
        elif price_change > 20:
            score += 1
        
        # Volume risk
        if volume < 50000:
            score += 2
        elif volume < 100000:
            score += 1
        
        return min(score, 10)
    
    def get_risk_level(self, score):
        """Get risk level description"""
        if score <= 3:
            return "🟢 Low"
        elif score <= 5:
            return "🟡 Medium"
        elif score <= 7:
            return "🟠 High"
        else:
            return "🔴 Extreme"
    
    def run_analysis(self):
        """Run complete analysis"""
        print("🚀 Starting Zcryptoanalysis Bot...")
        print("=" * 60)
        
        # Get data
        pairs = self.get_base_tokens()
        if not pairs:
            print("❌ No Base chain tokens found")
            return []
        
        print(f"📊 Analyzing {len(pairs)} Base pairs...")
        
        # Analyze opportunities
        opportunities = self.analyze_opportunities(pairs)
        
        if not opportunities:
            print("ℹ️  No opportunities meeting criteria")
            return []
        
        # Display results
        print(f"\n🎯 Found {len(opportunities)} opportunities:")
        print("-" * 60)
        
        for i, opp in enumerate(opportunities[:10]):
            print(f"{i+1}. {opp['token']} - {opp['name'][:40]}")
            print(f"   💰 Price: \${opp['price']:.8f}")
            print(f"   📈 Change: {opp['change_24h']:+.2f}%")
            print(f"   💧 Liquidity: \${opp['liquidity']:,.0f}")
            print(f"   📊 Volume: \${opp['volume_24h']:,.0f}")
            print(f"   {opp['risk_level']} Risk ({opp['risk_score']}/10)")
            print()
        
        # Summary
        total = len(opportunities)
        low_risk = len([o for o in opportunities if o['risk_score'] <= 3])
        high_risk = len([o for o in opportunities if o['risk_score'] > 7])
        
        print("📈 Analysis Summary:")
        print(f"   Total opportunities: {total}")
        print(f"   Low risk: {low_risk}")
        print(f"   High risk: {high_risk}")
        
        return opportunities

# Test the bot
if __name__ == '__main__':
    try:
        import requests
        analyzer = ZcryptoAnalyzer()
        results = analyzer.run_analysis()
        
        if results:
            print("✅ Zcryptoanalysis Bot is working perfectly!")
            print("🚀 Ready for Telegram integration")
        else:
            print("⚠️ Bot ran but found no opportunities")
            
    except ImportError:
        print("❌ Installing requests...")
        os.system('pip3 install requests')
        
    except Exception as e:
        print(f"❌ Bot error: {e}")
        print("🔄 Check internet connection and API availability")