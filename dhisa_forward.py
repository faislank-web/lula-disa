import asyncio
import os
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- DATA AKSES BUNDA ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
RAW_SESSION = '1BVtsOHcBuyDqGsgYZELUzOQooVO0K-D7QxPJi4aZ2zq5C3M9UDojZKrez2U3yfOXv9J5A0D8_XAUUo5MSkucszYEJoXuEK4NRo_Mir4FxuxQAe4DY8X5-cNv9E0z-yy-g9_9IR30VBBChBDx566GGkrbEjykycfYyL7jaLvUn0T1yLYoYHrXDxNFPj0luzzIdzVUk-49Nm8s3bfhAy7KpTE6maAW5gT18drf8HKgNvPsBaHpBw0To8cYJHUjM9nPvUAvMN30NER2FYtfiaAZ7IuMa3VDu2fnwRJjf5EGC_MWpnzvVlj2HBfoOc9A6lkEW23LimJ16Ve8Kq3eRtumhiq1WhEkoI8='

SUMBER = -1002186281759
TUJUAN = -1003473467525
REPLY_KE = 5318

client = TelegramClient(StringSession(RAW_SESSION.strip()), API_ID, API_HASH, sequential_updates=True)

def proses_teks_dhisa(teks):
    if not teks: return ""
    # 1. Hapus Markdown
    teks = re.sub(r'[*_`~\[\]]', '', teks)
    # 2. Hapus Link & Username
    teks = re.sub(r'https?://\S+', '', teks)
    teks = re.sub(r't\.me/\S+', '', teks)
    teks = re.sub(r'@\S+', '', teks)
    # 3. Ganti Kata Sesuai Request Bunda
    kamus = {
        "New TV Show Added!": "Series Update",
        "New Movie Added!": "Movie Update",
        "New Episode Released": "Episode Baru Tersedia",
        "Download Via": "silakan Request ke Bunda si-Cantik"
    }
    for lama, baru in kamus.items():
        teks = re.sub(re.escape(lama), baru, teks, flags=re.IGNORECASE)
    # 4. Footer
    return teks.strip() + "\n\n\nby Dhisa si-Cantik @nontonbarengFM"

async def main():
    print("--- DHISA FORWARDER: MEDIA ONLY MODE --- 🎀")
    try:
        await client.connect()
        if not await client.is_user_authorized(): return
        
        markup = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]
        last_id = 0
        if os.path.exists("last_id.txt"):
            with open("last_id.txt", "r") as f:
                c = f.read().strip()
                if c: last_id = int(c)

        async for msg in client.iter_messages(SUMBER, min_id=last_id, limit=None, reverse=True):
            if msg.action: continue 
            
            # --- PROTEKSI: HANYA FORWARD YANG ADA MEDIA ---
            if not msg.media:
                print(f"⏩ Skip ID {msg.id}: Bukan Media")
                # Tetap update last_id agar tidak dicek ulang
                last_id = msg.id
                with open("last_id.txt", "w") as f: f.write(str(last_id))
                continue
            
            try:
                caption_baru = proses_teks_dhisa(msg.text) if msg.text else "by Dhisa si-Cantik @nontonbarengFM"
                await client.send_message(TUJUAN, msg, message=caption_baru, reply_to=REPLY_KE, buttons=markup)
                
                last_id = msg.id
                with open("last_id.txt", "w") as f: f.write(str(last_id))
                print(f"✅ Media Forwarded: {msg.id}")
                await asyncio.sleep(2.5) 

            except Exception as e:
                print(f"⚠️ Error ID {msg.id}: {e}")
                if "Wait" in str(e): await asyncio.sleep(60)

    except Exception as e: print(f"❌ Error: {e}")

if __name__ == '__main__':
    with client: client.loop.run_until_complete(main())
