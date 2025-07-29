# 🔍Solana CA Scraper📃
A Telegram bot that monitors a specific channel for Solana contract addresses and sends alerts with:

- 📍 Detected contract address (easily copyable)
- ⏰ UTC timestamp
- 📈 Current market cap from Dexscreener
- 📬 Forwards it to your own Telegram (or another bot/channel)

---

## 🔧 Environment Variables (set on Render)

| Key           | Description                            |
|---------------|----------------------------------------|
| `API_ID`      | Telegram API ID                        |
| `API_HASH`    | Telegram API Hash                      |
| `BOT_TOKEN`   | Telegram Bot Token                     |
| `RECEIVER`    | Your own Telegram username or ID       |
| `CHANNEL_NAME`| The exact name of the channel to watch |

---

## ▶️ Running Locally

1. Set your environment variables using `.env` or directly in shell.
2. Install dependencies:
```bash
pip install -r requirements.txt

3. Run:



python solana_watcher.py


---

🚀 Deployment on Render

Make sure you have:

Your render.yaml

Your environment variables set in Render dashboard

Files in your repo: solana_watcher.py, requirements.txt, render.yaml, README.md


Then push your repo to Git and connect to Render.

---

## 🛠️ 4. `render.yaml`

```yaml
services:
  - type: web
    name: solana-watcher
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python solana_watcher.py
    autoDeploy: true
    envVars:
      - key: API_ID
        sync: false
      - key: API_HASH
        sync: false
      - key: BOT_TOKEN
        sync: false
      - key: CHANNEL_NAME
        sync: false
      - key: RECEIVER
        sync: false


---
