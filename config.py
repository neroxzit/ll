import os
class Config:
    API_ID= 
    API_HASH=""
    TOKEN=""
    SUDO = list(int(i) for i in os.environ.get("SUDO", "1404114574").split(" "))
    START_IMG=""
    BOT_ID=1013
    BOT_USERNAME=""
    BOT_NAME=""
