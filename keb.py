from telebot import *
from telebot.types import *
from time import sleep, time
from database_main import *

# from keepAlive import keep_alive


import telebot, time
from time import time
from telebot import types
from functions_to_my_bots import *
import messagesBots

# My_id = IsDevloper()


def Decor(text, type=[None, "b", "s", "del", "pre", "user", "url"], id=None, url=None):
    if type != None:
        if type == "b":
            return f"<b>{text}</b>"

        elif type == "s":
            return f"<s>{text}</s>"

        elif type == "del":
            return f"<del>{text}</del>"

        elif type == "pre":
            return f"<code>{text}</code>"

        elif type == "user":
            return f"""<a href='tg://user?id={id}'>  {text}  </a>"""

        elif type == "url":
            return f"<a href={url}>{text}</a>"


def must_sub(bot, msg, Group_ID, InlineKeyboardMarkup, InlineKeyboardButton):
    # Create an invite link class that contains info about the created invite link using create_chat_invite_link() with parameters
    invite = bot.create_chat_invite_link(
        Group_ID, member_limit=1, expire_date=int(time()) + 45
    )  # Here, the link will auto-expire in 45 seconds
    InviteLink = invite.invite_link  # Get the actual invite link from 'invite' class

    mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
    mrkplink.add(
        InlineKeyboardButton(bot.get_chat(Group_ID).title, url=InviteLink)
    )  # Added Invite Link to Inline Keyboard

    m = bot.send_message(
        msg.chat.id, Ismessage(), reply_markup=mrkplink, reply_to_message_id=msg.id
    )
    return m
    
def join_members(message: types.Message):
    global senderMsg
    if check_muted(message.from_user.id):
        senderMsg = [message.from_user, message.id]
        user = message.from_user
        full_name = str(user.first_name) + " " + str(user.last_name)
        username = str(user.username)
        Ids = int(user.id)
        msg = message.text
        name = Decor(full_name, id=Ids, type="user")
        if message.text != "/almortagel":
            if showGloblaReply(message.text):
                bot.send_message(
                    message.chat.id,
                    Decor(showGloblaReply(message.text), "b"),
                    parse_mode="HTML",
                    reply_to_message_id=message.id,
                )
                
def mycommands_on():
    mrk = ReplyKeyboardMarkup(row_width=6)

    ttns = [
        KeyboardButton("تلاوات"),
        KeyboardButton("عبد الباسط"),
        ]
    stns = [
        KeyboardButton(text="نقشبندي"),
        KeyboardButton(text="استوري"),
        ],
    ttnns = [
        KeyboardButton(text="افاتار شباب"),
        KeyboardButton(text="افاتار بنات"),
    ]
    mrk.add(*ttns)
    mrk.add(*stns)
    mrk.add(*ttnns)
    return mrk
    
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "تلاو" or text == "تلاوات" or text == "تلاوة":
        voice_url = "https://t.me/EIEI06/" + str(random.randint(24, 618))
        bot.send_voice(message.chat.id, voice_url, caption="« صلي على سيدنا محمد ﷺ »", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton('✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton('✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech')
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "عبدالباسط":
        voice_url = "https://t.me/telawatnader/" + str(random.randint(7, 265))
        bot.send_voice(message.chat.id, voice_url, caption="🥹♥ ¦ تـم اختيـار الشيخ عبدالباسط لـك", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton('✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton('✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech')
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "استوري" or text == "استوريات":
        voice_url = "https://t.me/yoipopl/" + str(random.randint(2, 140))
        bot.send_voice(message.chat.id, voice_url, caption="🥹♥ ¦ تـم اختيـار استوري لـك", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton('✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton('✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech')
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "نقشبندي" or text == "الشيخ نقشبندي":
        voice_url = "https://t.me/ggcnjj/" + str(random.randint(2, 114))
        bot.send_voice(message.chat.id, voice_url, caption="🥹♥ ¦ تـم اختيـار الشيخ نقشبندي لـك", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton('✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton('✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech')            

@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "افاتار شباب" or text == "صور شباب":
        voicee_url = "https://t.me/vgbmm/" + str(random.randint(2, 148))
        bot.send_photo(message.chat.id, voicee_url, caption="🥹♥ ¦ تـم اختيـار افاتار شباب لـك", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton('✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton('✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech') 
@bot.message_handler(func=lambda message: True)
def msgs(message):
    text = message.text
    if text == "افاتار بنات" or text == "صور بنات":
        voicee_url = "https://t.me/vvyuol/" + str(random.randint(2, 216))
        bot.send_photo(message.chat.id, voicee_url, caption="🥹♥ ¦ تـم اختيـار افاتار بنات لـك", reply_to_message_id=message.message_id, reply_markup=telebot.types.InlineKeyboardMarkup().row(
            telebot.types.InlineKeyboardButton('✧ - المطور 🌐', url='https://t.me/Almortagel_12'),
            telebot.types.InlineKeyboardButton('✧ - قناة مطور البوت', url='https://t.me/AlmortagelTech') 