from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup

@Client.on_message(filters.private & filters.incoming & filters.command("help"))
async def yardim(bot, msg):
    await bot.send_message(
        msg.chat.id,
        "**Beni nasıl kullanacağını öğren 🔐**\n" + Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons),
    )
