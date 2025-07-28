# 🛰️ Solana Contract Address Scraper Bot

This is a Telegram bot that listens to a specific Telegram channel and instantly extracts any **Solana contract addresses** (base58 format), then forwards them to your Telegram account or group.

## 🚀 Features

- 🔍 Detects Solana contract addresses (32–44 char base58)
- 🤖 Forwards them automatically using a bot token
- 🌐 Runs 24/7 on Render as a Python web service

---

## 🧠 How It Works

1. The bot uses `telethon` to listen to messages in a given Telegram channel.
2. It searches for any string that matches a Solana address pattern.
3. If found, it sends that address to your personal Telegram account or group.

---

## 📦 Requirements

- Python 3.9+
- Render (or Termux/local)
- Telegram API credentials:
  - `API_ID`
  - `API_HASH`
  - `BOT_TOKEN`
  - `RECEIVER` (your `@username` or chat ID)
  - `CHANNEL_NAME` (username of the channel to watch)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/zeking976/solanacascrape-bot.git
cd solanacascrape-bot

2. Install Requirements

pip install -r requirements.txt


---

🖥️ Deployment on Render

1. Create a New Web Service

Go to Render.com, connect your GitHub repo, and create a new Web Service.

2. Set Build and Start Commands

Build Command: pip install -r requirements.txt

Start Command: python solana_watcher.py


3. Add Environment Variables

In the Render dashboard:

Variable	Example

API_ID	1234567
API_HASH	abcdef1234567890abcdef
BOT_TOKEN	123456:ABC-xyz...
RECEIVER	@yourusername
CHANNEL_NAME	cryptodropschannel



---

📝 File Structure

solanacascrape-bot/
├── solana_watcher.py
├── requirements.txt
├── render.yaml
└── README.md


---

🤝 Credits

Created by @zeking976


---

📃 License

MIT License — use it however you like.

---
