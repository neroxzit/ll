#
# Copyright (C)  2021-2024 by TeamStetch@Github, < https://github.com/TeamStetch >.
#
# This file is part of < https://github.com/TeamStetch/StetchfyBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamStetch/StetchfyBot/blob/master/LICENSE >
#
# All rights reserved.

from Stetchfy.plugins.play.filters import command
from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from Stetchfy import app
from Stetchfy.core.call import Stetch
from Stetchfy.utils.database import is_music_playing, music_on
from Stetchfy.utils.decorators import AdminRightsCheckCB

# Commands
RESUME_COMMAND = get_command("RESUME_COMMAND")


@app.on_message(
    command(RESUME_COMMAND)
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheckCB
async def resume_com(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Stetch.resume_stream(chat_id)
    if message.sender_chat:
        mention = f'<a href=tg://user?id={message.chat.id}>{message.chat.title}</a>'
    else:
        mention = message.from_user.mention
    await message.reply_text(
        _["admin_4"].format(mention)
    )
