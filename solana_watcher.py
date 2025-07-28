from fastapi import FastAPI
import uvicorn
import asyncio
from telethon import TelegramClient, events
import os
import re
from datetime import datetime

# Load config from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']
channel_to_monitor = os.environ['CHANNEL_NAME']

# Solana address pattern (base58)
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Coin name detection pattern
coin_pattern = r"(?:Name|Coin|Token)\s*[:\-]?\s*([A-Z0-9\-]+)"

# Create FastAPI app (required to bind port)
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot is running"}

# Telegram client setup
client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    coin_matches = re.findall(coin_pattern, text, re.IGNORECASE)
    coin_name = coin_matches[0] if coin_matches else "Unknown"

    if addresses:
        for addr in addresses:
            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            message = f"""👾 *New Contract Detected!*

🪙 *Coin Name:* `{coin_name}`
🔗 *Address:* `{addr}`
🕒 *Time:* _{now}_

💬 _CA successfully scraped ✅ from monitored channel 📣._
🚀 *Get in early or stay informed!* ⚡
"""
            print(f"Forwarding: {addr}")
            await client.send_message(receiver, message, parse_mode='markdown')

# Run the Telegram client in background with FastAPI
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(client.run_until_disconnected())
