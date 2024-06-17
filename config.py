import os

# You Can Get API ID And API HASH From: https://core.telegram.org/api/obtaining_api_id

API_ID = int(os.getenv("API_ID", "14837825"))

API_HASH = os.getenv("API_HASH", "0ed849f5e7ab2df61d969317de2ca64c")

token = os.getenv("BOT_TOKEN", "7002307293:AAFuZLjS_3KIWJUKg-RzxqC5em1zWC_bKiw") #Telegram BoT Token, You Can Create One From: @BotFather

ADMIN = int(os.getenv("ADMIN", "1404114574")) #The ID of Account That Will Use The BoT