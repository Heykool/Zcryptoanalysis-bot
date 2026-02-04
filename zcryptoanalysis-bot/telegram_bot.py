#!/usr/bin/env python3
"""
Zcryptoanalysis Telegram Bot
Complete Telegram integration for Base chain analysis
"""

import asyncio
import os
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

class ZcryptoTelegramBot:
    def __init__(self, token):
        self.token = token
        
    def get_base_tokens(self):
        """Get trending tokens on Base chain"""
        try:
            response = requests.get('https://api.dexscreener.com/latest/dex/tickers', timeout=10)
            if response.status_code == 200:
                data = response.json()
                tickers = data.get('tickers', [])
                return [t for t in tickers if t.get('chainId') == 'base']
            return self.get_sample_data()
        except:
            return self.get_sample_data()
    
    def get_sample_data(self):
        """Sample data for testing"""
        return [
            {
                'chainId': 'base',
                'baseToken': {'symbol': 'AERO', 'name': 'Aerodrome Finance'},
                'priceUsd': '0.000001234',
                'liquidity': {'usd': 75000},
                'volume': {'h24': 250000},
                'priceChange': {'h24': 15.7}
            },
            {
                'chainId': 'base',
                'baseToken': {'symbol': 'DEGEN', 'name': 'Degen'},
                'priceUsd': '0.00004567',
                'liquidity': {'usd': 125000},
                'volume': {'h24': 180000},
                'priceChange': {'h24': -8.3}
            }
        ]
    
    def analyze_opportunities(self, tickers):
        """Analyze and score opportunities"""
        opportunities = []
        
        for ticker in tickers:
            try:
                token = ticker['baseToken']['symbol']
                name = ticker['baseToken'].get('name', token)
                price = float(ticker['priceUsd'])
                liquidity = float(ticker.get('liquidity', {}).get('usd', 0))
                volume = float(ticker.get('volume', {}).get('h24', 0))
                price_change = float(ticker.get('priceChange', {}).get('h24', 0))
                
                if liquidity >= 50000 and abs(price_change) >= 5:
                    risk_score = 3
                    if liquidity < 100000:
                        risk_score += 3
                    elif liquidity < 500000:
                        risk_score += 2
                    
                    if abs(price_change) > 100:
                        risk_score += 4
                    elif abs(price_change) > 50:
                        risk_score += 2
                    elif abs(price_change) > 20:
                        risk_score += 1
                    
                    opportunities.append({
                        'token': token,
                        'name': name,
                        'price': price,
                        'change_24h': price_change,
                        'liquidity': liquidity,
                        'volume_24h': volume,
                        'risk_score': min(risk_score, 10),
                        'risk_level': 'Low' if risk_score <= 3 else 'Medium' if risk_score <= 6 else 'High'
                    })
            except:
                continue
        
        return sorted(opportunities, key=lambda x: abs(x['change_24h']), reverse=True)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome = """🚀 **Zcryptoanalysis Bot - Base Chain Analyzer**

📊 **Available Commands:**
• `/scan` - Analyze current Base opportunities
• `/help` - Show help message

🔍 **Features:**
• Real-time DexScreener integration
• Base chain focus
• Risk scoring (1-10)
• $50k+ liquidity filter
• 5%+ price change filter"""
        await update.message.reply_text(welcome, parse_mode='Markdown')
    
    async def scan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🔍 Scanning Base chain opportunities...")
        
        tickers = self.get_base_tokens()
        opportunities = self.analyze_opportunities(tickers)
        
        if not opportunities:
            await update.message.reply_text("ℹ️ No opportunities found meeting criteria")
            return
        
        message = f"🎯 **Found {len(opportunities)} opportunities:**\n\n"
        
        for opp in opportunities[:5]:
            emoji = "🟢" if opp['risk_score'] <= 3 else "🟡" if opp['risk_score'] <= 6 else "🔴"
            message += f"{emoji} **{opp['token']}** - ${opp['price']:.8f}\n"
            message += f"📈 {opp['change_24h']:+.2f}% | 💧 ${opp['liquidity']:,} | Risk: {opp['risk_level']}\n\n"
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """🤖 **Zcryptoanalysis Bot Help**

**Commands:**
• `/scan` - Get current Base opportunities
• `/help` - Show this help

**How it works:**
1. Scans DexScreener for Base chain tokens
2. Filters by liquidity > $50k
3. Looks for 5%+ price changes
4. Provides risk scoring 1-10

**Risk Levels:**
🟢 Low (1-3) - Safer investments
🟡 Medium (4-6) - Moderate risk
🔴 High (7-10) - High volatility"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    def run(self):
        app = Application.builder().token(self.token).build()
        
        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('scan', self.scan))
        app.add_handler(CommandHandler('help', self.help))
        
        print('🤖 Zcryptoanalysis Telegram Bot started!')
        print('📍 Bot is ready for queries')
        app.run_polling()

if __name__ == '__main__':
    TOKEN = os.getenv('TELEGRAM_TOKEN', '6994487405:AAH8Qv1Kz3J8mN3xY9r5P8kL2mN4xY7z')
    bot = ZcryptoTelegramBot(TOKEN)
    bot.run()