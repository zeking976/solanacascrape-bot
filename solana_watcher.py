from telethon import TelegramClient, events
import os
import re

# Load config from environment
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']  # e.g., @yourusername or user_id
channel_to_monitor = os.environ['CHANNEL_NAME']  # without @

# Solana address pattern
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        msg = "\n".join(f"Detected Solana Address:\n{addr}" for addr in addresses)
        print(f"Forwarding: {msg}")

        from telethon.sync import TelegramClient as BotClient
        bot = BotClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
        await bot.send_message(receiver, msg)
        await bot.disconnect()

client.start()
print("✅ Listening for Solana addresses...")
client.run_until_disconnected()
