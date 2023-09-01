import os
import requests
import json 
import re
import pyrogram 
from pyrogram import *
from pyrogram.types import *
import time
import re
from dateutil import tz
from datetime import datetime
from Stetchfy import app




@app.on_message(filters.regex("مباريات اليوم")& filters.group)
async def matchs(client, message):
    yu=tz.gettz("Africa/Cairo")
    mody=datetime.now(tz=yu)
    current_time = mody.strftime("%m/%d/%Y")
    match_get = requests.get(f"https://www.filgoal.com/matches/ajaxlist?date={current_time}")
    getMatche = json.loads(match_get.text)
    match_text = f"᚛ مباريات اليوم ⦂ {mody.strftime('%d/%m/%Y')}\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n"
    count =0
    for i in range(len(getMatche)):
        #الفريق الاول
        fName = getMatche[i]['HomeTeamName']
        #الفريق الثاني
        sName = getMatche[i]['AwayTeamName']
        #صوره فرقه الاولي
        flogo = getMatche[i]['HomeTeamLogoUrl']
        #صوره الفرقه الثانيه
        slogo = getMatche[i]['AwayTeamLogoUrl']
        #اسكور الفريق الاول
        HomeScore = getMatche[i]['HomeScore'] if getMatche[i]['HomeScore'] is not None else "-"
        #اسكور الفريق الثاني
        AwayScore = getMatche[i]['AwayScore'] if getMatche[i]['AwayScore'] is not None else "-"
        #اسم البطوله
        ChampionshipName = getMatche[i]['ChampionshipName']
        #تفاصيل البطوله
        RoundName = getMatche[i]['RoundName'] if getMatche[i]['RoundName'] is not None else "غير معروف"
        #الوقت
        encoded_value = getMatche[i]['Date'] if getMatche[i]['Date'] is not None else "غير معروف"
        timestamp = int(re.search(r'\d+', encoded_value).group()) // 1000
        dt = datetime.fromtimestamp(timestamp)
        time_12h = dt.strftime("%I:%M %p")

        #استاد المتش
        StadiumName = "غير معروف" if getMatche[i]['StadiumName'] is None else getMatche[i]['StadiumName']
        #حالت المباراه
        MatchStatus = getMatche[i]['MatchStatusHistory'][0]['MatchStatusName']
        match_text += "᚛ البطوله ⦂ {}\n᚛ تفاصيل البطوله ⦂ {}\n᚛ مباراة ⦂ {}  {} 🆚 {}  {} \n᚛ توقيت المباراة ⦂ {}\n᚛ حالة المباراة ⦂ {}\n᚛ استاد المباراة ⦂ {}\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌\n".format(ChampionshipName,RoundName,fName,HomeScore,AwayScore,sName,time_12h,MatchStatus,StadiumName)
        count += 1
    if count == 0 :
        return await message.reply(f"لا يوجد مباريات اليوم")
    await message.reply(f"{match_text}")
            