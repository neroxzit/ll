import os
import json
from pymongo import MongoClient
# main.py

from database import db
try:
    from telethon.sessions import StringSession
    import asyncio, re, json, shutil
    from kvsqlite.sync import Client as uu
    from telethon.tl.types import KeyboardButtonUrl
    from telethon.tl.types import KeyboardButton, ReplyInlineMarkup
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.tl.types import DocumentAttributeFilename
    import time, datetime, random 
    from datetime import timedelta
    from telethon.errors import (
        ApiIdInvalidError,
        PhoneNumberInvalidError,
        PhoneCodeInvalidError,
        PhoneCodeExpiredError,
        SessionPasswordNeededError,
        PasswordHashInvalidError
    )
    from plugins.messages import *
    from plugins.get_gift import *
except:
    os.system("pip install telethon kvsqlite")
    try:
        from telethon.sessions import StringSession
        import asyncio, re, json, shutil
        from kvsqlite.sync import Client as uu
        from telethon.tl.types import KeyboardButtonUrl
        from telethon.tl.types import KeyboardButton
        from telethon import TelegramClient, events, functions, types, Button
        from telethon.tl.types import DocumentAttributeFilename
        import time, datetime, random 
        from datetime import timedelta
        from telethon.errors import (
            ApiIdInvalidError,
            PhoneNumberInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            SessionPasswordNeededError,
            PasswordHashInvalidError
        )
        from plugins.messages import *
        from plugins.get_gift import *
    except Exception as errors:
        print('An Erorr with: ' + str(errors))
        exit(0)

        

API_ID = "14837825"
API_HASH = "0ed849f5e7ab2df61d969317de2ca64c"
admin = -1404114574
DB_URL = ("DB_URL", "mongodb+srv://nora:nora@nora.f0ea0ix.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = ("DB_NAME", "memadder")
# Replace with your bot token
token = "7063341831:AAFX80TtAyeQyW4rqZpx9mwBWco1xzrAnzA"
client = TelegramClient('BotSession', API_ID, API_HASH).start(bot_token=token)
bot = client


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

async def remove_account(event):
    user_id = event.chat_id
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("- ارسل رقم الهاتف للحساب الذي تود حذفه")
        txt = await x.get_response()
        phone_number = txt.text.replace("+", "").replace(" ", "")
        acc = db.get("accounts")
        for i, account in enumerate(acc):
            if account['phone_number'] == phone_number:
                del acc[i]
                db.set("accounts", acc)
                await x.send_message("- تم حذف الحساب بنجاح ✅")
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
                            await bot.send_message(admin, f"**• رابط تليجرام مميز جديد 🥳**\n\n- الرابط : {gift_link}\n- الرقم : {phone_number}\n- تاريخ الاستلام : {message_date}\n- مدة الاشتراك : {subscription_duration} شهور")
                            #await bot.send_message(admin, f"**• رابط تليجرام مميز جديد 🥳**\n\n- الرابط : https://t.me/giftcode/{gift_code}\n- رقم الهاتف : `{i['phone_number']}`\n- مدة الاشتراك : {subscription_duration} شهور")
                            count += 1
                    except Exception as e:
                        print(f"Error while fetching gift code: {e}")
        await bot.send_message(admin, f"- تم الانتهاء من فحص الحسابات تم ايجاد {count} روابط")
#########################################################################################
async def filter_invalid_accounts():
    acc = db.get("accounts")
    valid_accounts = []
    invalid_accounts = 0
    for i in acc:
        try:
            async with TelegramClient(StringSession(i["session"]), API_ID, API_HASH) as app:
                await app.connect()
                if not await app.is_user_authorized():
                    raise Exception("Unauthorized session")
                valid_accounts.append(i)
        except Exception:
            invalid_accounts += 1
    db.set("accounts", valid_accounts)
    return len(valid_accounts), invalid_accounts
#########################################################################################
async def add_account(event):
    async with bot.conversation(event.chat_id) as x:
        await x.send_message("- ارسل رقم الهاتف الذي تريد إضافته:")
        txt = await x.get_response()
        phone_number = txt.text.strip()

        app = TelegramClient(StringSession(), API_ID, API_HASH)
        await app.connect()
        password = None
        try:
            code = await app.send_code_request(phone_number)
            await x.send_message("- تم ارسال كود التحقق الخاص بك علي حسابك علي تليجرام.\n\n- ارسل الكود بالتنسيق التالي : 1 2 3 4 5")
            txt = await x.get_response()
            code = txt.text.replace(" ", "")
            await app.sign_in(phone_number, code, password=None)
            me = await app.get_me()
            full_name = (me.first_name or "") + (" " + me.last_name if me.last_name else "")
            username = me.username if me.username else ""
            user_id = me.id
            string_session = app.session.save()
            await db.add_account(phone_number, full_name, username, user_id, string_session)
            await x.send_message("- تم حفظ الحساب بنجاح ✅")
        except (PhoneCodeInvalidError):
            await x.send_message("كود التحقق الذي أرسلته **غير صحيح.**")
        except (PhoneCodeExpiredError):
            await x.send_message("كود التحقق الذي أرسلته **منتهي الصلاحية.**")
        except (SessionPasswordNeededError):
            await x.send_message("- ارسل رمز التحقق بخطوتين الخاص بحسابك")
            txt = await x.get_response()
            password = txt.text
            try:
                await app.sign_in(password=password)
                me = await app.get_me()
                full_name = (me.first_name or "") + (" " + me.last_name if me.last_name else "")
                username = me.username if me.username else ""
                user_id = me.id
                string_session = app.session.save()
                await db.add_account(phone_number, full_name, username, user_id, string_session)
                await x.send_message("- تم حفظ الحساب بنجاح ✅")
            except (PasswordHashInvalidError):
                await x.send_message("كلمة المرور التي أرسلتها **غير صحيحة.**")
            except Exception as e:
                print(e)
                await x.send_message("حدث خطأ ما!")


#########################################################################################
@client.on(events.NewMessage(pattern="/start", func = lambda x: x.is_private))
async def start(event):
    user_id = event.chat_id
    if await db.config.find_one({"banned_users": user_id}):
        await event.respond("أنت محظور من استخدام هذا البوت.")
    async with bot.conversation(event.chat_id) as x:
        buttons = [
            [
                Button.inline("اضافة حساب", data="add"),
                Button.inline("ازالة حساب", data="remove_account"),
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
                Button.inline("تصفية الحسابات غير المتصلة", data="filter_invalid_accounts"),
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
                Button.inline("ازالة حساب", data="remove_account"),
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
                Button.inline("تصفية الحسابات غير المتصلة", data="filter_invalid_accounts"),
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
    
    if data == "filter_invalid_accounts":
        valid_count, invalid_count = await filter_invalid_accounts()
        await event.reply(f"- تم تصفية الحسابات بنجاح\n- عدد الحسابات الصالحة: {valid_count}\n- عدد الحسابات غير الصالحة: {invalid_count}")

    if data == "remove_account":
        await remove_account(event)
    if data == "display_accounts":
        await display_accounts(event)
    if data == "add":
        await add_account(event)
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
        
print("Bot is running...")                    
client.run_until_disconnected()

