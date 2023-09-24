#
# Copyright (C) 2021-2023 by Stetch, < https://github.com/TeamStetch >.
#
# This file is part of < https://github.com/TeamStetch/Nightosphere > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamStetch/Nightosphere/blob/master/LICENSE >
#
# All rights reserve

import aiohttp

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def NightoXbin(text):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link
