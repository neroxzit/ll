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
from Stetchfy.utils.database import set_loop
from Stetchfy.utils.decorators import AdminRightsCheck, AdminRightsCheckCB

# Commands
STOP_COMMAND = get_command("STOP_COMMAND")
STOP_COMMAND_chh = get_command("STOP_COMMAND_chh")


@app.on_message(
    command(STOP_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Stetch.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_9"].format(message.from_user.mention)
    )


@app.on_message(
    command(STOP_COMMAND_chh)
    & filters.channel
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminRightsCheckCB
async def stop_music_ch(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Stetch.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    if message.sender_chat:
        mention = f'<a href=tg://user?id={message.chat.id}>{message.chat.title}</a>'
    else:
        mention = message.from_user.mention
    await message.reply_text(
        _["admin_9"].format(mention)
    )
