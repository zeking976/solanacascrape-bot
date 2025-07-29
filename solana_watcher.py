from fastapi import FastAPI
from telethon import TelegramClient, events
import os
import re
import httpx
from datetime import datetime
import asyncio

# Load environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
channel_to_monitor = os.getenv("CHANNEL_NAME")
receiver = os.getenv("RECEIVER")

# Regex to detect Solana wallet/CA (32–44 char base58)
solana_pattern = r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b"

# FastAPI app for Render
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Baby Bot is running."}

# Initialize Telethon client properly
client = TelegramClient("session", api_id, api_hash).start(bot_token=bot_token)

# Dexscreener fetch
async def get_dex_data(ca):
    url = f"https://api.dexscreener.com/latest/dex/search/?q={ca}"
    async with httpx.AsyncClient() as session:
        try:
            r = await session.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data["pairs"]:
                    pair = data["pairs"][0]
                    name = pair.get("baseToken", {}).get("name", "Unknown")
                    mc = pair.get("fdv", 0)
                    return name, f"${mc:,.0f}"
        except Exception:
            pass
    return "Unknown", "N/A"

# Main handler
@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    msg = event.message.message
    addresses = re.findall(solana_pattern, msg)
    if addresses:
        for ca in addresses:
            token_name, market_cap = await get_dex_data(ca)
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            response = f"""🚀 *New Contract Detected!*

🔹 *Token:* `{token_name}`
📬 *Contract:* `{ca}`
💹 *Market Cap:* `{market_cap}`
⏰ *Time:* {timestamp}

Tap to copy contract easily and check early on [Dexscreener](https://dexscreener.com/solana/{ca})
"""
            await client.send_message(receiver, response, parse_mode="markdown")

# Start Telegram client with FastAPI
@app.on_event("startup")
async def startup():
    asyncio.create_task(client.run_until_disconnected())
