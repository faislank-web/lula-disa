import asyncio
import os
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- DATA DARI GITHUB SECRETS ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
RAW_SESSION = os.environ.get("SESSION_STRING")

SUMBER = -1002186281759
TUJUAN = -1003473467525
REPLY_KE = 5318 

client = TelegramClient(StringSession(RAW_SESSION.strip()), API_ID, API_HASH, sequential_updates=True)

def proses_teks_dhisa(teks):
    if not teks: return ""
    teks = re.sub(r'[*_`~\[\]]', '', teks)
    teks = re.sub(r'https?://\S+', '', teks)
    teks = re.sub(r't\.me/\S+', '', teks)
    teks = re.sub(r'@\S+', '', teks)
    kamus = {
        "New TV Show Added!": "Series Update",
        "New Movie Added!": "Movie Update",
        "New Episode Released": "Episode Baru Tersedia",
        "Download Via": "silakan Request ke Bunda"
    }
    for lama, baru in kamus.items():
        teks = re.sub(re.escape(lama), baru, teks, flags=re.IGNORECASE)
    return teks.strip() + "\n\n\nby Dhisa @nontonbarengFM"

async def main():
    print("--- DHISA: SIMPLE TOPIC BUTTON MODE --- 🎀")
    try:
        await client.connect()
        if not await client.is_user_authorized(): return
        
        # DEFINISI TOMBOL
        markup = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]
        
        last_id = 0
        if os.path.exists("last_id.txt"):
            with open("last_id.txt", "r") as f:
                c = f.read().strip()
                if c: last_id = int(c)

        async for msg in client.iter_messages(SUMBER, min_id=last_id, limit=None, reverse=True):
            if msg.action or not msg.media:
                if msg.id > last_id:
                    last_id = msg.id
                    with open("last_id.txt", "w") as f: f.write(str(last_id))
                continue
            
            try:
                caption_baru = proses_teks_dhisa(msg.text) if msg.text else "Update Film Baru 🎬"
                
                # --- CARA PALING STANDAR & AMAN ---
                await client.send_message(
                    TUJUAN, 
                    caption_baru, 
                    file=msg.media, 
                    reply_to=REPLY_KE, # Langsung tunjuk ID Topiknya
                    buttons=markup
                )
                
                last_id = msg.id
                with open("last_id.txt", "w") as f: f.write(str(last_id))
                print(f"✅ Berhasil Kirim ID: {msg.id}")
                await asyncio.sleep(4) 
            except Exception as e:
                print(f"⚠️ Gagal di ID {msg.id}: {e}")
                
    except Exception as e: print(f"❌ Error: {e}")

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
