import re
import asyncio
import os
import sys
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- [ DATA AKSES ] ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
# String Session Kakak (Dibersihkan otomatis oleh skrip di bawah)
RAW_SESSION = '1BVtsOIsBuxwXjk8GUAeZ6uHiMvcQLTsU7aKZkrx7ym8VOzZSyxGYexEhmtZ6Ucu7XjfYDR4eeRpRLwCxKFH4R4eRiHJPf9cuHFXSEDojc1F5AkFDSI634kN3q50fLjWvx1VXzL5KhgKC5qcFljyz214OiHsGuVGt2UusD29xBIc_8MI9RYxbB1bA0Vvf_3dmKAZqE9lopPBk0rw3GOqcOwzERhF8Aq9Y4jW_aUDPGPFHJXa7CscLHdsdidJHRR_CkT-SYsM3yOKNCYQjHwxSAPkpv7hf-KgCnk2v07-pkbGyg6zoFkUtsnqaj3iYgamp61s3fFRuaK941tORQa59ZAejtq5U6fU='

# Membersihkan String Session dari spasi/enter tersembunyi
FINAL_SESSION = "".join(RAW_SESSION.split())

SOURCE_CHANNEL = -1002186281759
DEST_GROUP = -1003473467525
TOPIC_ID = 5318 

client = TelegramClient(StringSession(FINAL_SESSION), API_ID, API_HASH)

async def send_to_dest(msg):
    try:
        text = msg.message or ""
        # Logika Pembersihan Teks
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
        
        print(f"✅ Berhasil Kirim: {text[:30]}...")
        return True
    except Exception as e:
        print(f"❌ Gagal kirim pesan: {e}")
        return False

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler_baru(event):
    await send_to_dest(event.message)

async def main():
    print("--- MEMULAI SISTEM ---")
    try:
        await client.start()
        me = await client.get_me()
        print(f"🤖 Login Berhasil sebagai: {me.first_name}")
    except Exception as e:
        print(f"❌ LOGIN GAGAL: {e}")
        return

    print(f"🔍 Mencari History di: {SOURCE_CHANNEL}")
    
    count = 0
    async for msg in client.iter_messages(SOURCE_CHANNEL, limit=None, reverse=True):
        success = await send_to_dest(msg)
        if success:
            count += 1
            # Jeda agar aman dari limit Telegram
            await asyncio.sleep(2)
        
        # Log setiap 10 pesan agar GitHub tidak mengira skrip mati (Timeout)
        if count % 10 == 0:
            print(f"🕒 Progress: {count} pesan terproses...")

    print(f"🏁 History Selesai! Total {count} pesan dikirim.")
    print("📡 Mode Standby Aktif...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Menggunakan loop yang lebih stabil untuk GitHub Actions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
