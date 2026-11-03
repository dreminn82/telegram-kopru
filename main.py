import os
import asyncio
from aiohttp import web
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = 33922924
API_HASH = "aaa4b88ff0a38c066cf8704e15d45010"
SESSION_STRING = "1BJWap1sBu8IJbcFYHEaohiz12HMjfO0xFXirxD5KPtFWxN3gwTRdkd1FRzIJKXg_sdXfkImZ9lNuBteODm6p9QkuDRbWw9qCVYXJcbW9KTuGqJ17rhKFtqT4QRfzKEhMKsvl8wvolcEme3j2sKkpGKp9KvVlg3uoZTOUlnUJ3okfQRUrdgciO9T-yIHhDjRUcB7IHPhEZo3oNnKnZoM7aMwRM5lLQycYBJZcIm08USygCtdULsAAcbd2MiWV-ksRue9LSTxQnVoIeonx64SpLaQetlMw4NBpXT0-Uxrn0Jd05SzOwpl8qWBEs9MhjLnNUj4E_okX3-zvwt2NyboGPqwW7P0r0AU="

SOURCE_CHAT_ID = -1003911500098
TARGET_CHAT_ID = -1003588984767

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def forward_handler(event):
    try:
        if event.message.text:
            await client.send_message(TARGET_CHAT_ID, event.message.text)
        elif event.message.media:
            await client.send_file(TARGET_CHAT_ID, event.message.media, caption=event.message.text)
        print("Sinyal aktarildi!")
    except Exception as e:
        print(f"Hata: {e}")

async def handle_ping(request):
    return web.Response(text="Kopru Aktif!")

async def main():
    # 1. Once Web sunucusunu baslat (Render hemen portu yakalasin)
    port = int(os.environ.get("PORT", 10000))
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web sunucusu {port} portunda devrede...")

    # 2. Ardindan Telegram istemcisini baslat
    await client.start()
    print("Telegram dinleyici devrede...")
    
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
