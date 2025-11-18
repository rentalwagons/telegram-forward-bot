from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("CHANNELS", "").split(",")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    if "message" in data:
        text = data["message"].get("text", "")
        
        # Forward to all channels
        for channel in CHANNELS:
            if channel:
                requests.post(
                    f"{TELEGRAM_API_URL}/sendMessage",
                    json={"chat_id": int(channel), "text": text}
                )

    return {"ok": True}
