#
# Copyright (C) 2021-2023 by Stetch, < https://github.com/TeamStetch >.
#
# This file is part of < https://github.com/TeamStetch/Nightosphere > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamStetch/Nightosphere/blob/master/LICENSE >
#
# All rights reserve

from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from strings.filters import command
from Nightosphere import app
from Nightosphere.core.call import NightoX
from Nightosphere.utils import bot_sys_stats
from Nightosphere.utils.decorators.language import language
from config import BANNED_USERS, MUSIC_BOT_NAME, PING_IMG_URL
from strings import get_command

### Commands
PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(
    command(PING_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@language
async def ping_com(_client, message: Message, _):
    response = await message.reply_animation(
        animation=PING_IMG_URL,
        caption=_["ping_1"],
    )
    start = datetime.now()
    pytgping = await NightoX.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            MUSIC_BOT_NAME, resp, UP, DISK, CPU, RAM, pytgping
        )
    )
