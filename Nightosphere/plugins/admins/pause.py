#
# Copyright (C) 2021-2023 by Stetch, < https://github.com/TeamStetch >.
#
# This file is part of < https://github.com/TeamStetch/Nightosphere > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamStetch/Nightosphere/blob/master/LICENSE >
#
# All rights reserve

from pyrogram import filters
from pyrogram.types import Message
from strings.filters import command
from Nightosphere import app
from Nightosphere.core.call import NightoX
from Nightosphere.utils.database import is_music_playing, music_off
from Nightosphere.utils.decorators import AdminRightsCheck, AdminRightsCheckCB
from config import BANNED_USERS
from strings import get_command

# Commands
PAUSE_COMMAND = get_command("PAUSE_COMMAND")



@app.on_message(
    command(PAUSE_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await NightoX.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention)
    )

@app.on_message(
    command(PAUSE_COMMAND)
    & filters.channel
    & ~BANNED_USERS
)

@AdminRightsCheckCB
async def stop_music_ch(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await Anon.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    if message.sender_chat:
        mention = f'<a href=tg://user?id={message.chat.id}>{message.chat.title}</a>'
    else:
        mention = message.from_user.mention
    await message.reply_text(
        _["admin_9"].format(mention)
    )