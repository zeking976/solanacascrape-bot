import os
import asyncio
from datetime import datetime
from fastapi import FastAPI
from telethon import TelegramClient, events
import httpx

# Load environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
channel_to_monitor = os.getenv("CHANNEL_NAME")
receiver = os.getenv("RECEIVER")

# FastAPI app
app = FastAPI()

# Initialize Telegram client (don't use await here)
client = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)


@app.on_event("startup")
async def startup_event():
    print("Bot is starting...")
    asyncio.create_task(run_bot())


async def get_market_data(ca):
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{ca}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            data = resp.json()
            if "pair" in data:
                token = data["pair"].get("baseToken", {}).get("name", "Unknown")
                market_cap = data["pair"].get("fdv", "N/A")
                return token, market_cap
    except Exception as e:
        print("Dexscreener fetch error:", e)
    return "Unknown", "N/A"


async def run_bot():
    @client.on(events.NewMessage(chats=channel_to_monitor))
    async def handler(event):
        text = event.raw_text.strip()
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        token, cap = await get_market_data(text)

        msg = f"""📡 *New Contract Detected!*

🔗 *Address:* `{text}`
🏷️ *Token:* {token}
💰 *Market Cap:* ${cap:,}
⏱️ *Timestamp:* `{timestamp}`

🧠 *Scraped from monitored channel!*
🚀 *Move early, stay sharp!*
"""
        await client.send_message(receiver, msg, parse_mode="markdown")

    await client.run_until_disconnected()
