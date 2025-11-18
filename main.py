import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("CHANNELS").split(",")

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

@dp.message()
async def forward_message(message: types.Message):
    for channel_id in CHANNELS:
        if message.text:
            await bot.send_message(channel_id, message.text)
        elif message.photo:
            await bot.send_photo(channel_id, message.photo[-1].file_id, caption=message.caption)
        elif message.video:
            await bot.send_video(channel_id, message.video.file_id, caption=message.caption)
        elif message.document:
            await bot.send_document(channel_id, message.document.file_id, caption=message.caption)
    await message.answer("✔️ Forwarded.")

async def start():
    app = web.Application()
    SimpleRequestHandler(dp, bot).register(app, path="/webhook")
    setup_application(app, dp)
    return app

app = asyncio.run(start())
