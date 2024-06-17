import os
import json
import asyncio
import re
import shutil
from kvsqlite.sync import Client as uu
from telethon.sessions import StringSession
from telethon.tl.types import KeyboardButtonUrl, KeyboardButton, DocumentAttributeFilename
from telethon import TelegramClient, events, functions, types, Button
import time
import datetime
import random 
from datetime import timedelta
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from telethon.utils import get_peer_id  # Import the utility function for peer ID
from plugins.messages import *
from plugins.get_gift import *
from config import *
        
if not os.path.isdir('database'):
    os.mkdir('database')

# Replace with your bot token
client = TelegramClient('BotSession', API_ID, API_HASH).start(bot_token=token)
bot = client

#Create DataBase

db = uu('database/stetch.ss', 'bot')

if not db.exists("accounts"):
    db.set("accounts", [])

if not db.exists("bad_guys"):
    db.set("bad_guys", [])

if not db.exists("force"):
   db.set("force", [])

#########################################################33##
async def display_accounts(event):
    acc = db.get("accounts")
    if acc:
        message = "قائمة الحسابات المسجلة:\n"
        for account in acc:
            message += f"الاسم: {account['full_name']}\n"
            message += f"رقم الهاتف: {account['phone_number']}\n"
            message += f"المعرف: {account['username']}\n"
            message += f"الايدي: {account['id']}\n"
            message += "=========================\n"
        await event.respond(message)
    else:
        await event.respond("لا توجد حسابات مسجلة في قاعدة البيانات")

