import os
import re
import httpx
import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
channel = os.environ["CHANNEL_NAME"]  # e.g., @SolanaAlpha
receiver = int(os.environ["RECEIVER"])  # Your personal Telegram user ID
# Initialize client session using your personal account
client = TelegramClient("user", API_ID, API_HASH)

def extract_token_data(text):
    ca_pattern = re.compile(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b')
    mc_pattern = re.compile(r'(?:MC|Market Cap)[\s:–-]*\$?([0-9,.]+[KMB]?)', re.IGNORECASE)

    contract = ca_pattern.findall(text)
    market_cap = mc_pattern.search(text)
    return contract[0] if contract else None, market_cap.group(1) if market_cap else "N/A"

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

🔗 *Address:* `{contract}`
⚡ *Token:* {token}
💰 *Market Cap:* ${market_cap_display}
⏱️ *Timestamp:* `{timestamp}`

📣 *Source:* {channel}"""

    await client.send_message(receiver, msg, parse_mode="markdown")

async def main():
    await client.start()
    print("Bot started. Listening for new messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
