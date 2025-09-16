from pyrogram.types import InlineKeyboardButton

class Data:
    START = """
Selam {}.
{}'ye hoş geldin!

Ben Fısıldayanların Ustasıyım (Game of Thrones'taki Varys gibi).

Beni kullanarak grup veya kanallarda arkadaşına gizli mesaj gönderebilirsin (ben olmasam bile).
Sadece sen ve o arkadaş mesajı görebilecek, diğerleri göremez.

Nasıl kullanılacağını görmek için aşağıdaki 'Nasıl Kullanılır?' butonuna tıkla.

By @StarkBots
    """

    home_buttons = [
        [InlineKeyboardButton("🔒 Fısılda Gönder 🔒", switch_inline_query="")],
        [InlineKeyboardButton("🏠 Ana Sayfaya Dön 🏠", callback_data="home")],
    ]

    buttons = [
        [InlineKeyboardButton("🔒 Fısılda Gönder 🔒", switch_inline_query="")],
        [
            InlineKeyboardButton("Nasıl Kullanılır ❔", callback_data="help"),
            InlineKeyboardButton("🎪 Hakkında 🎪", callback_data="about")
        ],
        [InlineKeyboardButton("♥ Daha Fazla Harika Bot ♥", url="https://t.me/StarkBots")],
        [InlineKeyboardButton("🎨 Destek Grubu 🎨", url="https://t.me/StarkBotsChat")],
    ]

    HELP = """
Mesaj göndermek için aşağıdaki formatı kullanın:

`@WhisperStarkBot mesajınız arkadaş_username/id`
    """

    ABOUT = """
**Bot Hakkında**

Bot oluşturucu: @StarkBots

Kaynak Kod : [Buraya Tıkla](https://github.com/StarkBotsIndustries/WhisperBot)

İlham Alan : nnbbot

Framework : [Pyrogram](https://docs.pyrogram.org)

Dil : [Python](https://www.python.org)

Geliştirici : @StarkProgrammer
    """
