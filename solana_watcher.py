import os
from telethon import TelegramClient, events
from keep_alive import keep_alive
import re

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
receiver = os.getenv("RECEIVER")
channel_to_monitor = os.getenv("CHANNEL")

solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

client = TelegramClient('main_session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        msg = "\n".join(f"Detected Solana Address:\n{addr}" for addr in addresses)
        from telethon.sync import TelegramClient as BotClient
        bot = BotClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
        await bot.send_message(receiver, msg)
        await bot.disconnect()

keep_alive()  # Keeps Replit awake
client.start()
print("Listening for Solana addresses...")
client.run_until_disconnected()
