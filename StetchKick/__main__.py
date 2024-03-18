from StetchKick import app,START_IMG,BOT_USERNAME,BOT_NAME,LOG
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery 

START_MSG="""
هلا **{}** , انا {},
البوت متخصص في تصفية الجروبات لو احتجت تعرف اي حاجة دوس خيار  المساعدة.
"""
START_BUTTONS=InlineKeyboardMarkup (
      [
      [
         InlineKeyboardButton (text="➕ اضفني الى مجموعة ➕",url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
      ],
      [
         InlineKeyboardButton (text="المساعدة",callback_data="help_back")
      ]
      ]
)

HELP_MSG="""
** كل الأوامر يمكن استخدامها فقط في المجموعات

⨷ /banall : حظر جميع الأعضاء في المجموعة

⨷ /unbanall : إلغاء حظر جميع الأعضاء في المجموعة

⨷ /kickall : طرد جميع الأعضاء في المجموعة

⨷ /muteall : كتم جميع الأعضاء في المجموعة

⨷ /unmuteall : إلغاء كتم جميع الأعضاء في المجموعة (ستبقى القائمة في قيود الأعضاء المحددين ولكن سيتم إزالة جميع القيود)

⨷/unpinall : إلغاء تثبيت جميع الرسائل في المجموعة.
"""




@app.on_message(filters.command("start"))
async def start(_,msg):
    await msg.reply_photo(
     photo=START_IMG,
     caption=START_MSG.format(msg.from_user.mention,BOT_NAME),
     reply_markup=START_BUTTONS)

@app.on_callback_query(filters.regex("help_back"))
async def help_back(_,callback_query: CallbackQuery):
    query=callback_query.message
    await query.edit_caption(HELP_MSG)    



if __name__ == "__main__":
    LOG.info("started")
    app.run()
