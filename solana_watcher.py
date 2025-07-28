from fastapi import FastAPI
import uvicorn
import asyncio
from telethon import TelegramClient, events
import os
import re

# Load config from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']
channel_to_monitor = os.environ['CHANNEL_NAME']

# Solana address pattern
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Create FastAPI app (required to bind port)
app = FastAPI()

@app.get("/")
def root():
    return {"status": "Bot is running"}

# Telegram client
client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        msg = "\n".join(f"Detected Solana Address:\n{addr}" for addr in addresses)
        print(f"Forwarding: {msg}")
        await client.send_message(receiver, msg)

async def start_bot():
    await client.start(bot_token=bot_token)
    print("✅ Bot Started")
    await client.run_until_disconnected()

# Start both FastAPI and bot together
def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    uvicorn.run(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    main()
