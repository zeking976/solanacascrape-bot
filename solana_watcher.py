import os
import asyncio
from datetime import datetime
from fastapi import FastAPI
from telethon import TelegramClient, events
import httpx
import re

# Load environment variables
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
channel_to_monitor = os.getenv("CHANNEL_NAME")
receiver = os.getenv("RECEIVER")

# FastAPI app
app = FastAPI()

# Initialize Telegram client
client = TelegramClient("bot_session", api_id, api_hash)

@app.on_event("startup")
async def startup_event():
    print("Bot is starting...")
    await client.start(bot_token=bot_token)
    asyncio.create_task(run_bot())


def extract_token_data(message_text: str):
    # Solana contract address regex (Base58, 32–44 chars)
    ca_pattern = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')

    # Market cap pattern, with optional $ and suffixes
    mc_pattern = re.compile(r'(?:MC|Market Cap)[\s:–-]*\$?([0-9,.]+[KMB]?)', re.IGNORECASE)

    contract_matches = ca_pattern.findall(message_text)
    contract_address = contract_matches[0] if contract_matches else None

    mc_match = mc_pattern.search(message_text)
    market_cap = mc_match.group(1) if mc_match else "N/A"

    return contract_address, market_cap


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

        contract_address, market_cap_text = extract_token_data(text)

        if not contract_address:
            print("No contract address found in message.")
            return

        token_name, cap_from_api = await get_market_data(contract_address)

        market_cap_display = cap_from_api if cap_from_api != "N/A" else market_cap_text

        msg = f"""👾 *New Contract Detected!*

🔗 *Address:* `{contract_address}`
🏷️ *Token:* {token_name}
💰 *Market Cap:* ${market_cap_display}
⏱️ *Timestamp:* `{timestamp}`

⚡ *Scraped from SOL Alpha Channel!*
🚀 *Move early, stay sharp!*"""

        await client.send_message(receiver, msg, parse_mode="markdown")

    await client.run_until_disconnected()
