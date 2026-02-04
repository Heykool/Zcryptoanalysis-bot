# Zcryptoanalysis Bot

A comprehensive cryptocurrency analysis bot for Base chain focusing on new token launches with social sentiment analysis.

## Features

- **DexScreener Integration**: Real-time Base chain pair analysis
- **Twitter Sentiment**: Small account analysis (100-10k followers)
- **Risk Scoring**: Multi-factor risk assessment
- **Telegram Bot**: Real-time alerts and analysis

## Files

- `crypto_final.py` - Main DexScreener analyzer
- `crypto_twitter_analyzer.py` - Twitter sentiment analysis
- `crypto_clean.py` - Clean/refactored version

## Setup

1. Install dependencies: `pip install aiohttp python-telegram-bot`
2. Set Twitter API bearer token
3. Configure Telegram bot token
4. Run: `python crypto_final.py`

## Risk Factors

- Liquidity thresholds ($50k minimum)
- Social sentiment scoring
- Token age verification
- Volume spike detection