import os
import asyncio
from aiohttp import web
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = 33922924
API_HASH = "aaa4b88ff0a38c066cf8704e15d45010"
SESSION_STRING = "1BJWap1sBu4lzyv94gjf7SE8bR6j9M6bJE_sRZJwAJ7rfJgbt34u_4Zw90lTx8PG4M9a7_dcwuYlKuqjdvuY7jA6MhjOAbl8MdjH2JpMDhEbref5wbII3DBGt91OYAP-nv1WbJGckUXV1o4xXlJyz_QiPnQIgmVhMLeq08KKlAS5DwbN0eS-82m8MIChYj5uovv6lRH58WnWvW5q5EB0gOQucWiLiM5TaTJ3FC-ChUy-WN4xRMCgJq13sigPIVAY9Cg8SCCHlo0UYVr3w3bE4EYlDYgXMQwKvZOnhIJWP8Rj3wLFIqK_GBHl9TYwxZywf6OBI0UmQHgqokKW2K6a9GCqdV9RmDpA="

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

if _name_ == "_main_":
    asyncio.run(main())
