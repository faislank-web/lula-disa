import asyncio
import os
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- DATA AKSES BUNDA (PROTECTED) ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
RAW_SESSION = '1BVtsOHcBuyDqGsgYZELUzOQooVO0K-D7QxPJi4aZ2zq5C3M9UDojZKrez2U3yfOXv9J5A0D8_XAUUo5MSkucszYEJoXuEK4NRo_Mir4FxuxQAe4DY8X5-cNv9E0z-yy-g9_9IR30VBBChBDx566GGkrbEjykycfYyL7jaLvUn0T1yLYoYHrXDxNFPj0luzzIdzVUk-49Nm8s3bfhAy7KpTE6maAW5gT18drf8HKgNvPsBaHpBw0To8cYJHUjM9nPvUAvMN30NER2FYtfiaAZ7IuMa3VDu2fnwRJjf5EGC_MWpnzvVlj2HBfoOc9A6lkEW23LimJ16Ve8Kq3eRtumhiq1WhEkoI8='

SUMBER = -1002186281759
TUJUAN = -1003473467525
REPLY_KE = 5318

client = TelegramClient(StringSession(RAW_SESSION.strip()), API_ID, API_HASH, sequential_updates=True)

def proses_teks_dhisa(teks):
    if not teks: return ""
    
    # 1. Hapus semua Markdown (simbol formatting)
    teks = re.sub(r'[*_`~\[\]]', '', teks)
    
    # 2. Hapus total semua link (http, t.me, @username)
    teks = re.sub(r'https?://\S+', '', teks)
    teks = re.sub(r't\.me/\S+', '', teks)
    teks = re.sub(r'@\S+', '', teks)

    # 3. Pergantian Kata Sesuai List Bunda si-Cantik
    kamus_ganti = {
        "New TV Show Added!": "Series Update",
        "New Movie Added!": "Movie Update",
        "New Episode Released": "Episode Baru Tersedia",
        "Download Via": "silakan Request ke Bunda si-Cantik"
    }
    
    for lama, baru in kamus_ganti.items():
        teks = re.sub(re.escape(lama), baru, teks, flags=re.IGNORECASE)

    # 4. Tambahkan Footer (2 baris kosong + Footer)
    teks = teks.strip() + "\n\n\nby Dhisa si-Cantik @nontonbarengFM"
    
    return teks

async def main():
    print("--- DHISA FORWARDER STARTING --- 🎀")
    try:
        await client.connect()
        if not await client.is_user_authorized():
            print("❌ SESSION TIDAK VALID!")
            return
        
        # Tombol di setiap pesan
        markup = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]

        # Load Progres
        last_id = 0
        if os.path.exists("last_id.txt"):
            with open("last_id.txt", "r") as f:
                content = f.read().strip()
                if content: last_id = int(content)

        print(f"🔍 Mencari pesan baru setelah ID: {last_id}")
        
        async for msg in client.iter_messages(SUMBER, min_id=last_id, limit=None, reverse=True):
            if msg.action: continue
            
            try:
                # Olah teks caption
                caption_baru = proses_teks_dhisa(msg.text) if msg.text else ""
                
                # Kirim ulang (Metode Upload Ulang)
                await client.send_message(
                    TUJUAN, 
                    msg, 
                    message=caption_baru, 
                    reply_to=REPLY_KE, 
                    buttons=markup
                )
                
                # Simpan progres lokal
                last_id = msg.id
                with open("last_id.txt", "w") as f:
                    f.write(str(last_id))
                
                print(f"✅ Sukses Forward ID: {msg.id}")
                await asyncio.sleep(2) # Delay aman

            except Exception as e:
                print(f"⚠️ Skip ID {msg.id} karena: {e}")
                if "Wait" in str(e): await asyncio.sleep(60)

    except Exception as e:
        print(f"❌ SYSTEM ERROR: {e}")

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
