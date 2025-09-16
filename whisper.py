import logging
from pyrogram import Client, idle
import Config
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

app = Client(
    "Whisper-Bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="WhisperBot"),
)

if __name__ == "__main__":
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("API_ID veya API_HASH geçersiz!")
    except AccessTokenInvalid:
        raise Exception("BOT_TOKEN geçersiz!")

    try:
        uname = app.get_me().username
        print(f"@{uname} başarıyla başlatıldı!")
    except Exception as e:
        print(f"Kullanıcı bilgisi alınamadı: {e}")

    idle()
    app.stop()
    print("Bot durduruldu. Hoşça kal!")
