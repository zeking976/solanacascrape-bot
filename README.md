# 🔎 Solana Contract Address Watcher Bot

A FastAPI + Telethon-powered Telegram bot that monitors a specific Telegram channel for **Solana Contract Addresses (CAs)** and forwards them to you in a stylized message.

## ⚙️ Features

- Detects **Solana CAs** (base58 format: 32–44 characters)
- Extracts **coin name** from message (`Name:`, `Coin:`, or `Token:`)
- Sends the address to your Telegram with:
  - ✅ Stylized markdown message
  - 📎 Tap-to-copy contract address
  - ⏰ UTC timestamp
- Built with `FastAPI` for free hosting on [Render.com](https://render.com)

---

## 🚀 Live Demo

Once deployed, your bot will be **available at**:

https://<your-service-name>.onrender.com

Example response from your endpoint:
```json
{ "status": "Bot is running" }


---

📦 Requirements

Create a requirements.txt file like this:

telethon
fastapi
uvicorn


---

🌍 Environment Variables

Set these in Render → Environment Settings or in your .env:

Variable	Description

API_ID	Your Telegram API ID
API_HASH	Your Telegram API hash
BOT_TOKEN	Your Telegram bot token from BotFather
CHANNEL_NAME	Channel username or ID to monitor
RECEIVER	Your own Telegram username or ID


> 💡 Use your Telegram numeric ID for RECEIVER if username doesn't work.




---

🧠 How It Works

1. FastAPI binds the app to a port (required for Render free hosting)


2. Telegram bot listens to messages from a target channel


3. When a contract address is detected:

Coin name is extracted (if available)

Stylized message is sent to your account





---

✅ Sample Output

👾 New Contract Detected!

🪙 Coin Name: `PEPE`
🔗 Address: `6R2c6...N8dE5tXz`
🕒 Time: 2025-07-28 15:00 UTC

💬 CA successfully scraped ✅ from monitored channel 📣.
🚀 Get in early or stay informed! ⚡


---

🧪 Local Test (Optional)

uvicorn solana_watcher:app --host 0.0.0.0 --port 8000


---

💰 Free Hosting on Render (Web Service)

Choose Web Service, not Background Worker

Use build command:

pip install -r requirements.txt

Use start command:

python solana_watcher.py



---

📜 License

MIT License — use freely, but give credit if you fork or remix.


---

🧑‍💻 Author

Created by @zeking976

---

Let me know if you'd like me to:
- Upload this `README.md` directly to your repo
- Add badges (e.g. Python version, Render live status)
- Create a deploy button for Render or Railway
