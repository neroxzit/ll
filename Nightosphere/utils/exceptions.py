#
# Copyright (C) 2021-2023 by Stetch, < https://github.com/TeamStetch >.
#
# This file is part of < https://github.com/TeamStetch/Nightosphere > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamStetch/Nightosphere/blob/master/LICENSE >
#
# All rights reserve


class AssistantErr(Exception):
    def __init__(self, errr: str):
        super().__init__(errr)
