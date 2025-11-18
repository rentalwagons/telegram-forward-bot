from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS_RAW = os.getenv("CHANNELS", "")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ---- Parse CHANNELS ----
# Format:
# -1001234:2,-1005555:10,-1009999
# meaning:
# chat_id:thread_id OR just chat_id
def parse_channels(raw: str):
    result = []
    parts = raw.split(",")
    for p in parts:
        p = p.strip()
        if not p:
            continue

        if ":" in p:
            chat_id, thread_id = p.split(":")
            result.append((int(chat_id), int(thread_id)))
        else:
            result.append((int(p), None))

    return result


CHANNELS = parse_channels(CHANNELS_RAW)


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    if "message" in data:
        text = data["message"].get("text", "")

        # Send to all destinations
        for chat_id, thread_id in CHANNELS:
            payload = {
                "chat_id": chat_id,
                "text": text
            }

            # add thread ID if exists
            if thread_id is not None:
                payload["message_thread_id"] = thread_id

            requests.post(
                f"{TELEGRAM_API_URL}/sendMessage",
                json=payload
            )

    return {"ok": True}