#############################################################
async def logout_account(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("- ارسل رقم الهاتف للحساب الذي تود تسجيل الخروج منه")
        txt = await x.get_response()
        phone_number = txt.text.replace("+", "").replace(" ", "")
        acc = db.get("accounts")
        for i, account in enumerate(acc):
            if account['phone_number'] == phone_number:
                async with TelegramClient(StringSession(account['session']), API_ID, API_HASH) as app:
                    await app.connect()
                    await app.log_out()
                del acc[i]
                db.set("accounts", acc)
                await x.send_message("- تم تسجيل الخروج بنجاح ✅")
                return
        await x.send_message("- لم يتم العثور على هذا الرقم في قاعدة البيانات")

######################################################################################### 
async def  get_gift(event):
    async with bot.conversation(event.chat_id) as x:
        await event.answer(f"- تم بدا جلب روابط المميز من الحسابات برجاء انتظار اشعار", alert=True)
        acc = db.get("accounts")
        count = 0
        for i in acc:
            async with TelegramClient(StringSession(i["session"]), API_ID, API_HASH) as X:
                async for message in X.iter_messages(777000, limit=None):
                    try:
                        if isinstance(message.action, types.MessageActionGiftCode):
                            gift_code = message.action.slug
                            subscription_duration = message.action.months
                            message_date = message.date.strftime("%m/%d • %I:%M %p")
                            gift_link = f"https://t.me/giftcode/{gift_code}"
                            phone_number = i['phone_number']
                            boosted_chat_username = "N/A"
                            if hasattr(message.action, 'boost_peer'):
                                boosted_chat_id = message.action.boost_peer
                                boosted_chat = await X.get_entity(boosted_chat_id)
                                if boosted_chat.username:
                                    boosted_chat_username = f"[{boosted_chat.title}](https://t.me/{boosted_chat.username})"
                            await bot.send_message(ADMIN, f"**• رابط تليجرام مميز جديد 🥳**\n\n"
                                                         f"- الرابط : {gift_link}\n"
                                                         f"- الرقم : {phone_number}\n"
                                                         f"- تاريخ الاستلام : {message_date}\n"
                                                         f"- مدة الاشتراك : {subscription_duration} شهور\n" 
                                                         f"- اسم قناة السحب: {boosted_chat_username}\n"                                               
                                                         )
                            count += 1
                    except Exception as e:
                        print(f"Error while fetching gift code: {e}")
        if count == 0:
            await bot.send_message(ADMIN, "لا يوجد أي روابط في أي حساب.")
        else:
            await bot.send_message(ADMIN, f"- تم الانتهاء من فحص الحسابات تم ايجاد {count} روابط")

#########################################################################################    
@client.on(events.NewMessage(pattern="/start", func = lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    bans = db.get('bad_guys') if db.exists('bad_guys') else []
    async with bot.conversation(event.chat_id) as x:
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("ازالة حساب", data="logout_account"),
            ],
            [
                Button.inline("جلب الروابط", data="get_gift"),
            ],    
            [
                Button.inline("الانضمام لقناة", data="join_channel"),
                Button.inline("مغادرة قناة", data="leave_channel"),
            ],
            [
                Button.inline("نسخة احتياطية", data="zip_all"),
                Button.inline("جلب جلسة", data="get_session"),
            ],
            [
                Button.inline("عدد حسابات البوت", data="get_accounts_count"),
            ],
            [
                Button.inline("تنظيف الحسابات", data="check"),
                Button.inline("مغادرة القنوات", data="leave_all"),
            ],
            [
                
                Button.inline("عرض الحسابات المسجلة", data="display_accounts"),
            ],
        ]
        await event.reply("**- مرحبا بك في بوت جلب روابط المميز من حساباتك المسجلة 🔗**\n\n- اختر من الازرار ادناه ما تود فعله.", buttons=buttons)
        
        
        
@client.on(events.callbackquery.CallbackQuery())
async def start_lis(event):
    data = event.data.decode('utf-8')
    user_id = event.chat_id
    if data == "back" or data == "cancel":
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("ازالة حساب", data="logout_account"),
            ],
            [
                Button.inline("جلب الروابط", data="get_gift"),
            ],    
            [
                Button.inline("الانضمام لقناة", data="join_channel"),
                Button.inline("مغادرة قناة", data="leave_channel"),
            ],
            [
                Button.inline("نسخة احتياطية", data="zip_all"),
                Button.inline("جلب جلسة", data="get_session"),
            ],
            [
                Button.inline("عدد حسابات البوت", data="get_accounts_count"),
            ],
            [
                Button.inline("تنظيف الحسابات", data="check"),
                Button.inline("مغادرة القنوات", data="leave_all"),
            ],
            [
                
                Button.inline("عرض الحسابات المسجلة", data="display_accounts"),
            ],
        ]
        await event.edit("**- مرحبا بك في بوت جلب روابط المميز من حساباتك المسجلة 🔗**\n\n- اختر من الازرار ادناه ما تود فعله.", buttons=buttons)
    if data == "logout_account":
        await logout_account(event)
    if data == "display_accounts":
        await display_accounts(event)
    if data == "add":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("✔️الان ارسل رقمك مع رمز دولتك , مثال :+201000000000")
            txt = await x.get_response()
            phone_number = txt.text.replace("+", "").replace(" ", "")
            app = TelegramClient(StringSession(), API_ID, API_HASH, device_model="STETCH CTRL")
            await app.connect()
            password=None
            try:
                code = await app.send_code_request(phone_number)
            except (ApiIdInvalidError):
                await x.send_message("ʏᴏᴜʀ **ᴀᴩɪ_ɪᴅ** ᴀɴᴅ **ᴀᴩɪ_ʜᴀsʜ** ᴄᴏᴍʙɪɴᴀᴛɪᴏɴ ᴅᴏᴇsɴ'ᴛ ᴍᴀᴛᴄʜ ᴡɪᴛʜ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴩᴩs sʏsᴛᴇᴍ.")
                return
            except (PhoneNumberInvalidError):
                await x.send_message("ᴛʜᴇ **ᴩʜᴏɴᴇ_ɴᴜᴍʙᴇʀ** ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ᴅᴏᴇsɴ'ᴛ ʙᴇʟᴏɴɢ ᴛᴏ ᴀɴʏ ᴛᴇʟᴇɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ.")
                return
            await x.send_message("- تم ارسال كود التحقق الخاص بك علي حسابك علي تليجرام.\n\n- ارسل الكود بالتنسيق التالي : 1 2 3 4 5")
            txt = await x.get_response()
            code = txt.text.replace(" ", "")
            try:
                await app.sign_in(phone_number, code, password=None)
                me = await app.get_me()
                full_name = (me.first_name or "") + (" " + me.last_name if me.last_name else "")
                username = "@" + me.username if me.username else "لا يوجد"
                user_id = me.id
                string_session = app.session.save()
                data = {"phone_number": phone_number, "two-step": "لا يوجد", "session": string_session, "full_name": full_name, "username": username,"id": user_id}
                accounts = db.get("accounts")
                accounts.append(data)
                db.set("accounts", accounts)
                text = f'**✅ تم تسجيل الدخول بنجاح\n👤 الاسم : {full_name}\n🆔 بطاقة تعريف : {user_id}\n📞 رقم الهاتف : +{phone_number}\n📛 المعرف : {username}\n/start**'
                await x.send_message(text)
            except (PhoneCodeInvalidError):
                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴡʀᴏɴɢ.**")
                return
            except (PhoneCodeExpiredError):
                await x.send_message("ᴛʜᴇ ᴏᴛᴩ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs **ᴇxᴩɪʀᴇᴅ.**")
                return
            except (SessionPasswordNeededError):
                await x.send_message("- ارسل رمز التحقق بخطوتين الخاص بحسابك")
                txt = await x.get_response()
                password = txt.text
                try:
                    await app.sign_in(password=password)
                    me = await app.get_me()
                    full_name = (me.first_name or "") + (" " + me.last_name if me.last_name else "")
                    username = "@" + me.username if me.username else "لا يوجد"
                    user_id = me.id
                    string_session = app.session.save()
                    data = {"phone_number": phone_number, "two-step": password, "session": string_session, "full_name": full_name, "username": username,"id": user_id}
                    accounts = db.get("accounts")
                    accounts.append(data)
                    db.set("accounts", accounts)
                    text = f'**✅ تم تسجيل الدخول بنجاح\n👤 الاسم : {full_name}\n🆔 بطاقة تعريف : {user_id}\n📞 رقم الهاتف : +{phone_number}\n📛 المعرف : {username}\n/start**'
                    await x.send_message(text)
                except (PasswordHashInvalidError):
                    await x.send_message("ᴛʜᴇ ᴩᴀssᴡᴏʀᴅ ʏᴏᴜ'ᴠᴇ sᴇɴᴛ ɪs ᴡʀᴏɴɢ.")
                    return
                except Exception as e:
                    print(e)
                    await x.send_message("حدث خطأ ما!")
                    return
    if data == "get_accounts_count":
        acc = db.get("accounts")
        await event.answer(f"- عدد الحسابات المسجلة ; {len(acc)}", alert=True)
    if data == "get_gift":
        await get_gift(event)
    if data == "join_channel":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل الان رابط او معرف القناة التي تريد الانضمام لها بكل الحسابات")
            ch = await x.get_response()
            if "@" not in ch.text:
                if "/t.me/" not in ch.text:
                    await x.send_message(f"- ارسل رابط او معرف القناة بشكل صحيح")
                    return 
            channel = ch.text.replace("https://t.me/", "").replace("http://t.me/", "").replace("@", "")
            acc = db.get("accounts")
            true, false = 0, 0
            await x.send_message(f"- تم بدء الانضمام من {len(acc)} حساب")
            for i in acc:
                xx = await join_channel(i["session"], channel)
                if xx is True:
                    true += 1
                else:
                    false += 1
            await x.send_message(f"**- تم انتهاء طلبك بنجاح ✅**\n\n- نجاح : {true}\n- فشل : {false}")
    if data == "leave_channel":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل الان رابط او معرف القناة التي تريد المغادرة منها بكل الحسابات")
            ch = await x.get_response()
            if "@" not in ch.text:
                if "/t.me/" not in ch.text:
                    await x.send_message(f"- ارسل رابط او معرف القناة بشكل صحيح")
                    return 
            channel = ch.text.replace("https://t.me/", "").replace("http://t.me/", "").replace("@", "")
            acc = db.get("accounts")
            true, false = 0, 0
            await x.send_message(f"- تم بدء المغادرة من {len(acc)} حساب")
            for i in acc:
                xx = await leave_channel(i["session"], channel)
                if xx is True:
                    true += 1
                else:
                    false += 1
            await x.send_message(f"**- تم انتهاء طلبك بنجاح ✅**\n\n- نجاح : {true}\n- فشل : {false}")
    if data == 'zip_all':
        folder_path = f"./database"
        zip_file_name = f"database.zip"
        zip_file_nam = f"database"
        try:
            shutil.make_archive(zip_file_nam, 'zip', folder_path)
            with open(zip_file_name, 'rb') as zip_file:
                await client.send_file(user_id, zip_file, attributes=[DocumentAttributeFilename(file_name="database.zip")])
            os.remove(zip_file_name)
        except Exception as a:
            print(a)
    if data == "leave_all":
        buttons = [
            [
                Button.inline("تأكيد ✅", data="leave_all_channels"),
                Button.inline("الغاء ❌", data="cancel"),
            ]
        ]
        await event.edit("**- هل تود فعلاً تأكيد المغادرة من كل الحسابات؟**", buttons=buttons)
    if data == "leave_all_channels":
        async with bot.conversation(event.chat_id) as x:
            acc = db.get("accounts")
            await event.edit(f"**- تم بدء مغادرة كل القنوات من {len(acc)} حساب, سيصلك اشعار عند الانتهاء **")
            true, false = 0, 0
            await x.send_message(f"- تم بدء المغادرة من {len(acc)} حساب")
            for i in acc:
                xx = await leave_all(i["session"])
                if xx is True:
                    true += 1
                else:
                    false += 1
            await x.send_message(f"**- تم انتهاء مغادرة القنوات بنجاح ✅**\n\n- نجاح : {true}\n- فشل : {false}")
    
    if data == "check":
        buttons = [
            [
                Button.inline("تأكيد ✅", data="check_accounts"),
                Button.inline("الغاء ❌", data="cancel"),
            ]
        ]
        await event.edit("**- هل تود فعلاً تأكيد المغادرة من كل الحسابات؟**", buttons=buttons)
    if data == "check_accounts":
        async with bot.conversation(event.chat_id) as x:
            acc = db.get("accounts")
            await event.edit(f"**- تم بدء فحص كل الحسابات من {len(acc)} حساب, سيصلك اشعار عند الانتهاء **")
            true, false = 0, 0
            await x.send_message(f"- تم بدء فحص {len(acc)} حساب")
            for i in acc:
                xx = await check(i["session"])
                if xx is True:
                    true += 1
                else:
                    false += 1
            await x.send_message(f"**- تم انتهاء فحص الحسابات بنجاح ✅**\n\n- حسابات شغالة : {true}\n- حسابات محذوفة : {false}")
    if data == "get_session":
        async with bot.conversation(event.chat_id) as x:
            await x.send_message("- ارسل الان رقم الهاتف الذي قمت بتسجيلة للبوت لجلب السيشن منه")
            txt = await x.get_response()
            phone_number = txt.text.replace("+", "").replace(" ", "")
            acc = db.get("accounts")
            for i in acc:
                if phone_number == i['phone_number']:
                    text = f"• رقم الهاتف : {phone_number}\n\n- التحقق بخطوتين : {i['two-step']}\n\n- الجلسة : `{i['session']}"
                    await x.send_message(text)
                    return
            await x.send_message("- لم يتم العثور علي هذا الرقم ضمن قائمة الحسابات")
        
print("Bot Started \nHave Fun <3")                    
client.run_until_disconnected()

