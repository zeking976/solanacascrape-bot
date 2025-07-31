import os
import re
import httpx
import asyncio
import base64
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from current directory
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Decode session file from base64 if not present
if not Path("user.session").exists():
    b64data = os.getenv("SESSION_B64")
    if b64data:
        with open("user.session", "wb") as f:
            f.write(base64.b64decode(b64data))

# Load credentials
api_id = int(os.getenv("API_ID") or 0)
api_hash = os.getenv("API_HASH")
channel = os.getenv("CHANNEL_USERNAME")
receiver = int(os.getenv("RECEIVER") or 0)

# Initialize Telegram client session
client = TelegramClient("user", api_id, api_hash)

# Extract contract address and market cap from text
def extract_token_data(text):
    ca_pattern = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
    mc_pattern = re.compile(r'(?:MC|Market Cap)[\s:–-]*\$?([0-9,.]+[KMB]?)', re.IGNORECASE)

    contract = ca_pattern.findall(text)
    market_cap = mc_pattern.search(text)
    return contract[0] if contract else None, market_cap.group(1) if market_cap else "N/A"

# Get live market data from dexscreener
async def get_market_data(ca):
    try:
        url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{ca}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            data = resp.json()
            if "pair" in data:
                token = data["pair"]["baseToken"]["name"]
                mcap = data["pair"].get("fdv", "N/A")
                return token, mcap
    except Exception as e:
        print("Error fetching market data:", e)
    return "Unknown", "N/A"

# Event handler for new messages in the channel
@client.on(events.NewMessage(chats=channel))
async def handle_new_message(event):
    text = event.raw_text
    print("Scraped:", text)
    contract, mcap_text = extract_token_data(text)
    if not contract:
        return

    token, mcap_api = await get_market_data(contract)
    market_cap_display = mcap_api if mcap_api != "N/A" else mcap_text
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    msg = f"""👾 *New Contract Detected!*

🔗 *Contract Address:* `{contract}`
⚡ *Token:* {token}
💰 *Market Cap:* ${market_cap_display}
⏱️ *Timestamp:* `{timestamp}`

📣 *From:* `{channel}`"""

    await client.send_message(receiver, msg, parse_mode="markdown")

# Run the bot
async def main():
    await client.start()
    print("Bot started. Listening for new messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
