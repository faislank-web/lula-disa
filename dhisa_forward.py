import asyncio
import os
import re
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- DATA DARI GITHUB SECRETS ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
RAW_SESSION = os.environ.get("SESSION_STRING")

SUMBER = -1002659601192
TUJUAN_1 = -1003874231232

client = TelegramClient(StringSession(RAW_SESSION.strip()), API_ID, API_HASH, sequential_updates=True)

def proses_teks_custom(teks):
    if not teks: return ""
    
    # Hapus tanda kurung apa pun sebelum judul agar rapi (misal: [DL NIME])
    teks = re.sub(r'^\[[^\]]+\]\s*', '', teks)
    
    # Pembersihan link lama dan karakter markdown mentah agar tidak tabrakan
    teks = re.sub(r'https?://\S+', '', teks)
    teks = re.sub(r't\.me/\S+', '', teks)
    teks = re.sub(r'@\S+', '', teks)
    teks = re.sub(r'[_`~]', '', teks)  # Menyisakan [] untuk keperluan tautan markdown nanti
    
    kamus = {
        "New TV Show Added!": "Series Update",
        "New Movie Added!": "Yakinnn nih gada yg mau???\n\n",
        "New Episode Released": "Episode Baru Tersedia"
    }
    
    for lama, baru in kamus.items():
        teks = re.sub(re.escape(lama), baru, teks, flags=re.IGNORECASE)
        
    # Mengubah Download Via menjadi tautan yang bisa diklik (Markdown style)
    teks = re.sub(r'Download Via', 'Yang Mau Cuss Request [DISINI](https://t.me/+0S7aEJ6a3FZlYTY1)', teks, flags=re.IGNORECASE)
    
    footer = "\n\nSalam dari Via @Colectionn_My"
    return teks.strip() + footer

async def main():
    print("--- MODE 1 TUJUAN AKTIF --- 🎀")
    try:
        await client.connect()
        if not await client.is_user_authorized(): return
        
        markup = [Button.url("Channel Utama 💎", "https://t.me/colectionn_my")]
        
        last_id = 0
        if os.path.exists("last_id.txt"):
            with open("last_id.txt", "r") as f:
                c = f.read().strip()
                if c: last_id = int(c)

        async for msg in client.iter_messages(SUMBER, min_id=last_id, limit=None, reverse=True):
            if msg.action or not msg.media:
                continue
            
            # --- FILTER: Melewati postingan New Episode Released ATAU New TV Show Added ---
            if msg.text and (re.search(r'New Episode Released', msg.text, re.IGNORECASE) or 
                             re.search(r'New TV Show Added', msg.text, re.IGNORECASE)):
                print(f"⏭ Melewati ID {msg.id} (Filter detected)")
                
                # Update last_id agar tidak memproses ulang pesan ini di masa depan
                last_id = msg.id
                with open("last_id.txt", "w") as f: f.write(str(last_id))
                continue
            
            try:
                # Siapkan teks dengan format markdown yang sama
                cap = proses_teks_custom(msg.text) if msg.text else "Update Baru 🎬"
                
                # Kirim hanya ke Tujuan 1
                await client.send_message(TUJUAN_1, cap, file=msg.media, buttons=markup, parse_mode='md')
                print(f"✅ Berhasil Kirim ID {msg.id} ke Tujuan 1")
                
                # Update ID setelah berhasil kirim
                last_id = msg.id
                with open("last_id.txt", "w") as f: f.write(str(last_id))
                
                await asyncio.sleep(5) 
                
            except Exception as e:
                print(f"⚠️ Gagal di ID {msg.id}: {e}")
                
    except Exception as e: print(f"❌ Error: {e}")

if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
