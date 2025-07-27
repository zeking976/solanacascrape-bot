import os
import re
from telethon import TelegramClient, events

# Get from environment
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
receiver = os.environ.get("RECEIVER")
channel_to_monitor = os.environ.get("CHANNEL")

solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Create bot client directly using bot_token
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        msg = "\n".join(f"Detected Solana Address:\n{addr}" for addr in addresses)
        print(f"Forwarding: {msg}")
        await client.send_message(receiver, msg)

print("Bot is running and listening...")
client.run_until_disconnected()
