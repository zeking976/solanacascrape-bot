from fastapi import FastAPI
import uvicorn
import asyncio
from telethon import TelegramClient, events
import os
import re
from datetime import datetime
import httpx

# Environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']  # Your username or chat ID (e.g., 'me')
channel_to_monitor = os.environ['CHANNEL_NAME']  # Channel username

# Solana contract pattern
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# FastAPI app (required for Render Web Service)
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Baby Bot is live and watching!"}

# Initialize Telegram client
client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)

    for addr in addresses:
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
        token_info = await get_token_info(addr)

        message = f"""👾 *New Contract Detected! 🔑*

🔗 *Address:* `{addr}`  
💰 *Token:* `{token_info['symbol']}`  
📊 *Market Cap:* `${token_info['market_cap']}`  
🕒 *Time:* {timestamp}

💬 _CA successfully scraped from channel._
🚀 *Get in early or stay informed!* ⚡
"""
        await client.send_message(receiver, message, parse_mode='markdown')

async def get_token_info(ca: str):
    try:
        url = f'https://api.dexscreener.com/latest/dex/search/?q={ca}'
        async with httpx.AsyncClient() as session:
            res = await session.get(url, timeout=10)
            data = res.json()

        if 'pairs' in data and data['pairs']:
            pair = data['pairs'][0]
            market_cap = pair.get('fdv', 'N/A')
            symbol = pair.get('baseToken', {}).get('symbol', 'N/A')

            # Format market cap as readable
            if isinstance(market_cap, (int, float)):
                market_cap = f"{int(market_cap):,}"
            else:
                market_cap = "N/A"

            return {
                "symbol": symbol,
                "market_cap": market_cap
            }
        else:
            return {
                "symbol": "Unknown",
                "market_cap": "Unknown"
            }
    except Exception as e:
        return {
            "symbol": "Error",
            "market_cap": "Error"
        }

# Startup function
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    loop.create_task(client.run_until_disconnected())
