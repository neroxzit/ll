from mody import Mody
import requests

token = Mody.ELHYBA
tkn = int(token)
chat_id = Mody.OWNER
urlp = "https://t.me/CC_UG5"
url = f"https://api.telegram.org/bot{tkn}/getChat?chat_id={chat_id}"

req = requests.get(url).json()
print(req)
