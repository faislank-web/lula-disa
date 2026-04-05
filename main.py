import re
import asyncio
import os
import sys
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- [ KONFIGURASI DATA AKSES ] ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
# Pakai String Session BARU yang barusan Kakak buat (Fresh!)
RAW_SESSION = '1BVtsOHcBuyDqGsgYZELUzOQooVO0K-D7QxPJi4aZ2zq5C3M9UDojZKrez2U3yfOXv9J5A0D8_XAUUo5MSkucszYEJoXuEK4NRo_Mir4FxuxQAe4DY8X5-cNv9E0z-yy-g9_9IR30VBBChBDx566GGkrbEjykycfYyL7jaLvUn0T1yLYoYHrXDxNFPj0luzzIdzVUk-49Nm8s3bfhAy7KpTE6maAW5gT18drf8HKgNvPsBaHpBw0To8cYJHUjM9nPvUAvMN30NER2FYtfiaAZ7IuMa3VDu2fnwRJjf5EGC_MWpnzvVlj2HBfoOc9A6lkEW23LimJ16Ve8Kq3eRtumhiq1WhEkoI8='

# Pembersihan otomatis karakter spasi/enter di session
FINAL_SESSION = "".join(RAW_SESSION.split())

# --- [ KONFIGURASI GRUP & CHANNEL ] ---
SOURCE_CHANNEL = -1002186281759
DEST_GROUP = -1003473467525
TOPIC_ID = 5318 

client = TelegramClient(StringSession(FINAL_SESSION), API_ID, API_HASH)

async def send_to_dest(msg):
    """Fungsi untuk memproses teks, foto, footer, dan tombol inline."""
    try:
        text = msg.message or ""
        
        # 1. Logika Pembersihan & Penggantian Kata (Persis Skrip Disa)
        text = text.replace("New TV Show Added!", "Series Update Tersedia") \
                   .replace("New Movie Added!", "Movie Update Tersedia") \
                   .replace("New Episode Released!", "Episode Baru Tersedia")
        
        # Hapus Link (re-sub)
        text = re.sub(r'(https?://\S+|www\.\S+)', '', text)
        
        # Logika Request Bunda si-Cantik
        if "Download Via:" in text or "Watch Via:" in text:
            text = text.replace("Download Via:", "Silakan Request ke Bunda si-Cantik") \
                       .replace("Watch Via:", "Silakan Request ke Bunda si-Cantik")
        else: 
            text += "\nSilakan Request ke Bunda si-Cantik"
        
        # Footer Identitas Disa (Spasi panjang di awal)
        text += "\n\n                                by Disa @nontonbarengFM"
        
        # 2. Tombol Inline Channel Utama
        buttons = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]

        # 3. Eksekusi Pengiriman ke Topik
        if msg.photo:
            path = await msg.download_media()
            await client.send_file(
                DEST_GROUP, 
                path, 
                caption=text, 
                parse_mode="HTML", 
                reply_to=TOPIC_ID,
                buttons=buttons
            )
            if os.path.exists(path): os.remove(path)
        elif text.strip():
            await client.send_message(
                DEST_GROUP, 
                text, 
                parse_mode="HTML", 
                reply_to=TOPIC_ID,
                buttons=buttons
            )
        
        print(f"✅ Berhasil Kirim: {text[:30]}...")
        return True
    except Exception as e:
        print(f"❌ Gagal kirim pesan: {e}")
        return False

# --- HANDLER POSTINGAN BARU ---
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler_baru(event):
    await send_to_dest(event.message)

async def main():
    print("\n--- 🔨 PALU BASA FORWARDER SYSTEM STARTING ---")
    try:
        await client.start()
        me = await client.get_me()
        print(f"🤖 Login Berhasil sebagai: {me.first_name} (@{me.username})")
    except Exception as e:
        print(f"❌ LOGIN GAGAL: {e}\nSilakan cek String Session Kakak!")
        return

    print(f"🔍 Mencari History di Channel: {SOURCE_CHANNEL}")
    
    count = 0
    # iter_messages(limit=None) menarik SEMUA pesan dari awal (reverse=True)
    async for msg in client.iter_messages(SOURCE_CHANNEL, limit=None, reverse=True):
        success = await send_to_dest(msg)
        if success:
            count += 1
            # Jeda agar aman dari FloodWait/Limit Telegram
            await asyncio.sleep(2)
        
        # Log Progress setiap 10 pesan
        if count % 10 == 0:
            print(f"🕒 Progress: {count} pesan history terproses...")

    print(f"🏁 History Selesai! Total {count} pesan terkirim ke Topik {TOPIC_ID}.")
    print("📡 Mode Standby Aktif... Menunggu postingan baru dari sumber.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Menggunakan event loop yang stabil untuk server GitHub Actions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
