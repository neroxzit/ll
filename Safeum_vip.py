import os
import sys
import time
import requests
import random
import webbrowser
from os import system, name
from ssl import CERT_NONE
from gzip import decompress
from random import choice, choices
from concurrent.futures import ThreadPoolExecutor
from json import dumps
import pyfiglet

# Attempt to import websocket and install if not present
try:
    from websocket import create_connection
except ImportError:
    system('pip install websocket-client')
    from websocket import create_connection

failed = 0
success = 0
retry = 0
accounts = []

def generate_random_password(length=12):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(choices(characters, k=length))

def work():
    global failed, success, retry
    username = choice('qwertyuioplkjhgfdsazxcvbnm') + ''.join(choices('qwertyuioplkjhgfdsazxcvbnm1234567890', k=12))
    password = generate_random_password()
    try:
        con = create_connection(
            "wss://193.200.173.45/Auth",
            header={
                "app": "com.safeum.android",
                "host": None,
                "remoteIp": "193.200.173.45",
                "remotePort": "8080",
                "sessionId": "b6cbb22d-06ca-41ff-8fda-c0ddeb148195",
                "time": "2023-04-30 12:13:32",
                "url": "wss://51.79.208.190/Auth"
            },
            sslopt={"cert_reqs": CERT_NONE}
        )
        con.send(dumps({
            "action": "Register",
            "subaction": "Desktop",
            "locale": "en_IN",
            "gmt": "+05",
            "password": {
                "m1x": "aefb63e82a28d0f7864c9162e97014e062e2d82961a2cfdfa2d795ebe597cbd0",
                "m1y": "36708d26797e41be1528c777db8d2679f2bc26f2356798e499f4004f5e119a88",
                "m2": "4b03e693bff7381edb8d81687f0daf7ab2291258cb28eb3200c0db7870a6a91c",
                "iv": "a924eefd30f6138eb47a1e500e1f0e9b",
                "message": "4caf0b1bf8d2f9e8da57069ce4aed5013d0c745bdbfa0ff59bf43e6d2f1b0c88fd979c155529348bdbf3baabd1ff8669d50613c260918a6f93ab5d576779795ac13dd4804f42198b2866d1467dced3b1"
            },
            "magicword": {
                "m1x": "d20e90d862a1a3c73687ba5fdc3523d5b59b9143c5e0f62321b46e69ec6a96f6",
                "m1y": "a17a92e1eb880ff3432f98d9dc7fc16a0f59e906c85ef1dd690a6585196b082b",
                "m2": "0bdc3b308d3e224127594e53864a714ece879d846a74196835b2b7554eda73ad",
                "iv": "bb3ee985ea37262ef61f1b3db7fbbede",
                "message": "6fcb86db8feea00fc0d46ca1c9590b74"
            },
            "magicwordhint": "0000",
            "login": str(username),
            "devicename": "Xiaomi 23128PC33I",
            "softwareversion": "1.1.0.2300",
            "nickname": "rqhi9wb8er8jw5",
            "os": "AND",
            "deviceuid": "5f8d62999fe0bd86",
            "devicepushuid": "*eB6Q8j1TSUCg-Xz8cOnqbG:APA91bHBo1vUF4B_b6ohA7aNshKALxlhPztOxtOAxYgB1rvs1n45KPmCysnJmUKRG46UKNB9wUXJuk34AXsNKr0Q_lYsbhyleeTuFFrSq2P_SOGFjcOy1D6kRXpDeMsyhueqz6R9aEue",
            "osversion": "and_13.0.0",
            "id": "364651978"
        }))
        gzip = decompress(con.recv()).decode('utf-8')
        if '"status":"Success"' in gzip:
            success += 1
            accounts.append(f'{username}  :  "aaaa"')
            with open('SafeumakVip.txt', 'a') as f:
                f.write(f'{username}  :  "aaaa"\n\n')
        else:
            failed += 1
    except:
        retry += 1

start = ThreadPoolExecutor(max_workers=1000)
while True:
    start.submit(work)
    print('\n\n\n' + ' ' * 25 + 'Success : ' + str(success) + '\n\n\n' + ' ' * 25 + 'Failed : ' + str(failed) + '\n\n\n' + ' ' * 25 + 'Retry : ' + str(retry))
    if success > 0:
        print("\n Accounts: \n" + "\n".join(accounts))
    system("cls" if name == "nt" else "clear")