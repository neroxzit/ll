from pyrogram import filters, Client
from Stetchfy import app
import asyncio
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from Stetchfy.core.call import Stetch
from Stetchfy.utils.database import *
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError,AlreadyJoinedError)


@app.on_message(filters.regex("^مين في الكول$")
 
    )
async def strcall(client, message):
    assistant = await group_assistant(Stetch,message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("./assets/stetch.mp3"), stream_type=StreamType().pulse_stream)
        text="الناس القاعده في المكالمه تكذب:\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k =0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut="يرغوي "
            else:
                mut="ساكت "
            user = await client.get_users(participant.user_id)
            k +=1
            text +=f"{k}➤{user.mention}➤{mut}\n"
        text += f"\nعددهم : {len(participants)}\n✔️"    
        await message.reply(f"{text}")
        await asyncio.sleep(7)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply(f"المكالمه مش مفتوحه اصلا")
    except TelegramServerError:
        await message.reply(f"ارسل الامر تاني في مشكله في سيرفر التلجرام")
    except AlreadyJoinedError:
        text="االناس القاعده في المكالمه تكذب:\n\n"
        participants = await assistant.get_participants(message.chat.id)
        k =0
        for participant in participants:
            info = participant
            if info.muted == False:
                mut="يرغوي"
            else:
                mut="ساكت "
            user = await client.get_users(participant.user_id)
            k +=1
            text +=f"{k}➤{user.mention}➤{mut}\n"
        text += f"\nعددهم : {len(participants)}\n✔️"    
        await message.reply(f"{text}")
