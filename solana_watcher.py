from telethon import TelegramClient, events
import re

# === USER CONFIG ===
import os

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
receiver = os.environ.get("RECEIVER")
channel_to_monitor = os.environ.get("CHANNEL")  # Channel name (no @)

# === Solana address pattern (Base58, 32–44 characters) ===
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# === Create main client session ===
client = TelegramClient('main_session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)

    if addresses:
        msg = "\n".join(f"🔍 Detected Solana Address:\n{addr}" for addr in addresses)
        print(f"Forwarding:\n{msg}")

        # Start a bot client to send message
        from telethon.sync import TelegramClient as BotClient
        bot = BotClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
        await bot.send_message(receiver, msg)
        await bot.disconnect()

# Start listening
client.start()
print("🔄 Listening for Solana addresses...")
client.run_until_disconnected()
