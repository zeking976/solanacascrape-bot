from telethon import TelegramClient, events
import os
import re
import asyncio
import socket

# Read config directly from environment variables
api_id = int(os.environ['API_ID'])
api_hash = os.environ['API_HASH']
bot_token = os.environ['BOT_TOKEN']
receiver = os.environ['RECEIVER']
channel_to_monitor = os.environ['CHANNEL_NAME']

# Solana address pattern (base58: 32–44 chars)
solana_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

# Create main Telegram client session
client = TelegramClient('session', api_id, api_hash)

@client.on(events.NewMessage(chats=channel_to_monitor))
async def handler(event):
    text = event.message.message
    addresses = re.findall(solana_pattern, text)
    if addresses:
        msg = "\n".join(f"🔍 Detected Solana Address:\n{addr}" for addr in addresses)
        print(f"Forwarding:\n{msg}")

        from telethon.sync import TelegramClient as BotClient
        bot = BotClient('bot_session', api_id, api_hash).start(bot_token=bot_token)
        await bot.send_message(receiver, msg)
        await bot.disconnect()

# Trick Render Web Service into staying alive by binding a port
async def hold_port_open():
    port = int(os.environ.get("PORT", 10000))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", port))
    s.listen(1)
    while True:
        await asyncio.sleep(3600)

# Start everything
loop = asyncio.get_event_loop()
loop.create_task(hold_port_open())
client.start()
print("✅ Bot is running and watching for Solana contract addresses...")
client.run_until_disconnected()
