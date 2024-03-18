from StetchKick import app,BOT_ID,SUDO
from pyrogram import filters,enums
from pyrogram.types import ChatPermissions

@app.on_message(filters.command("banall") & filters.user(SUDO))
async def ban_all(_,msg):
    chat_id=msg.chat.id    
    bot=await app.get_chat_member(chat_id,BOT_ID)
    bot_permission=bot.privileges.can_restrict_members==True    
    if bot_permission:
        async for member in app.get_chat_members(chat_id):       
            try:
                    await app.ban_chat_member(chat_id, member.user.id)                   
            except Exception:
                pass
    else:
        await msg.reply_text("انت لست مشرف في البوت")  


@app.on_message(filters.command("unbanall") & filters.user(SUDO))
async def unban_all(_,msg):
    chat_id=msg.chat.id   
    x = 0
    bot=await app.get_chat_member(chat_id,BOT_ID)
    bot_permission=bot.privileges.can_restrict_members==True 
    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)       
            try:
                    await app.unban_chat_member(chat_id,banned_users[x])                                        
            except Exception:
                pass
    else:
        await msg.reply_text("انت لست مشرف في البوت")

@app.on_message(filters.command("kickall") & filters.user(SUDO))
async def ban_all(_,msg):
    chat_id=msg.chat.id    
    bot=await app.get_chat_member(chat_id,BOT_ID)
    bot_permission=bot.privileges.can_restrict_members==True    
    if bot_permission:
        async for member in app.get_chat_members(chat_id):       
            try:
                    await app.ban_chat_member(chat_id, member.user.id)
                    await app.unban_chat_member(chat_id,member.user.id)                    
            except Exception:
                pass
    else:
        await msg.reply_text("انت لست مشرف في البوت")          

@app.on_message(filters.command("muteall") & filters.user(SUDO))
async def mute_all(_,msg):
    chat_id=msg.chat.id    
    bot=await app.get_chat_member(chat_id,BOT_ID)
    bot_permission=bot.privileges.can_restrict_members==True    
    if bot_permission:
        async for member in app.get_chat_members(chat_id):       
            try:
                    await app.restrict_chat_member(chat_id, member.user.id,ChatPermissions(can_send_messages=False))                                        
            except Exception:
                pass
    else:
        await msg.reply_text("انت لست مشرف في البوت")  

@app.on_message(filters.command("unmuteall") & filters.user(SUDO))
async def unmute_all(_,msg):
    chat_id=msg.chat.id   
    x = 0
    bot=await app.get_chat_member(chat_id,BOT_ID)
    bot_permission=bot.privileges.can_restrict_members==True 
    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
            banned_users.append(m.user.id)       
            try:
                    await app.restrict_chat_member(chat_id,banned_users[x], ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_polls=True,can_add_web_page_previews=True,can_invite_users=True))

            except Exception as e:
                print(e)
    else:
        await msg.reply_text("انت لست مشرف في البوت")


@app.on_message(filters.command("unpinall") & filters.user(SUDO))
async def unpin_all(_,msg):
    chat_id=msg.chat.id    
    bot=await app.get_chat_member(chat_id,BOT_ID)
    bot_permission=bot.privileges.can_pin_messages==True
    if bot_permission:
        try:
            await app.unpin_all_chat_messages(chat_id)
            await msg.reply_text("تم الغاء تثبيت جميع الرسائل  بنجاح.")
        except Exception:
            pass
    else:
        await msg.reply_text("قم يمنح البوت الصلاحيات اولا")