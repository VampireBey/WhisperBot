import ast
import json
from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChosenInlineResult
)
from pyrogram.errors import UsernameInvalid, UsernameNotOccupied, PeerIdInvalid
from WhisperBot.database.whisper_sql import Whispers
from WhisperBot.database.users_sql import Users
from WhisperBot.database import SESSION
from WhisperBot.bot_users import check_for_users

main = [
    InlineQueryResultArticle(
        title="Fısıltı Botu",
        input_message_content=InputTextMessageContent(
            "Mesajınızın sonuna alıcı kullanıcının @username veya ID'sini yazın."
        ),
        url="https://t.me/StarkBots",
        description="Mesajınızın sonuna alıcı kullanıcının @username veya ID'sini yazın.",
        thumb_url="https://telegra.ph/file/33af12f457b16532e1383.jpg",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Daha Fazla Bilgi", url="https://t.me/WhisperStarkBot?start=start")],
                [InlineKeyboardButton("🔒 Fısıltı Gönder 🔒", switch_inline_query="")],
                [InlineKeyboardButton("♥ Daha Fazla Harika Bot ♥", url="https://t.me/StarkBots")]
            ]
        ),
    )
]

@Client.on_chosen_inline_result()
async def _chosen(bot: Client, result: ChosenInlineResult):
    if not result.query:
        return
    sender_id = result.from_user.id
    inline_msg_id = result.inline_message_id
    try:
        parts = result.query.split(" ")
        message = " ".join(parts[:-1])
        receiver = parts[-1]
        target_user = await bot.get_users(receiver)
        receiver_id = target_user.id
        SESSION.add(Whispers(inline_msg_id, message))
        user_record = SESSION.query(Users).get(sender_id)
        if user_record:
            user_record.target_user = str(target_user)
        else:
            SESSION.add(Users(sender_id, str(target_user)))
        SESSION.commit()
        await check_for_users([sender_id, receiver_id])
    except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, IndexError):
        SESSION.add(Whispers(inline_msg_id, result.query))
        SESSION.commit()


async def previous_target(sender_id):
    user_record = SESSION.query(Users).get(sender_id)
    if user_record and user_record.target_user:
        target_user = json.loads(user_record.target_user)
        receiver = target_user["id"]
        data_list = [sender_id, receiver]
        name = target_user.get("first_name", "")
        if "last_name" in target_user:
            name += target_user["last_name"]
        text1 = f"{name} kişisine bir fısıltı mesajı"
        text2 = "Sadece o kişi mesajı açabilir."
        mention = f"[{name}](tg://user?id={receiver})"
        results = [
            InlineQueryResultArticle(
                title=text1,
                input_message_content=InputTextMessageContent(
                    f"{mention} kişisine bir fısıltı mesajı. {text2}"
                ),
                url="https://t.me/StarkBots",
                description=text2,
                thumb_url="https://telegra.ph/file/33af12f457b16532e1383.jpg",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🔐 Mesajı Göster 🔐", callback_data=str(data_list))]]
                )
            ),
            main[0]
        ]
    else:
        results = main
    return results


@Client.on_inline_query()
async def answer(bot: Client, query):
    query_text = query.query
    sender_id = query.from_user.id
    query_list = query_text.split(" ")

    if not query_text:
        await query.answer(
            results=main,
            switch_pm_text="🔒 Fısıltı Gönderimi Öğren",
            switch_pm_parameter="start"
        )
        return

    if len(query_list) == 1:
        results = await previous_target(sender_id)
        await query.answer(
            results=results,
            switch_pm_text="🔒 Fısıltı Gönderimi Öğren",
            switch_pm_parameter="start"
        )
        return

    if len(query_list) >= 2:
        mentioned_user = query_list[-1]
        try:
            mentioned_user = ast.literal_eval(mentioned_user)
        except (ValueError, SyntaxError):
            pass

        if isinstance(mentioned_user, str) and not mentioned_user.startswith("@"):
            results = await previous_target(sender_id)
            await query.answer(
                results=results,
                switch_pm_text="🔒 Fısıltı Gönderimi Öğren",
                switch_pm_parameter="start"
            )
            return

        try:
            target_user = await bot.get_users(mentioned_user)
            receiver_id = target_user.id
            data_list = [sender_id, receiver_id]
            name = target_user.first_name
            if target_user.last_name:
                name += target_user.last_name
            text1 = f"{name} kişisine bir fısıltı mesajı"
            text2 = "Sadece o kişi mesajı açabilir."
            await query.answer(
                results=[
                    InlineQueryResultArticle(
                        title=text1,
                        input_message_content=InputTextMessageContent(
                            f"{target_user.mention} kişisine bir fısıltı mesajı. {text2}"
                        ),
                        url="https://t.me/StarkBots",
                        description=text2,
                        thumb_url="https://telegra.ph/file/33af12f457b16532e1383.jpg",
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("🔐 Mesajı Göster 🔐", callback_data=str(data_list))]]
                        )
                    )
                ],
                switch_pm_text="🔒 Fısıltı Gönderimi Öğren",
                switch_pm_parameter="start"
            )
            await check_for_users(receiver_id)
        except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid, IndexError):
            results = await previous_target(sender_id)
            await query.answer(
                results=results,
                switch_pm_text="🔒 Fısıltı Gönderimi Öğren",
                switch_pm_parameter="start"
            )

    await check_for_users(sender_id)
