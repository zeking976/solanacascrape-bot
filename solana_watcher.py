from fastapi import FastAPI
import uvicorn
import asyncio
from telethon import TelegramClient, events
import os
import re
from datetime import datetime
from contextlib import asynccontextmanager

# Load config from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']
channel_to_monitor = os.environ['CHANNEL_NAME']

# Solana address pattern
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Telegram client
client = TelegramClient('session', api_id, api_hash)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.start(bot_token=bot_token)
    print("✅ Bot Started")
    yield
    await client.disconnect()

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"status": "Bot is running"}

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for address in addresses:
            message = f"""👾 *New Contract Detected!*

🪙 *Coin:* `Unknown`
🔗 *Address:* `{address}`

📅 *Time:* `{timestamp}`

💬 _CA successfully scraped✅ from monitored channel📣._
🚀 *Get in early or stay informed!*⚡
"""
            await client.send_message(receiver, message, parse_mode='markdown')
