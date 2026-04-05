import re
import asyncio
import os
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- [ DATA AKSES ] ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
STRING_SESSION = '1BVtsOIsBuxwXjk8GUAeZ6uHiMvcQLTsU7aKZkrx7ym8VOzZSyxGYexEhmtZ6Ucu7XjfYDR4eeRpRLwCxKFH4R4eRiHJPf9cuHFXSEDojc1F5AkFDSI634kN3q50fLjWvx1VXzL5KhgKC5qcFljyz214OiHsGuVGt2UusD29xBIc_8MI9RYxbB1bA0Vvf_3dmKAZqE9lopPBk0rw3GOqcOwzERhF8Aq9Y4jW_aUDPGPFHJXa7CscLHdsdidJHRR_CkT-SYsM3yOKNCYQjHwxSAPkpv7hf-KgCnk2v07-pkbGyg6zoFkUtsnqaj3iYgamp61s3fFRuaK941tORQa59ZAejtq5U6fU='
FINAL_SESSION = STRING_SESSION.strip().replace(" ", "").replace("\n", "").replace("\r", "")

SOURCE_CHANNEL = -1002186281759
DEST_GROUP = -1003473467525
TOPIC_ID = 5318 

client = TelegramClient(StringSession(FINAL_SESSION), API_ID, API_HASH)

async def send_to_dest(msg):
    try:
        text = msg.message or ""
        # Logika Pembersihan (Persis skrip Disa)
        text = text.replace("New TV Show Added!", "Series Update Tersedia") \
                   .replace("New Movie Added!", "Movie Update Tersedia") \
                   .replace("New Episode Released!", "Episode Baru Tersedia")
        text = re.sub(r'(https?://\S+|www\.\S+)', '', text)
        
        if "Download Via:" in text or "Watch Via:" in text:
            text = text.replace("Download Via:", "Silakan Request ke Bunda si-Cantik") \
                       .replace("Watch Via:", "Silakan Request ke Bunda si-Cantik")
        else: 
            text += "\nSilakan Request ke Bunda si-Cantik"
        
        text += "\n\n                                by Disa @nontonbarengFM"
        buttons = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]

        if msg.photo:
            path = await msg.download_media()
            await client.send_file(DEST_GROUP, path, caption=text, parse_mode="HTML", reply_to=TOPIC_ID, buttons=buttons)
            if os.path.exists(path): os.remove(path)
        elif text.strip():
            await client.send_message(DEST_GROUP, text, parse_mode="HTML", reply_to=TOPIC_ID, buttons=buttons)
        print(f"✅ Berhasil: {text[:20]}...")
    except Exception as e:
        print(f"❌ Gagal: {e}")

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler_baru(event):
    await send_to_dest(event.message)

async def main():
    print("🚀 Memulai Forwarder...")
    await client.start()
    print(f"🔍 Menarik History dari awal di {SOURCE_CHANNEL}...")
    
    # limit=None menarik semua dari awal, reverse=True agar urutan dari lama ke baru
    async for msg in client.iter_messages(SOURCE_CHANNEL, limit=None, reverse=True):
        await send_to_dest(msg)
        await asyncio.sleep(1.8) # Jeda aman agar tidak kena limit
            
    print("✅ History selesai. Menunggu pesan baru...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
