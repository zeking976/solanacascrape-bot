import os
import re
from telethon import TelegramClient, events

# Load environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']
channel_to_monitor = os.environ['CHANNEL_NAME']  # Don't include '@'

# Regex pattern to detect Solana wallet addresses
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Initialize Telegram bot client using bot token (no user login)
client = TelegramClient('session', api_id, api_hash).start(bot_token=bot_token)

# Event listener for new messages in the target channel
@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)

    if addresses:
        msg = "\n".join(f"Detected Solana Address:\n{addr}" for addr in addresses)
        print(f"Forwarding:\n{msg}")
        await client.send_message(receiver, msg)

print("✅ Bot is running and listening for Solana addresses...")
client.run_until_disconnected()
