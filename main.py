import asyncio
from telethon import TelegramClient, events, Button
from telethon.sessions import StringSession

# --- DATA AKSES ---
API_ID = 25754026
API_HASH = '1f92e666a7f053ca4413e1136437c352'
RAW_SESSION = '1BVtsOHcBuyDqGsgYZELUzOQooVO0K-D7QxPJi4aZ2zq5C3M9UDojZKrez2U3yfOXv9J5A0D8_XAUUo5MSkucszYEJoXuEK4NRo_Mir4FxuxQAe4DY8X5-cNv9E0z-yy-g9_9IR30VBBChBDx566GGkrbEjykycfYyL7jaLvUn0T1yLYoYHrXDxNFPj0luzzIdzVUk-49Nm8s3bfhAy7KpTE6maAW5gT18drf8HKgNvPsBaHpBw0To8cYJHUjM9nPvUAvMN30NER2FYtfiaAZ7IuMa3VDu2fnwRJjf5EGC_MWpnzvVlj2HBfoOc9A6lkEW23LimJ16Ve8Kq3eRtumhiq1WhEkoI8='

# Pastikan session bersih total
FINAL_SESSION = RAW_SESSION.strip()

client = TelegramClient(StringSession(FINAL_SESSION), API_ID, API_HASH, sequential_updates=True)

async def main():
    print("--- MENCOBA LOGIN KE TELEGRAM ---")
    try:
        # Kita pakai start() tanpa parameter agar tidak menunggu input manual
        await client.connect()
        if not await client.is_user_authorized():
            print("❌ SESSION TIDAK VALID / EXPIRED! Silakan buat baru di Colab.")
            return
        
        me = await client.get_me()
        print(f"🤖 BERHASIL LOGIN SEBAGAI: {me.first_name}")
        
        # Tes kirim satu pesan ke grup untuk memastikan koneksi
        await client.send_message(-1003473467525, "🚀 Forwarder Aktif! Memulai tarik history...", reply_to=5318)
        
        print("🔍 Memulai proses history...")
        async for msg in client.iter_messages(-1002186281759, limit=None, reverse=True):
            # Logika kirim sama seperti sebelumnya...
            # (Untuk tes, kita coba login-nya dulu saja sampai muncul nama Kakak)
            pass

    except Exception as e:
        print(f"❌ ERROR TERDETEKSI: {e}")

if __name__ == '__main__':
    asyncio.run(main())
