from mody import Mody
from pyrogram import Client, filters

bot_token = Mody.ELHYBA

api_id = Mody.API_ID
api_hash = Mody.API_HASH
app = Client("nb", api_id, api_hash, bot_token=bot_token)


app.start()


@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text(f"Hello")


app.run()

