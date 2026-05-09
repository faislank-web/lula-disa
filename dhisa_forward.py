def proses_teks_custom(teks, tipe_tujuan):
    if not teks: return ""
    
    # Pembersihan dasar
    teks = re.sub(r'[*_`~\[\]]', '', teks)
    teks = re.sub(r'https?://\S+', '', teks)
    teks = re.sub(r't\.me/\S+', '', teks)
    teks = re.sub(r'@\S+', '', teks)
    
    # Kamus dasar
    kamus = {
        "New TV Show Added!": "Series Update",
        "New Movie Added!": "Movie Update",
        "New Episode Released": "Episode Baru Tersedia"
    }
    
    # Logika perbedaan sesuai keinginan Anda
    if tipe_tujuan == "tujuan_1":
        kamus["Download Via"] = "silakan Request ke Bunda"
        footer = "\n\n\nby Dhisa @nontonbarengFM"
    else:
        kamus["Download Via"] = "silakan Request ke Admin @anmdni"
        footer = "\n\n\nby Admin @anmpanen138"

    for lama, baru in kamus.items():
        teks = re.sub(re.escape(lama), baru, teks, flags=re.IGNORECASE)
        
    return teks.strip() + footer

async def main():
    print("--- MODE KIRIM GANDA: DHISA & ADMIN --- 🎀")
    try:
        await client.connect()
        if not await client.is_user_authorized(): return
        
        # DEFINISI TOMBOL SESUAI TUJUAN
        markup_1 = [Button.url("Channel Utama 💎", "https://t.me/nontonbarengFM")]
        markup_2 = [Button.url("Channel Utama 💎", "https://t.me/anmpanen138")]
        
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
                # 1. Kirim ke TUJUAN_1 (Gaya Bunda)
                caption_1 = proses_teks_custom(msg.text, "tujuan_1") if msg.text else "Update Baru 🎬"
                await client.send_message(TUJUAN_1, caption_1, file=msg.media, buttons=markup_1)
                
                # 2. Kirim ke TUJUAN_2 (Gaya Admin)
                caption_2 = proses_teks_custom(msg.text, "tujuan_2") if msg.text else "Update Baru 🎬"
                await client.send_message(TUJUAN_2, caption_2, file=msg.media, buttons=markup_2)
                
                print(f"✅ Berhasil Forward ID: {msg.id} ke kedua grup")
                
                last_id = msg.id
                with open("last_id.txt", "w") as f: f.write(str(last_id))
                
                # Jeda agar aman dari spam filter Telegram
                await asyncio.sleep(5) 
                
            except Exception as e:
                print(f"⚠️ Gagal di ID {msg.id}: {e}")
                
    except Exception as e: 
        print(f"❌ Error: {e}")
