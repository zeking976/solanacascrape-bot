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

# Solana address pattern
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# FastAPI app to keep service alive
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Solana Watcher Bot is running"}

# Telegram client
client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)

    if addresses:
        for addr in addresses:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            msg = f"📡 *Detected Solana Contract Address:*\n`{addr}`\n🕒 *Time:* {timestamp}"

            # Get market
