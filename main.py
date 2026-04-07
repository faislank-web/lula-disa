import asyncio
import os
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- DATA AKSES (TETAP SAMA) ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
RAW_SESSION = '1BVtsOHcBuyDqGsgYZELUzOQooVO0K-D7QxPJi4aZ2zq5C3M9UDojZKrez2U3yfOXv9J5A0D8_XAUUo5MSkucszYEJoXuEK4NRo_Mir4FxuxQAe4DY8X5-cNv9E0z-yy-g9_9IR30VBBChBDx566GGkrbEjykycfYyL7jaLvUn0T1yLYoYHrXDxNFPj0luzzIdzVUk-49Nm8s3bfhAy7KpTE6maAW5gT18drf8HKgNvPsBaHpBw0To8cYJHUjM9nPvUAvMN30NER2FYtfiaAZ7IuMa3VDu2fnwRJjf5EGC_MWpnzvVlj2HBfoOc9A6lkEW23LimJ16Ve8Kq3eRtumhiq1WhEkoI8='

SUMBER = -1002186281759
TUJUAN = -1003473467525
REPLY_KE = 5318

client = TelegramClient(StringSession(RAW_SESSION.strip()), API_ID, API_HASH, sequential_updates=True)

# --- FUNGSI PEMBERSIHAN KHUSUS BUNDA ---
def proses_caption_dhisa(teks):
    if not teks: return ""
    
    # 1. Hapus Markdown (Simbol *, _, `, ~, [])
    teks = re.sub(r'[*_`~\[\]]', '', teks)
    
    # 2. Hapus semua link/tautan (http, t.me, @username)
    teks = re.sub(r'https?://\S+', '', teks)
    teks = re.sub(r't\.me/\S+', '', teks)
    teks = re.sub(r'@\S+', '', teks)

    # 3. Pergantian Kata Sesuai List Bunda
    kamus = {
        "New TV Show Added!": "Series Update",
        "New Movie Added!": "Movie Update",
        "New Episode Released": "Episode Baru Tersedia",
        "Download Via": "silakan Request ke Bunda si-Cantik"
    }
    
    for lama, baru in kamus.items():
        # Menggunakan re.IGNORECASE agar kalau huruf besar/kecil beda tetap kena ganti
        teks = re.sub(re.escape(lama), baru, teks, flags=re.IGNORECASE)

    # 4. Tambahkan Footer (2 baris kosong + Footer)
    footer = "\n\n\nby Dhisa si-Cantik @nontonbarengFM"
    teks = teks.strip() + footer
    
    return teks

async def main():
    print("--- [ DHISA FORWARDER: REWRITE MODE ] --- 🎀")
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("❌ SESSION TIDAK VALID!")
            return
        
        # Tombol Channel Utama
        markup = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]

        last_id = 0
        if os.path.exists("last_id.txt"):
            with open("last_id.txt", "r") as f:
                content = f.read().strip()
                if content: last_id = int(content)

        async for msg in client.iter_messages(SUMBER, min_id=last_id, limit=None, reverse=True):
            if msg.action: continue
            
            try:
                # Olah teks caption
                caption_baru = proses_caption_dhisa(msg.text) if msg.text else ""
                
                # Kirim ulang ke Topik dengan Reply ID & Tombol
                await client.send_message(
                    TUJUAN, 
                    msg, 
                    message=caption_baru, 
                    reply_to=REPLY_KE, 
                    buttons=markup
                )
                
                # Simpan progres
                last_id = msg.id
                with open("last_id.txt", "w") as f:
                    f.write(str(last_id))
                
                print(f"✅ Berhasil Re-write ID: {msg.id}")
                await asyncio.sleep(2.5) # Jeda lebih lama agar tidak kena limit

            except Exception as e:
                print(f"⚠️ Error di ID {msg.id}: {e}")
                if "Wait" in str(e): await asyncio.sleep(60)

        print("🏁 PROSES SELESAI, BUNDA! 🌸")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == '__main__':
    asyncio.run(main())
