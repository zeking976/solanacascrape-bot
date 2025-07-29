from fastapi import FastAPI
import uvicorn
import asyncio
from telethon import TelegramClient, events
import os
import re
import requests
from datetime import datetime

# Load config from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']
channel_to_monitor = os.environ['CHANNEL_NAME']

# FastAPI app for Render to keep alive
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Solana bot running"}

# Solana address regex
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Setup Telegram bot
client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

# Function to fetch market cap from Dexscreener
def get_market_cap(ca):
    try:
        url = f"https://api.dexscreener.com/latest/dex/search?q={ca}"
        res = requests.get(url)
        data = res.json()
        pair = data.get("pairs", [])[0]
        market_cap = pair.get("fdv") or pair.get("marketCap") or None
        if market_cap:
            market_cap = int(market_cap)
            return f"${market_cap:,.0f}"
    except:
        pass
    return "Market cap not found"

# Telegram event handler
@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        for addr in addresses:
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            market_cap = get_market_cap(addr)

            message = f"""👾 *New Contract Detected!*

🔗 *Address:* `{addr}`
📈 *Market Cap:* _{market_cap}_  
📆 *Timestamp:* _{now}_  
💬 _CA successfully scraped✅ from monitored channel📣._
🚀 *Get in early or stay informed!*⚡
"""
            await client.send_message(receiver, message, parse_mode='markdown')

# Keep Telethon running in background
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(client.run_until_disconnected())
