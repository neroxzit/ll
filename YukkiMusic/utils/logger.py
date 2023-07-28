#⚡MOHAMED HELAL⚡

from config import LOG, LOG_GROUP_ID
from YukkiMusic import app
from YukkiMusic.utils.database import is_on_off
from pyrogram.types import (InlineKeyboardButton,CallbackQuery,InlineKeyboardMarkup)

async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        if message.from_user:
            useri =f"`{message.from_user.id}`"
            user =f"{message.from_user.mention}"
        else:
            useri ="لا يـوجد ايـدي"
            user ="لا يـوجد اسـم"
        if message.chat.username:
            await app.send_message(LOG_GROUP_ID,f"""
"**
•⚡• ســـ‌ــــــورس ســـتـــيـــتـــشـــفـــاـــي•⚡•

━━━━━━━━━━━━━━━━━━━

•⚡• مــعــلــومـــات الــشــات •⚡•

• اســـم الــشـــات : {message.chat.title}

• ايـــــدي الــشــات : {message.chat.id}

━━━━━━━━━━━━━━━━━━━

•⚡• مــعــلــومـــات الــمــســتــخــدم •⚡•

• الــمــســتــخــدم : {user}

• ايــــــدي المــســتــخــدم : {useri}

━━━━━━━━━━━━━━━━━━━

•⚡• مــعــلــومـــات الــتــشــغــيــل •⚡•

• رســالـــه الــتــشــغــيــل : {message.text}

• نـــوع الــتــشــغــيــل :  {streamtype}

━━━━━━━━━━━━━━━━━━━
• قــنــاة : [ســـ‌ــــــورس ســـتـــيـــتـــشـــفـــاـــي](https://t.me/stetchfy)
━━━━━━━━━━━━━━━━━━━**""",disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.chat.title, url=f"https://t.me/{message.chat.username}")],]),)
        else:
            try:
            	invitelink = await app.export_chat_invite_link(message.chat.id)
            	await app.send_message(LOG_GROUP_ID,
f"""**
•⚡• ســـ‌ــــــورس ســـتـــيـــتـــشـــفـــاـــي •⚡•

━━━━━━━━━━━━━━━━━━━

•⚡• مــعــلــومـــات الــشــات •⚡•

• اســـم الــشـــات : {message.chat.title}

• ايـــــدي الــشــات : {message.chat.id}

━━━━━━━━━━━━━━━━━━━

•⚡• مــعــلــومـــات الــمــســتــخــدم •⚡•

• الــمــســتــخــدم : {user}

• ايــــــدي المــســتــخــدم : {useri}

━━━━━━━━━━━━━━━━━━━

•⚡• مــعــلــومـــات الــتــشــغــيــل •⚡•

• رســالـــه الــتــشــغــيــل : {message.text}

• نـــوع الــتــشــغــيــل :  {streamtype}

━━━━━━━━━━━━━━━━━━━
• قــنــاة : [ســـ‌ــــــورس ســـتـــيـــتـــشـــفـــاـــي](https://t.me/stetchfy)
━━━━━━━━━━━━━━━━━━━**""",disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(message.chat.title, url=f"{invitelink}")],]),)
            except:
            	return await message.reply_text("**قــم بـتـفـعـيـل صـلاحـيـة دعـوه الـمـسـتـخـدمـيـن فـي الـجـروب ✗**")