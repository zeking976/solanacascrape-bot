from telethon import TelegramClient, events
import re

# === USER CONFIG ===
api_id = 29195559  # Your API ID
api_hash = '8c79486da7334b88c8d6663e92cc43a2'  # Your API Hash
bot_token = '8273702287:AAGfDgoec3Lt3Za9reM31UIcldEynIGNNf0'  # Bot token from BotFather
receiver = '@alienonlinebtc'  # Your Telegram username (with @)

channel_to_monitor = 'the_defi_investor'  # Channel name (no @)

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
